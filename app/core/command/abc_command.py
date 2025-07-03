from abc import ABC, abstractmethod
from typing import Any, Optional

class Command(ABC):
    @abstractmethod
    async def execute(self) -> Any:
        pass