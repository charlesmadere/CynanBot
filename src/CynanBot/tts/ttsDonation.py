from abc import ABC, abstractmethod

from CynanBot.tts.ttsDonationType import TtsDonationType


class TtsDonation(ABC):

    @property
    @abstractmethod
    def donationType(self) -> TtsDonationType:
        pass
