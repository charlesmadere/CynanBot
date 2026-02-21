from abc import ABC, abstractmethod


class MouseCursorHelperInterface(ABC):

    @abstractmethod
    async def applyMouseCursor(
        self,
        twitchChannel: str,
        twitchChannelId: str,
    ) -> bool:
        pass
