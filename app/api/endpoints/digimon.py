from fastapi import APIRouter, HTTPException
from app.core.facades.entity_facade import EntityFacade
from app.core.iterator.digimon_iterator import DigimonIterator
from app.models.digimon_model import Digimon
from typing import List

router = APIRouter()

@router.get("/{digimon_name}", response_model=Digimon)
async def get_digimon(digimon_name: str):
    try:
        facade = EntityFacade(entity_type="digimon")
        digimon = await facade.get_entity(digimon_name)
        if not digimon:
            raise HTTPException(status_code=404, detail="Digimon não encontrado")
        return digimon
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar Digimon: {str(e)}")

@router.get("/", response_model=List[Digimon])
async def get_digimon_list(limit: int = 20, offset: int = 0):
    try:
        facade = EntityFacade(entity_type="digimon")
        return await facade.get_entity_list(limit, offset)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar lista de Digimon: {str(e)}")

@router.get("/iterated/", response_model=List[Digimon])
async def get_digimon_iterated(limit: int = 10):
    try:
        facade = EntityFacade(entity_type="digimon")
        iterator = DigimonIterator(facade, limit=20)
        result = []
        async for digimon in iterator:
            result.append(digimon)
            if len(result) >= limit:
                break
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iterar Digimon: {str(e)}")