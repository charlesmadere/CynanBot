from abc import ABC, abstractmethod


class MicrosoftSamHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        message: str | None
    ) -> bytes | None:
        pass
