from typing import Dict, Any, Optional

class DigimonAdapter:
    def adapt(self, digimon_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not digimon_data:
            return None
        return {
            "id": None,  # Digimon API não fornece ID
            "name": digimon_data.get("name"),
            "types": [{"slot": 1, "type": {"name": digimon_data.get("level"), "url": ""}}],
            "abilities": [],  # Digimon API não fornece habilidades
            "height": None,
            "weight": None
        }
