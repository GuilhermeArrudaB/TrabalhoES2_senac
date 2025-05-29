from app.core.factory import APIServiceFactory
import asyncio
from typing import List, Dict, Any, Optional


class PokemonRepository:
    def __init__(self, factory: APIServiceFactory):
        self.factory = factory

    async def get_pokemon(self, pokemon_id: str) -> Optional[Dict[str, Any]]:
        try:
            return await self.factory.get_pokemon(pokemon_id)
        except Exception:
            return None

    async def get_pokemon_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        return await self.factory.get_pokemon_list(limit, offset)

    async def get_species(self, species_id: str) -> Optional[Dict[str, Any]]:
        try:
            return await self.factory.get_species(species_id)
        except Exception:
            return None

    async def get_species_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        return await self.factory.get_species_list(limit, offset)

    async def execute_concurrently(self, tasks: List) -> List[Dict[str, Any]]:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [result for result in results if not isinstance(result, Exception)]
