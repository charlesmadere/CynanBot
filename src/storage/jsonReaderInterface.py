from abc import ABC, abstractmethod
from typing import Any


class JsonReaderInterface(ABC):

    @abstractmethod
    def deleteFile(self):
        pass

    @abstractmethod
    async def deleteFileAsync(self):
        pass

    @abstractmethod
    def fileExists(self) -> bool:
        pass

    @abstractmethod
    async def fileExistsAsync(self) -> bool:
        pass

    @abstractmethod
    def readJson(self) -> dict[Any, Any] | None:
        pass

    @abstractmethod
    async def readJsonAsync(self) -> dict[Any, Any] | None:
        pass
