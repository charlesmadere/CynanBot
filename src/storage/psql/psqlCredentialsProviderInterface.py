from abc import ABC, abstractmethod

from ...misc.clearable import Clearable


class PsqlCredentialsProviderInterface(Clearable, ABC):

    @abstractmethod
    async def getHost(self) -> str | None:
        pass

    @abstractmethod
    async def getPassword(self) -> str | None:
        pass

    @abstractmethod
    async def getPort(self) -> int | None:
        pass

    @abstractmethod
    async def requireDatabaseName(self) -> str:
        pass

    @abstractmethod
    async def requireMaxConnections(self) -> int:
        pass

    @abstractmethod
    async def requireUser(self) -> str:
        pass
