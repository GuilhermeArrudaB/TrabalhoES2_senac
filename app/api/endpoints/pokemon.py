from fastapi import APIRouter, HTTPException
from app.services.api_service import APIService
from app.models.pokemon_model import Pokemon
from typing import List

router = APIRouter()

@router.get("/{pokemon_id}", response_model=Pokemon)
async def get_pokemon(pokemon_id: str):
    try:
        api_service = APIService()
        pokemon = await api_service.fetch_pokemon(pokemon_id)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokemon não encontrado")
        return pokemon
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar Pokemon: {str(e)}")

@router.get("/", response_model=List[Pokemon])
async def get_pokemon_list(limit: int = 20, offset: int = 0):
    try:
        api_service = APIService()
        return await api_service.fetch_pokemon_list(limit, offset)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar lista de Pokemon: {str(e)}")