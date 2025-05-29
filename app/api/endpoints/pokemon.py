from fastapi import APIRouter, HTTPException
from app.services.api_service import APIService
from app.models.pokemon_model import Pokemon
from typing import List

router = APIRouter()

@router.get("/{pokemon_id}", response_model=Pokemon)
async def get_pokemon(pokemon_id: str):
    try:
        api_service = APIService(entity_type="pokemon")
        pokemon = await api_service.fetch_entity(pokemon_id)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokémon não encontrado")
        return pokemon
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar Pokémon: {str(e)}")

@router.get("/", response_model=List[Pokemon])
async def get_pokemon_list(limit: int = 20, offset: int = 0):
    try:
        api_service = APIService(entity_type="pokemon")
        return await api_service.fetch_entity_list(limit, offset)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar lista de Pokémon: {str(e)}")