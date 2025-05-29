from fastapi import FastAPI
from app.api.endpoints import pokemon

app = FastAPI(title="Middleware Pokemon API com padrões de projeto")

# Registrar roteadores
app.include_router(pokemon.router, prefix="/pokemon", tags=["Pokemon"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Middleware da Pokemon API"}
