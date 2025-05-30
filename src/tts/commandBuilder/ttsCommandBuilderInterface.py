from abc import ABC, abstractmethod

from ..models.ttsEvent import TtsEvent


class TtsCommandBuilderInterface(ABC):

    @abstractmethod
    async def buildDonationPrefix(self, event: TtsEvent | None) -> str | None:
        pass
