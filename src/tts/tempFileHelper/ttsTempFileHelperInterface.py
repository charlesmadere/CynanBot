from abc import ABC, abstractmethod
from typing import Collection


class TtsTempFileHelperInterface(ABC):

    @abstractmethod
    async def deleteOldTempFiles(self):
        pass

    @abstractmethod
    async def registerTempFile(self, fileName: str | None):
        pass

    @abstractmethod
    async def registerTempFiles(self, fileNames: Collection[str]):
        pass
