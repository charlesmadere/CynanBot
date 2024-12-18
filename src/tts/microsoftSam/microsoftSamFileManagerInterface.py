from abc import ABC, abstractmethod


class MicrosoftSamFileManagerInterface(ABC):

    @abstractmethod
    async def saveSpeechToNewFile(self, speechBytes: bytes) -> str | None:
        pass
