import pytest
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, patch
from app.models.digimon_model import Digimon

client = TestClient(app)

mock_digimon_data = {
    "name": "Agumon",
    "img": "https://digimon-api.vercel.app/images/agumon.jpg",
    "level": "Rookie"
}

mock_digimon_list_data = [
    {"name": "Agumon", "url": "https://digimon-api.vercel.app/api/digimon/name/agumon"},
    {"name": "Gabumon", "url": "https://digimon-api.vercel.app/api/digimon/name/gabumon"}
]


@pytest.mark.asyncio
async def test_get_digimon_success(mocker):
    mocker.patch(
        "app.core.factories.digimon_factory.DigimonAPIFactory.get_entity",
        AsyncMock(return_value=mock_digimon_data)
    )

    response = client.get("/digimon/agumon")

    assert response.status_code == 200
    assert response.json() == mock_digimon_data
    assert response.json()["name"] == "Agumon"
    assert response.json()["level"] == "Rookie"


@pytest.mark.asyncio
async def test_get_digimon_not_found(mocker):
    mocker.patch(
        "app.core.factories.digimon_factory.DigimonAPIFactory.get_entity",
        AsyncMock(return_value=None)
    )

    response = client.get("/digimon/unknown")

    assert response.status_code == 404
    assert response.json() == {"detail": "Digimon não encontrado"}


@pytest.mark.asyncio
async def test_get_digimon_list_success(mocker):
    mocker.patch(
        "app.core.factories.digimon_factory.DigimonAPIFactory.get_entity_list",
        AsyncMock(return_value=mock_digimon_list_data)
    )
    mocker.patch(
        "app.core.factories.digimon_factory.DigimonAPIFactory.get_entity",
        AsyncMock(side_effect=[mock_digimon_data, mock_digimon_data])
    )

    response = client.get("/digimon?limit=2&offset=0")

    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "Agumon"
    assert response.json()[0]["level"] == "Rookie"


@pytest.mark.asyncio
async def test_get_digimon_list_internal_error(mocker):
    mocker.patch(
        "app.core.factories.digimon_factory.DigimonAPIFactory.get_entity_list",
        AsyncMock(side_effect=Exception("Erro interno"))
    )

    response = client.get("/digimon?limit=2&offset=0")

    assert response.status_code == 500
    assert response.json() == {"detail": "Erro ao buscar lista de Digimon: Erro interno"}
