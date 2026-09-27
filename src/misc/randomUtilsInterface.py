from abc import ABC, abstractmethod


class RandomUtilsInterface(ABC):

    @abstractmethod
    def bool(self) -> bool:
        pass

    @abstractmethod
    def float(self) -> float:
        pass

    @abstractmethod
    def uuid(self) -> str:
        pass
