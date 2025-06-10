from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class APIServiceFactory(ABC):
    @abstractmethod
    async def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_entity_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        pass