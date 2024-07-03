from abc import ABC, abstractmethod


class TtsTempFileHelperInterface(ABC):

    @abstractmethod
    async def deleteOldTempFiles(self):
        pass

    @abstractmethod
    async def registerTempFile(self, fileName: str | None):
        pass
