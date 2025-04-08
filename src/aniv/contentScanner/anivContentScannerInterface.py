from abc import ABC, abstractmethod

from ..models.anivContentCode import AnivContentCode


class AnivContentScannerInterface(ABC):

    @abstractmethod
    async def scan(self, message: str | None) -> AnivContentCode:
        pass
