from app.core.factory import APIServiceFactory, PokeAPIFactory, DigimonAPIFactory
from app.repository.entity_repository import EntityRepository
from app.models.pokemon_model import Pokemon
from app.models.digimon_model import Digimon
from typing import List, Optional, Union


class APIService:
    def __init__(self, entity_type: str, factory: APIServiceFactory = None):
        self.entity_type = entity_type.lower()
        if factory is None:
            if self.entity_type == "pokemon":
                factory = PokeAPIFactory()
            elif self.entity_type == "digimon":
                factory = DigimonAPIFactory()
            else:
                raise ValueError(f"Unsupported entity type: {entity_type}")
        self.repository = EntityRepository(factory)

    async def fetch_entity(self, entity_id: str) -> Optional[Union[Pokemon, Digimon]]:
        entity_data = await self.repository.get_entity(entity_id)
        if entity_data is None:
            return None
        if self.entity_type == "pokemon":
            return Pokemon(**entity_data)
        elif self.entity_type == "digimon":
            return Digimon(**entity_data)
        return None

    async def fetch_entity_list(self, limit: int, offset: int) -> List[Union[Pokemon, Digimon]]:
        entity_list = await self.repository.get_entity_list(limit, offset)
        tasks = [self.repository.get_entity(entity["name"]) for entity in entity_list]
        results = await self.repository.execute_concurrently(tasks)
        if self.entity_type == "pokemon":
            return [Pokemon(**data) for data in results if data]
        elif self.entity_type == "digimon":
            return [Digimon(**data) for data in results if data]
        return []