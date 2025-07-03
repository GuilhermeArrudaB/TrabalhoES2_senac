from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from app.core.command.pokemon.pokemon_command import GetTopPokemonCommand
from main import app
from unittest.mock import AsyncMock, patch
from app.models.pokemon_model import Pokemon, PokemonAbility, Ability, PokemonType, Type

client = TestClient(app)

# Dados de exemplo para mock
mock_pokemon_data = {
    "id": 25,
    "name": "pikachu",
    "abilities": [
        {"ability": {"name": "static", "url": "https://pokeapi.co/api/v2/ability/9/"}, "is_hidden": False, "slot": 1}
    ],
    "types": [
        {"slot": 1, "type": {"name": "electric", "url": "https://pokeapi.co/api/v2/type/13/"}}],
    "height": 4,
    "weight": 60,
    "stats": [
        {"base_stat": 35, "effort": 0, "stat": {"name": "hp", "url": ""}},
        {"base_stat": 55, "effort": 0, "stat": {"name": "attack", "url": ""}},
        {"base_stat": 40, "effort": 0, "stat": {"name": "defense", "url": ""}},
        {"base_stat": 50, "effort": 0, "stat": {"name": "special-attack", "url": ""}},
        {"base_stat": 50, "effort": 0, "stat": {"name": "special-defense", "url": ""}},
        {"base_stat": 90, "effort": 2, "stat": {"name": "speed", "url": ""}}
    ]
}

mock_pokemon_list_data = [
    {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
    {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"}
]


@pytest.mark.asyncio
async def test_get_pokemon_success(mocker):
    mocker.patch(
        "app.core.factories.pokemon_factory.PokeAPIFactory.get_entity",
        AsyncMock(return_value=mock_pokemon_data)
    )

    response = client.get("/pokemon/pikachu")

    assert response.status_code == 200
    assert response.json() == mock_pokemon_data
    assert response.json()["name"] == "pikachu"
    assert response.json()["id"] == 25


@pytest.mark.asyncio
async def test_get_pokemon_not_found(mocker):
    mocker.patch(
        "app.core.factories.pokemon_factory.PokeAPIFactory.get_entity",
        AsyncMock(return_value=None)
    )

    response = client.get("/pokemon/unknown")

    assert response.status_code == 404
    assert response.json() == {"detail": "Pokemon não encontrado"}


@pytest.mark.asyncio
async def test_get_pokemon_list_success(mocker):
    mocker.patch(
        "app.core.factories.pokemon_factory.PokeAPIFactory.get_entity_list",
        AsyncMock(return_value=mock_pokemon_list_data)
    )
    mocker.patch(
        "app.core.factories.pokemon_factory.PokeAPIFactory.get_entity",
        AsyncMock(side_effect=[mock_pokemon_data, mock_pokemon_data])
    )

    response = client.get("/pokemon?limit=2&offset=0")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "pikachu"  # Dados mockados
    assert response.json()[0]["id"] == 25


@pytest.mark.asyncio
async def test_get_pokemon_list_internal_error(mocker):
    mocker.patch(
        "app.core.factories.pokemon_factory.PokeAPIFactory.get_entity_list",
        AsyncMock(side_effect=Exception("Erro interno"))
    )

    response = client.get("/pokemon?limit=2&offset=0")

    assert response.status_code == 500
    assert response.json() == {"detail": "Erro ao buscar lista de Pokemon: Erro interno"}

@pytest.mark.asyncio
async def test_get_top_pokemon_stats_success(mocker, tmp_path):
    mocker.patch(
        "app.core.facades.entity_facade.EntityFacade.get_entity_list",
        AsyncMock(return_value=[Pokemon(**mock_pokemon_data), Pokemon(**mock_pokemon_data)])
    )
    mock_workbook = mocker.MagicMock()
    mocker.patch(
        "app.core.command.pokemon.pokemon_command.openpyxl.Workbook",
        return_value=mock_workbook
    )

    mock_command = mocker.MagicMock()
    mock_command.execute = AsyncMock(return_value=str(tmp_path / "top_pokemon.xlsx"))
    mock_command.output_dir = tmp_path

    mocker.patch(
        "app.core.command.pokemon.pokemon_command.GetTopPokemonCommand.execute",
        return_value=mock_command
    )

    response = client.get("/pokemon/top-stats/")
    assert response.status_code == 200
    assert response.json().startswith("Relatório dos Pokémon mais fortes gerado em:")

@pytest.mark.asyncio
async def test_get_top_pokemon_stats_error(mocker):
    mocker.patch(
        "app.core.facades.entity_facade.EntityFacade.get_entity_list",
        AsyncMock(side_effect=Exception("Erro interno"))
    )
    response = client.get("/pokemon/top-stats/")
    assert response.status_code == 500
    assert response.json() == {"detail": "Erro ao gerar relatório de Pokémon: Erro interno"}