from abc import ABC, abstractmethod


class HardcodedTwitchChannelEditorsRepositoryInterface(ABC):

    @abstractmethod
    async def get(self, twitchChannelId: str) -> frozenset[str]:
        pass
