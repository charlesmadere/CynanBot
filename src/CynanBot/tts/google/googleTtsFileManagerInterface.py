from abc import ABC, abstractmethod


class GoogleTtsFileManagerInterface(ABC):

    @abstractmethod
    async def writeBase64CommandToNewFile(self, base64Command: str) -> str | None:
        pass
