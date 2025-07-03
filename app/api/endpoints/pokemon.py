from fastapi import APIRouter, HTTPException
from app.core.command.pokemon.pokemon_command import GetTopPokemonCommand
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

@router.get("/top/", response_model=str)
async def get_top_pokemon():
    try:
        facade = EntityFacade(entity_type="pokemon")
        command = GetTopPokemonCommand(facade)
        file_path = await command.execute()
        return f"Arquivo Excel gerado: {file_path}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar arquivo Excel: {str(e)}")

@router.get("/top-stats/", response_model=str)
async def get_top_pokemon_stats():
    try:
        facade = EntityFacade(entity_type="pokemon")
        command = GetTopPokemonCommand(facade, limit=10)
        file_path = await command.execute()
        return f"Relatório dos Pokémon mais fortes gerado em: {file_path}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar relatório de Pokémon: {str(e)}")