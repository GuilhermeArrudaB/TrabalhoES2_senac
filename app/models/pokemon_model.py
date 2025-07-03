from pydantic import BaseModel
from typing import List, Optional

class Type(BaseModel):
    name: str
    url: str

class PokemonType(BaseModel):
    slot: int
    type: Type

class Ability(BaseModel):
    name: str
    url: str

class PokemonAbility(BaseModel):
    ability: Ability
    is_hidden: bool
    slot: int

class Stat(BaseModel):
    name: str
    url: str

class PokemonStat(BaseModel):
    base_stat: int
    effort: int
    stat: Stat

class Pokemon(BaseModel):
    id: Optional[int]
    name: str
    abilities: List[PokemonAbility]
    types: List[PokemonType]
    height: Optional[int]
    weight: Optional[int]
    stats: Optional[List[PokemonStat]] = None  # Novo campo para stats