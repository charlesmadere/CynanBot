from abc import ABC, abstractmethod
from typing import Any, MutableSequence


class RandomUtilsInterface(ABC):

    @abstractmethod
    def bool(self) -> bool:
        pass

    @abstractmethod
    def float(self) -> float:
        pass

    @abstractmethod
    def int(self, low: int, high: int) -> int:
        pass

    @abstractmethod
    def shuffle(self, collection: MutableSequence[Any]):
        pass

    @abstractmethod
    def uuid(self) -> str:
        pass
