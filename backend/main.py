from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import caronas, passageiros

app = FastAPI(
    title="API Caronas UFG",
    description="Backend completo com roteamento, banco PostgreSQL e autenticação.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(caronas.router)
app.include_router(passageiros.router)

@app.get("/")
def raiz_api():
    return {
        "message": "API de Caronas roando com sucesso!",
        "documentacao": "Acesse /docs no seu navegador para ver e testar as rotas rotas organizadas."
    }