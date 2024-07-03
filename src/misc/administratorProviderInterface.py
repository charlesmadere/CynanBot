from abc import abstractmethod

from .clearable import Clearable


class AdministratorProviderInterface(Clearable):

    @abstractmethod
    async def getAdministratorUserId(self) -> str:
        pass

    @abstractmethod
    async def getAdministratorUserName(self) -> str:
        pass
