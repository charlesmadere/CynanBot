from abc import ABC, abstractmethod


class GuaranteedTimeoutUsersRepositoryInterface(ABC):

    @abstractmethod
    async def isGuaranteed(self, userId: str) -> bool:
        pass
