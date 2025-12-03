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


def processar_pagamento(valor: float, status: str) -> str:
    if status == "pendente":      # Ramo 1
        return "Aguardando"
    elif status == "cancelado":   # Ramo 2
        return "Cancelado"
    elif valor > 1000:            # Ramo 3
        return "Alto Valor"
    else:                         # Ramo 4
        return "Processado"

def processar_pagamento(valor: float, status: str) -> str:
    if status == "pendente":      # Ramo 1
        return "Aguardando"
    elif status == "cancelado":   # Ramo 2
        return "Cancelado"
    elif valor > 1000:            # Ramo 3
        return "Alto Valor"
    else:                         # Ramo 4
        return "Processado"

def processar_pagamento(valor: float, status: str) -> str:
    if status == "pendente":      # Ramo 1
        return "Aguardando"
    elif status == "cancelado":   # Ramo 2
        return "Cancelado"
    elif valor > 1000:            # Ramo 3
        return "Alto Valor"
    else:                         # Ramo 4
        return "Processado"
