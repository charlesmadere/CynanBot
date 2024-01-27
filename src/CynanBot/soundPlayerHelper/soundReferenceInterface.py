from abc import ABC, abstractmethod


class SoundReferenceInterface(ABC):

    @abstractmethod
    async def getDurationMillis(self) -> int:
        pass

    @abstractmethod
    async def play(self):
        pass
