from typing import Iterator, Optional
from app.core.facades.entity_facade import EntityFacade
from app.models.digimon_model import Digimon


class DigimonIterator:
    def __init__(self, facade: EntityFacade, limit: int = 20):
        self.facade = facade
        self.limit = limit
        self.offset = 0
        self.current_page: list[Digimon] = []
        self.current_index = 0

    def __aiter__(self) -> Iterator[Digimon]:
        return self

    async def __anext__(self) -> Digimon:
        # Se chegou ao fim da página atual, busca a próxima
        if self.current_index >= len(self.current_page):
            self.current_page = await self.facade.get_entity_list(self.limit, self.offset)
            self.offset += self.limit
            self.current_index = 0
            if not self.current_page:  # Se não há mais dados
                raise StopAsyncIteration

        # Retorna o próximo Digimon
        digimon = self.current_page[self.current_index]
        self.current_index += 1
        return digimon