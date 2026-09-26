from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class HardcodedTwitchChannelEditorsRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def get(self, twitchChannelId: str) -> frozenset[str]:
        pass
