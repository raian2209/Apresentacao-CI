from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()


class HealthCheck(BaseModel):
    status: str = "OK"


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/teste")
async def teste():
    return {"message": "Teste CI-CD"}


@app.get(
    "/health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on.
    """
    return HealthCheck(status="OK")


def cpu_bound_task(number: int) -> int:
    """
    Simula uma tarefa pesada de CPU (ex: processamento de imagem, criptografia).
    Se não for testada com valores negativos, a cobertura de 'branches' falhará.
    """
    if number < 0:
        return 0  # <--- RAMIFICAÇÃO 1
    
    # Simula cálculo pesado
    result = sum(i * i for i in range(number))
    return result

def legacy_io_task(file_name: str) -> str:
    """
    Simula uma operação de I/O bloqueante (ex: driver antigo de banco de dados, leitura de arquivo).
    """
    if not file_name:
        raise ValueError("Filename cannot be empty") # <--- RAMIFICAÇÃO 2
    
    if file_name == "error.txt":
        raise IOError("Disk error simulated") # <--- RAMIFICAÇÃO 3

    time.sleep(0.1) # Bloqueia a thread propositalmente
    return f"Processed {file_name}"

# --- ENDPOINTS ---

@app.post("/sync/compute/{number}", status_code=status.HTTP_200_OK)
def compute_endpoint(number: int):
    """
    Endpoint síncrono. O FastAPI rodará isso em uma thread pool.
    """
    # Se o teste chamar apenas com número positivo, a linha do 'if number < 0'
    # na função cpu_bound_task nunca será executada -> COBERTURA CAI.
    result = cpu_bound_task(number)
    return {"input": number, "computed_result": result}

@app.get("/sync/process-file")
def process_file_endpoint(file_name: str = ""):
    """
    Endpoint com múltiplas possibilidades de erro.
    """
    try:
        result = legacy_io_task(file_name)
        return {"status": "success", "data": result}
    except ValueError as e:
        # Se não escrevermos um teste que passe string vazia,
        # esta linha não é coberta.
        raise HTTPException(status_code=400, detail=str(e))
    except IOError as e:
        # Se não escrevermos um teste com file_name="error.txt",
        # esta linha não é coberta.
        raise HTTPException(status_code=500, detail="Internal Legacy Error")