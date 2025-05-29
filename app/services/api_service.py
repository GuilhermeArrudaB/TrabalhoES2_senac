from app.core.factory import PokeAPIFactory, APIServiceFactory
from app.repository.pokemon_repository import PokemonRepository
from app.models.pokemon_model import Pokemon
from typing import List, Optional


class APIService:
    def __init__(self, factory: APIServiceFactory = None):
        self.factory = factory or PokeAPIFactory()
        self.repository = PokemonRepository(self.factory)

    async def fetch_pokemon(self, pokemon_id: str) -> Optional[Pokemon]:
        pokemon_data = await self.repository.get_pokemon(pokemon_id)
        return Pokemon(**pokemon_data) if pokemon_data else None

    async def fetch_pokemon_list(self, limit: int, offset: int) -> List[Pokemon]:
        pokemon_list = await self.repository.get_pokemon_list(limit, offset)
        tasks = [self.repository.get_pokemon(pokemon["name"]) for pokemon in pokemon_list]
        results = await self.repository.execute_concurrently(tasks)
        return [Pokemon(**data) for data in results if data]
