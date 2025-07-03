from pydantic import BaseModel
from typing import Optional, List

class Digimon(BaseModel):
    id: Optional[int]
    name: str
    img: Optional[str] = None
    level: Optional[str] = None