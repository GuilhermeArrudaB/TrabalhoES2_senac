from abc import ABC, abstractmethod
import httpx
from app.core.config import settings
from typing import List, Dict, Any


class APIServiceFactory(ABC):
    @abstractmethod
    async def get_pokemon(self, pokemon_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_pokemon_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_species(self, species_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_species_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        pass


class PokeAPIFactory(APIServiceFactory):
    async def get_pokemon(self, pokemon_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.POKEAPI_URL}/pokemon/{pokemon_id}")
            response.raise_for_status()
            return response.json()

    async def get_pokemon_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.POKEAPI_URL}/pokemon?limit={limit}&offset={offset}")
            response.raise_for_status()
            return response.json()["results"]

    async def get_species(self, species_id: str) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.POKEAPI_URL}/pokemon-species/{species_id}")
            response.raise_for_status()
            return response.json()

    async def get_species_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{settings.POKEAPI_URL}/pokemon-species?limit={limit}&offset={offset}")
            response.raise_for_status()
            return response.json()["results"]