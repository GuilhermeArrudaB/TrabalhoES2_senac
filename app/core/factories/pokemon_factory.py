from app.core.factories.abc_factory import APIServiceFactory
import httpx
from app.core.config import settings
from typing import List, Dict, Any, Optional

class PokeAPIFactory(APIServiceFactory):
    async def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings.POKEAPI_URL}/pokemon/{entity_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                return None

    async def get_entity_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.POKEAPI_URL}/pokemon?limit={limit}&offset={offset}")
            response.raise_for_status()
            return response.json()["results"]