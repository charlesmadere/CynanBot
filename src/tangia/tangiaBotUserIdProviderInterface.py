from abc import ABC, abstractmethod


class TangiaBotUserIdProviderInterface(ABC):

    @abstractmethod
    async def getTangiaBotUserId(self) -> str | None:
        pass
