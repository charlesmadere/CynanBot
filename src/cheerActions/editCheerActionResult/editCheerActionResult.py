from abc import ABC, abstractmethod


class EditCheerActionResult(ABC):

    @property
    @abstractmethod
    def bits(self) -> int:
        pass

    @property
    @abstractmethod
    def twitchChannelId(self) -> str:
        pass
