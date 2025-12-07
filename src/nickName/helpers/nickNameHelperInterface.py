from abc import ABC, abstractmethod

from ..models.nickNameData import NickNameData


class NickNameHelperInterface(ABC):

    @abstractmethod
    async def get(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> NickNameData | None:
        pass
