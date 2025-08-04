from abc import ABC, abstractmethod


class SupStreamerHelperInterface(ABC):

    @abstractmethod
    async def isSupStreamerMessage(
        self,
        chatMessage: str | None,
        supStreamerMessage: str,
    ) -> bool:
        pass
