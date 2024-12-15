from abc import abstractmethod

from ...misc.clearable import Clearable


class TwitchChannelEditorsRepositoryInterface(Clearable):

    @abstractmethod
    async def isEditor(
        self,
        chatterUserId: str,
        twitchChannelId: str
    ) -> bool:
        pass
