from abc import ABC, abstractmethod


class DecTalkFileManagerInterface(ABC):

    @abstractmethod
    async def generateNewSpeechFile(self) -> str:
        pass
