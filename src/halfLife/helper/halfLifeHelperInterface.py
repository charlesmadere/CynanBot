from abc import ABC, abstractmethod


class HalfLifeHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        message: str | None
    ) -> list[str] | None:
        pass
