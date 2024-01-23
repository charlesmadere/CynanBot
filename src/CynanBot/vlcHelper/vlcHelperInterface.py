from abc import ABC, abstractmethod


class VlcHelperInterface(ABC):

    @abstractmethod
    async def play(self, filePath: str):
        pass
