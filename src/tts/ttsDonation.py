from abc import ABC, abstractmethod

from .ttsDonationType import TtsDonationType


class TtsDonation(ABC):

    @property
    @abstractmethod
    def donationType(self) -> TtsDonationType:
        pass
