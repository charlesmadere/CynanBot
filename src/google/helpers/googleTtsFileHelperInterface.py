from abc import ABC, abstractmethod


class GoogleTtsFileHelperInterface(ABC):

    @abstractmethod
    async def writeBase64CommandToNewFile(self, base64Command: str) -> str | None:
        pass
