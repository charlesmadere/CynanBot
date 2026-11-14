from abc import ABC, abstractmethod
from typing import AbstractSet, Any, MutableSequence, Sequence, TypeVar, ValuesView

T = TypeVar('T')


class RandomUtilsInterface(ABC):

    @abstractmethod
    def bool(self) -> bool:
        pass

    @abstractmethod
    def choice(self, collection: AbstractSet[T] | Sequence[T] | ValuesView[T]) -> T:
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
