from abc import ABC, abstractmethod

from ..models.mostRecentAnivMessage import MostRecentAnivMessage
from ...misc.clearable import Clearable


class MostRecentAnivMessageRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(
        self,
        twitchChannelId: str,
    ) -> MostRecentAnivMessage | None:
        pass

    @abstractmethod
    async def set(
        self,
        message: str | None,
        twitchChannelId: str,
    ):
        pass
