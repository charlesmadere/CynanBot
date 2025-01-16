from abc import ABC, abstractmethod
from typing import Any


class GoogleTtsMessageCleanerInterface(ABC):

    @abstractmethod
    async def clean(self, message: str | Any | None) -> str | None:
        pass
