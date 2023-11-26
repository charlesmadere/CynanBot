from abc import ABC, abstractmethod
from typing import List, Optional


class LinesReaderInterface(ABC):

    @abstractmethod
    def readLines(self) -> Optional[List[str]]:
        pass

    @abstractmethod
    async def readLinesAsync(self) -> Optional[List[str]]:
        pass
