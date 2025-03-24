from abc import ABC, abstractmethod

from ..misc.clearable import Clearable


class GuaranteedTimeoutUsersRepositoryInterface(Clearable, ABC):

    @abstractmethod
    async def getUserIds(self) -> frozenset[str]:
        pass

    @abstractmethod
    async def isGuaranteed(self, userId: str) -> bool:
        pass
