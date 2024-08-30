from abc import ABC, abstractmethod
from typing import Any

from .pkmnCatchType import PkmnCatchType


class PkmnCatchTypeJsonMapperInterface(ABC):

    @abstractmethod
    def parse(self, catchType: str | Any | None) -> PkmnCatchType | None:
        pass

    @abstractmethod
    def require(self, catchType: str | Any | None) -> PkmnCatchType:
        pass
