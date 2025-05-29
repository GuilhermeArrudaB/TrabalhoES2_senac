from fastapi import FastAPI
from app.api.endpoints import pokemon, digimon

app = FastAPI(title="Pokémon and Digimon API Middleware com Abstract Factory")

# Registrar roteadores
app.include_router(pokemon.router, prefix="/pokemon", tags=["Pokémon"])
app.include_router(digimon.router, prefix="/digimon", tags=["Digimon"])

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Middleware da Pokémon e Digimon API"}
