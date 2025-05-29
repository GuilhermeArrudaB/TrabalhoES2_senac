from pydantic import BaseModel
from typing import Optional

class Digimon(BaseModel):
    name: str
    img: str
    level: str