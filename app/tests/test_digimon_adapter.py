import pytest
from app.core.adapters.digimon_adapter import DigimonAdapter

# Dados de exemplo
mock_digimon_data = {
    "name": "Agumon",
    "img": "https://digimon-api.vercel.app/images/agumon.jpg",
    "level": "Rookie"
}

expected_adapted_data = {
    "id": None,
    "name": "Agumon",
    "types": [{"slot": 1, "type": {"name": "Rookie", "url": ""}}],
    "abilities": [],
    "height": None,
    "weight": None
}

@pytest.mark.asyncio
async def test_digimon_adapter_success():
    adapter = DigimonAdapter()
    result = adapter.adapt(mock_digimon_data)
    assert result == expected_adapted_data
    assert result["name"] == "Agumon"
    assert result["types"][0]["type"]["name"] == "Rookie"

@pytest.mark.asyncio
async def test_digimon_adapter_none_input():
    adapter = DigimonAdapter()
    result = adapter.adapt(None)
    assert result is None