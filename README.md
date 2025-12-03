# CI com FastAPI, GitHub Actions e GitOps

Este repositório contém uma aplicação FastAPI de exemplo e um pipeline de CI robusto construído com GitHub Actions. O objetivo do projeto é automatizar padronizar o desenvolvimento: desde a validação do código com testes até a padronização do codigo, seguindo as melhores práticas de GitOps.
## 🏛️ Arquitetura

Este projeto adota uma arquitetura GitOps baseada em dois repositórios distintos para garantir uma clara separação de interesses:

1.  **Repositório da Aplicação (`Apresentacao-CI` - este repositório):**

      * **Responsabilidade:** Contém o código-fonte da aplicação FastAPI, os testes automatizados (`pytest`) e a definição do contêiner (`Dockerfile`).
      * **Pipeline de CI:** O workflow valida a qualidade do código (Linting, Formatting, Commit Messages), executa testes e publica a imagem Docker versionada.

2.  **Registro de Contêiner (Docker Hub):**

      * **Responsabilidade:** Armazenar as imagens imutáveis geradas pelo pipeline, prontas para serem consumidas por orquestradores (como Kubernetes).

Link: <https://hub.docker.com/r/raian2209/hello-app>


## 🛠️ Tecnologias Utilizadas

  * **Backend:** FastAPI
  * **Testes:** Pytest
  * **Containerização:** Docker
  * **CI/CD:** GitHub Actions
  * **Registro de Contêiner:** Docker Hub



## 📁 Estrutura do Projeto

```
.
├──.github/
│   └── workflows/
│       └── ci-build-push.yml      # Definição do pipeline de CI/CD
├── tests/
│   └── test_main.py      # Testes automatizados com Pytest
├──.gitignore
├── Dockerfile            # Instruções para construir a imagem Docker
├── main.py               # Código da aplicação FastAPI
└── requirements.txt      # Dependências Python do projeto
```

## 🚀 Setup e Desenvolvimento Local

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/raian2209/pythonCI-CD.git
    cd pythonCI-CD
    ```

2.  **Crie e ative um ambiente virtual:**

    ```bash
    # Crie o ambiente
    python3 -m venv .venv

    # Ative o ambiente (Linux/macOS)
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute os testes (Opcional, mas recomendado):**

    ```bash
    pytest
    ```

5.  **Inicie o servidor de desenvolvimento:**

    ```bash
    uvicorn main:app --reload
    ```

    A aplicação estará disponível em `http://127.0.0.1:8000`.

## ⚙️ Análise do Workflow de CI/CD (`.github/workflows/main.yml`)

Este workflow automatiza o processo de teste, construção, versionamento e a proposta de implantação da aplicação.

### Gatilho (Trigger)

*   **Push de Tags (`v*`):** Dispara o processo completo de build e publicação da imagem (Release).
*   **Pull Request (`main`):** Dispara apenas as verificações de qualidade e testes para proteger a branch principal.

### 1. Job: Code Quality (`code-quality`)
Este job atua como um **Quality Gate**. Se qualquer passo falhar, o pipeline é interrompido.

1.  **Checkout & Setup:** Prepara o ambiente Python 3.10.
2.  **Check Commit Messages:**
    *   Utiliza `cz check` (Commitizen) para validar se as mensagens dos commits seguem o padrão **Conventional Commits** (ex: `feat:...`, `fix:...`). Isso é crucial para automação de changelogs.
3.  **Lint and Format (Ruff):**
    *   Verifica a formatação do código e erros lógicos/estilísticos com `ruff`. O pipeline falha se o código não estiver em conformidade.
4.  **Lint Dockerfile (Hadolint):**
    *   Analisa o `Dockerfile` em busca de violações de segurança e boas práticas (ex: rodar como root, versões não fixadas).
5.  **Run tests (Pytest):**
    *   Executa a suíte de testes com relatório de cobertura.

### 2. Job: Build & Push (`build-and-push`)
Executado apenas se o job de qualidade passar e o gatilho for uma **Tag**.

1.  **Setup Docker:** Configura QEMU e Docker Buildx.
2.  **Login:** Autenticação no Docker Hub via Secrets.
3.  **Extract Version:** Captura a versão da tag Git (ex: `v1.0.0`) para usar como tag da imagem.
4.  **Build and Push:** Constrói a imagem e envia para o Docker Hub (`${{ secrets.DOCKER_USERNAME }}/hello-app:${{ env.IMAGE_TAG }}`).

## 🏷️ Como Fazer um Release (Acionar o Pipeline)

Para criar uma nova versão da aplicação e acionar o pipeline, siga os passos:

1.  Certifique-se de que sua branch `main` está atualizada com o código que você deseja lançar.
2.  Crie uma nova tag Git localmente (seguindo o versionamento semântico):
    ```bash
    # Exemplo para a primeira versão
    git tag v0.1.0
    ```
3.  Envie a tag para o repositório remoto no GitHub:
    ```bash
    git push origin v0.1.0
    ```
    Isso acionará o workflow, que pode ser monitorado na aba "Actions" do seu repositório.

## 🔐 Configuração de Segredos

Para que o workflow funcione, os seguintes segredos devem ser configurados em **Settings \> Secrets and variables \> Actions** do repositório da aplicação:

| Secret | Descrição | Como Gerar |
| :--- | :--- | :--- |
| `DOCKER_USERNAME` | Seu nome de usuário do Docker Hub. | - |
| `DOCKER_PASSWORD` | Um Token de Acesso do Docker Hub (não sua senha). | Vá para Docker Hub \> Account Settings \> Security \> New Access Token. |
