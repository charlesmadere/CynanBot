from abc import ABC, abstractmethod


class EditCheerActionResult(ABC):

    @abstractmethod
    def getBits(self) -> int:
        pass

    @abstractmethod
    def getTwitchChannelId(self) -> str:
        pass
