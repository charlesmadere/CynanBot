from abc import ABC, abstractmethod


class StreamElementsFileManagerInterface(ABC):

    @abstractmethod
    async def saveSpeechToNewFile(self, speechBytes: bytes) -> str | None:
        pass
