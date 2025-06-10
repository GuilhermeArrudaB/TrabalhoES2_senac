from app.core.factories.abc_factory import APIServiceFactory
import asyncio
from typing import List, Dict, Any, Optional

class EntityRepository:
    def __init__(self, factory: APIServiceFactory):
        self.factory = factory

    async def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        try:
            return await self.factory.get_entity(entity_id)
        except Exception:
            return None

    async def get_entity_list(self, limit: int, offset: int) -> List[Dict[str, Any]]:
        return await self.factory.get_entity_list(limit, offset)

    async def execute_concurrently(self, tasks: List) -> List[Dict[str, Any]]:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [result for result in results if not isinstance(result, Exception)]