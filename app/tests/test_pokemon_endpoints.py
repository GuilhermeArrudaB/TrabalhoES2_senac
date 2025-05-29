import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, patch
from app.models.pokemon_model import Pokemon, PokemonAbility, Ability, PokemonType, Type

# Inicializa o cliente de teste do FastAPI
client = TestClient(app)

# Dados de exemplo para mock
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

mock_pokemon_list_data = [
    {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"},
    {"name": "ivysaur", "url": "https://pokeapi.co/api/v2/pokemon/2/"}
]


@pytest.mark.asyncio
async def test_get_pokemon_success(mocker):
    # Mock da fábrica para retornar dados válidos
    mocker.patch(
        "app.core.factory.PokeAPIFactory.get_pokemon",
        AsyncMock(return_value=mock_pokemon_data)
    )

    # Faz a requisição ao endpoint
    response = client.get("/pokemon/pikachu")

    # Verifica o status e o conteúdo
    assert response.status_code == 200
    assert response.json() == mock_pokemon_data
    assert response.json()["name"] == "pikachu"
    assert response.json()["id"] == 25


@pytest.mark.asyncio
async def test_get_pokemon_not_found(mocker):
    # Mock da fábrica para retornar None (Pokemon não encontrado)
    mocker.patch(
        "app.core.factory.PokeAPIFactory.get_pokemon",
        AsyncMock(return_value=None)
    )

    # Faz a requisição ao endpoint
    response = client.get("/pokemon/unknown")

    # Verifica o status e a mensagem de erro
    assert response.status_code == 404
    assert response.json() == {"detail": "Pokemon não encontrado"}


@pytest.mark.asyncio
async def test_get_pokemon_list_success(mocker):
    # Mock da fábrica para a lista de Pokemon
    mocker.patch(
        "app.core.factory.PokeAPIFactory.get_pokemon_list",
        AsyncMock(return_value=mock_pokemon_list_data)
    )
    # Mock da fábrica para cada Pokemon individual
    mocker.patch(
        "app.core.factory.PokeAPIFactory.get_pokemon",
        AsyncMock(side_effect=[mock_pokemon_data, mock_pokemon_data])
    )

    # Faz a requisição ao endpoint
    response = client.get("/pokemon?limit=2&offset=0")

    # Verifica o status e o conteúdo
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "pikachu"  # Dados mockados
    assert response.json()[0]["id"] == 25


@pytest.mark.asyncio
async def test_get_pokemon_list_internal_error(mocker):
    # Mock da fábrica para simular um erro
    mocker.patch(
        "app.core.factory.PokeAPIFactory.get_pokemon_list",
        AsyncMock(side_effect=Exception("Erro interno"))
    )

    # Faz a requisição ao endpoint
    response = client.get("/pokemon?limit=2&offset=0")

    # Verifica o status e a mensagem de erro
    assert response.status_code == 500
    assert response.json() == {"detail": "Erro ao buscar lista de Pokemon: Erro interno"}