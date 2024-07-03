from abc import ABC, abstractmethod


class DecTalkFileManagerInterface(ABC):

    @abstractmethod
    async def writeCommandToNewFile(self, command: str) -> str | None:
        pass
