import pytest
from unittest.mock import AsyncMock, patch
from app.core.facade import EntityFacade
from app.models.pokemon_model import Pokemon, PokemonAbility, Ability, PokemonType, Type
from app.models.digimon_model import Digimon
from typing import List, Optional, Union

mock_pokemon_data = {
    "id": 25,
    "name": "pikachu",
    "abilities": [
        {"ability": {"name": "static", "url": "https://pokeapi.co/api/v2/ability/9/"}, "is_hidden": False, "slot": 1}
    ],
    "types": [
        {"slot": 1, "type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"}}
    ],
    "height": 4,
    "weight": 60
}

mock_digimon_data = {
    "name": "Agumon",
    "img": "https://digimon-api.vercel.app/images/agumon.jpg",
    "level": "Rookie"
}

mock_pokemon_list_data = [
    {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
    {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"}
]

mock_digimon_list_data = [
    {"name": "Agumon", "url": "https://digimon-api.vercel.app/api/digimon/name/agumon"},
    {"name": "Gabumon", "url": "https://digimon-api.vercel.app/api/digimon/name/gabumon"}
]

@pytest.mark.asyncio
async def test_get_pokemon_success(mocker):
    mocker.patch(
        "app.services.api_service.APIService.fetch_entity",
        AsyncMock(return_value=Pokemon(**mock_pokemon_data))
    )

    facade = EntityFacade(entity_type="pokemon")

    pokemon = await facade.get_entity("pikachu")

    assert isinstance(pokemon, Pokemon)
    assert pokemon.name == "pikachu"
    assert pokemon.id == 25

@pytest.mark.asyncio
async def test_get_digimon_success(mocker):
    mocker.patch(
        "app.services.api_service.APIService.fetch_entity",
        AsyncMock(return_value=Digimon(**mock_digimon_data))
    )

    facade = EntityFacade(entity_type="digimon")

    digimon = await facade.get_entity("agumon")

    assert isinstance(digimon, Digimon)
    assert digimon.name == "Agumon"
    assert digimon.level == "Rookie"

@pytest.mark.asyncio
async def test_get_entity_not_found(mocker):
    mocker.patch(
        "app.services.api_service.APIService.fetch_entity",
        AsyncMock(return_value=None)
    )

    facade = EntityFacade(entity_type="pokemon")

    result = await facade.get_entity("unknown")

    assert result is None

@pytest.mark.asyncio
async def test_get_pokemon_list_success(mocker):
    mocker.patch(
        "app.services.api_service.APIService.fetch_entity_list",
        AsyncMock(return_value=[Pokemon(**mock_pokemon_data), Pokemon(**mock_pokemon_data)])
    )

    facade = EntityFacade(entity_type="pokemon")

    pokemon_list = await facade.get_entity_list(limit=2, offset=0)

    assert isinstance(pokemon_list, List)
    assert len(pokemon_list) == 2
    assert all(isinstance(p, Pokemon) for p in pokemon_list)
    assert pokemon_list[0].name == "pikachu"

@pytest.mark.asyncio
async def test_get_digimon_list_success(mocker):
    mocker.patch(
        "app.services.api_service.APIService.fetch_entity_list",
        AsyncMock(return_value=[Digimon(**mock_digimon_data), Digimon(**mock_digimon_data)])
    )

    facade = EntityFacade(entity_type="digimon")

    digimon_list = await facade.get_entity_list(limit=2, offset=0)

    assert isinstance(digimon_list, List)
    assert len(digimon_list) == 2
    assert all(isinstance(d, Digimon) for d in digimon_list)
    assert digimon_list[0].name == "Agumon"

@pytest.mark.asyncio
async def test_get_entity_list_internal_error(mocker):
    mocker.patch(
        "app.services.api_service.APIService.fetch_entity_list",
        AsyncMock(side_effect=Exception("Erro interno"))
    )

    facade = EntityFacade(entity_type="pokemon")

    with pytest.raises(Exception, match="Erro interno"):
        await facade.get_entity_list(limit=2, offset=0)