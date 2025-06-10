from app.core.factories.abc_factory import APIServiceFactory
import httpx
from app.core.config import settings
from typing import List, Dict, Any, Optional
from app.core.adapters.digimon_adapter import DigimonAdapter

class DigimonAPIFactory(APIServiceFactory):
    def __init__(self):
        self.adapter = DigimonAdapter()

    async def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings.DIGIMON_API_URL}/digimon/name/{entity_id}")
                response.raise_for_status()
                return self.adapter.adapt(response.json()[0])
            except (httpx.HTTPStatusError, IndexError):
                return None

    async def get_entity_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.DIGIMON_API_URL}/digimon")
            response.raise_for_status()
            data = response.json()
            start = offset
            end = offset + limit
            # Aplica o adaptador a cada item da lista
            return [self.adapter.adapt(item) for item in data[start:end] if item]