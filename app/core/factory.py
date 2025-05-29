from abc import ABC, abstractmethod
import httpx
from app.core.config import settings
from typing import List, Dict, Any, Optional


class APIServiceFactory(ABC):
    @abstractmethod
    async def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_entity_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        pass


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


class DigimonAPIFactory(APIServiceFactory):
    async def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings.DIGIMON_API_URL}/digimon/name/{entity_id}")
                response.raise_for_status()
                return response.json()[0]  # Digimon API retorna uma lista com um item
            except (httpx.HTTPStatusError, IndexError):
                return None

    async def get_entity_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.DIGIMON_API_URL}/digimon")
            response.raise_for_status()
            data = response.json()
            # Simula paginação, já que a Digimon API não suporta limit/offset diretamente
            start = offset
            end = offset + limit
            return data[start:end] if start < len(data) else []