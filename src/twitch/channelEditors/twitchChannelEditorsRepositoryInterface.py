from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class TwitchChannelEditorsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def fetchEditorIds(
        self,
        twitchChannelId: str,
    ) -> frozenset[str]:
        pass

    @abstractmethod
    async def isEditor(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> bool:
        pass
