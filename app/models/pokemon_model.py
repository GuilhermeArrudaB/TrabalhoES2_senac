from pydantic import BaseModel
from typing import List, Dict

class Ability(BaseModel):
    name: str
    url: str

class PokemonAbility(BaseModel):
    ability: Ability
    is_hidden: bool
    slot: int

class Type(BaseModel):
    name: str
    url: str

class PokemonType(BaseModel):
    slot: int
    type: Type

class Pokemon(BaseModel):
    id: int
    name: str
    abilities: List[PokemonAbility]
    types: List[PokemonType]
    height: int
    weight: int