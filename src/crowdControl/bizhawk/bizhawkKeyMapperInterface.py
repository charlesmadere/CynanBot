from abc import ABC, abstractmethod
from typing import Any

from .bizhawkKey import BizhawkKey


class BizhawkKeyMapperInterface(ABC):

    @abstractmethod
    async def fromString(self, string: str | Any | None) -> BizhawkKey | None:
        pass
