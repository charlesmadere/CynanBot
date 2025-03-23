from abc import ABC, abstractmethod
from typing import Any

from ..models.anivUser import AnivUser


class AnivUserParserInterface(ABC):

    @abstractmethod
    async def parse(
        self,
        string: str | Any | None
    ) -> AnivUser | None:
        pass

    @abstractmethod
    async def require(
        self,
        string: str | Any | None
    ) -> AnivUser:
        pass

    @abstractmethod
    async def serialize(
        self,
        anivUser: AnivUser
    ) -> str:
        pass
