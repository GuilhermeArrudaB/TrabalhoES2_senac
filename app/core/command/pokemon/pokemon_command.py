from app.core.command.abc_command import Command
from app.core.facades.entity_facade import EntityFacade
from app.models.pokemon_model import Pokemon
from typing import List, Optional
import openpyxl
from pathlib import Path

class GetPokemonCommand(Command):
    def __init__(self, facade: EntityFacade, pokemon_id: str):
        self.facade = facade
        self.pokemon_id = pokemon_id

    async def execute(self) -> Optional[Pokemon]:
        return await self.facade.get_entity(self.pokemon_id)


class GetPokemonListCommand(Command):
    def __init__(self, facade: EntityFacade, limit: int, offset: int):
        self.facade = facade
        self.limit = limit
        self.offset = offset

    async def execute(self) -> List[Pokemon]:
        return await self.facade.get_entity_list(self.limit, self.offset)


class GetTopPokemonCommand(Command):
    def __init__(self, facade: EntityFacade, limit: int = 10):
        self.facade = facade
        self.limit = limit
        self.output_dir = Path("output")
        self.output_file = self.output_dir / "top_pokemon.xlsx"

    async def execute(self) -> str:
        self.output_dir.mkdir(exist_ok=True)

        pokemon_list = await self.facade.get_entity_list(limit=50, offset=0)

        pokemon_stats = []
        for pokemon in pokemon_list:
            total_stat = sum(stat.base_stat for stat in (pokemon.stats or []))
            pokemon_stats.append((pokemon, total_stat))

        top_pokemon = sorted(pokemon_stats, key=lambda x: x[1], reverse=True)[:self.limit]

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Top Pokémon"

        headers = ["Name", "ID", "Total Base Stat", "HP", "Attack", "Defense",
                   "Special Attack", "Special Defense", "Speed"]
        ws.append(headers)

        for pokemon, total_stat in top_pokemon:
            stats_dict = {stat.stat.name: stat.base_stat for stat in (pokemon.stats or [])}  # Trata stats ausente
            row = [
                pokemon.name,
                pokemon.id,
                total_stat,
                stats_dict.get("hp", 0),
                stats_dict.get("attack", 0),
                stats_dict.get("defense", 0),
                stats_dict.get("special-attack", 0),
                stats_dict.get("special-defense", 0),
                stats_dict.get("speed", 0)
            ]
            ws.append(row)

        wb.save(self.output_file)
        return str(self.output_file)