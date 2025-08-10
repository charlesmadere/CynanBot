from abc import ABC, abstractmethod

from frozendict import frozendict

from ..models.mostRecentAnivMessage import MostRecentAnivMessage
from ..models.whichAnivUser import WhichAnivUser
from ...misc.clearable import Clearable


class MostRecentAnivMessageRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        twitchChannelId: str,
    ) -> frozendict[WhichAnivUser, MostRecentAnivMessage | None]:
        pass

    @abstractmethod
    async def set(
        self,
        message: str | None,
        twitchChannelId: str,
        whichAnivUser: WhichAnivUser,
    ):
        pass
