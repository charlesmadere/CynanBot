from abc import ABC, abstractmethod


class TwitchHandleProviderInterface(ABC):

    @abstractmethod
    async def getTwitchHandle(self) -> str:
        pass
