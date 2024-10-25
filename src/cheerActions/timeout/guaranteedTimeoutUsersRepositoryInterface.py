from abc import ABC, abstractmethod


class GuaranteedTimeoutUsersRepositoryInterface(ABC):

    @abstractmethod
    async def getUserIds(self) -> frozenset[str]:
        pass
