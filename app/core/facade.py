from app.services.api_service import APIService
from app.models.pokemon_model import Pokemon
from app.models.digimon_model import Digimon
from typing import List, Optional, Union


class EntityFacade:
    def __init__(self, entity_type: str):
        self.service = APIService(entity_type=entity_type)

    async def get_entity(self, entity_id: str) -> Optional[Union[Pokemon, Digimon]]:
        return await self.service.fetch_entity(entity_id)

    async def get_entity_list(self, limit: int = 20, offset: int = 0) -> List[Union[Pokemon, Digimon]]:
        return await self.service.fetch_entity_list(limit, offset)
