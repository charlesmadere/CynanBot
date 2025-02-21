from abc import ABC, abstractmethod

from .clearable import Clearable


class AdministratorProviderInterface(Clearable, ABC):

    @abstractmethod
    async def getAdministratorUserId(self) -> str:
        pass

    @abstractmethod
    async def getAdministratorUserName(self) -> str:
        pass
