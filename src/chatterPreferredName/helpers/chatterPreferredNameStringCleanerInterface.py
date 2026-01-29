from abc import ABC, abstractmethod
from typing import Any


class ChatterPreferredNameStringCleanerInterface(ABC):

    @abstractmethod
    async def clean(
        self,
        preferredName: str | Any | None,
    ) -> str | None:
        pass
