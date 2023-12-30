from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.aniv.anivContentCode import AnivContentCode


class AnivContentScannerInterface(ABC):

    @abstractmethod
    async def scan(self, message: Optional[str]) -> AnivContentCode:
        pass
