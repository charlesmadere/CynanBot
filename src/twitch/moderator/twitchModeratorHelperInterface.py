from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class TwitchModeratorHelperInterface(Clearable, ABC):

    @abstractmethod
    async def isModerator(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> bool:
        pass
