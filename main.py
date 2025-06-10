from fastapi import FastAPI
from app.api.endpoints import pokemon, digimon
from app.core.middlewares import LoggingMiddleware

app = FastAPI(title="API Middleware com padrões de projeto")

app.add_middleware(LoggingMiddleware)

# Registrar roteadores
app.include_router(pokemon.router, prefix="/pokemon", tags=["Pokemon"])
app.include_router(digimon.router, prefix="/digimon", tags=["Digimon"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao API Middleware"}
