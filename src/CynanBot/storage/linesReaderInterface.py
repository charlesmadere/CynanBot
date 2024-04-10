from abc import ABC, abstractmethod


class LinesReaderInterface(ABC):

    @abstractmethod
    def readLines(self) -> list[str] | None:
        pass

    @abstractmethod
    async def readLinesAsync(self) -> list[str] | None:
        pass
