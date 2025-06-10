from fastapi import APIRouter, HTTPException
from app.models.pokemon_model import Pokemon
from typing import List
from app.core.facades.entity_facade import EntityFacade

router = APIRouter()

@router.get("/{pokemon_id}", response_model=Pokemon)
async def get_pokemon(pokemon_id: str):
    try:
        facade = EntityFacade(entity_type="pokemon")
        pokemon = await facade.get_entity(pokemon_id)
        if not pokemon:
            raise HTTPException(status_code=404, detail="Pokemon não encontrado")
        return pokemon
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar Pokemon: {str(e)}")

@router.get("/", response_model=List[Pokemon])
async def get_pokemon_list(limit: int = 20, offset: int = 0):
    try:
        facade = EntityFacade(entity_type="pokemon")
        return await facade.get_entity_list(limit, offset)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar lista de Pokemon: {str(e)}")