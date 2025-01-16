from abc import ABC, abstractmethod


class DecTalkHelperInterface(ABC):

    @abstractmethod
    async def getSpeech(
        self,
        message: str | None
    ) -> str | None:
        pass
