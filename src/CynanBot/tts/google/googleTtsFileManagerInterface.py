from abc import ABC, abstractmethod


class GoogleTtsFileManagerInterface(ABC):

    @abstractmethod
    async def deleteFile(self, fileName: str | None):
        pass

    @abstractmethod
    async def writeBase64CommandToNewFile(self, base64Command: str) -> str | None:
        pass
