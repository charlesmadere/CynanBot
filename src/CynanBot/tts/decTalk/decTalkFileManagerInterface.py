from abc import ABC, abstractmethod
from typing import Optional


class DecTalkFileManagerInterface(ABC):

    @abstractmethod
    async def deleteFile(self, fileName: Optional[str]):
        pass

    @abstractmethod
    async def writeCommandToNewFile(self, command: str) -> Optional[str]:
        pass
