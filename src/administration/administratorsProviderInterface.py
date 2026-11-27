from abc import ABC, abstractmethod
from typing import Collection

from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..misc.clearable import Clearable


class AdministratorsProviderInterface(
    AdministratorProviderInterface,
    Clearable,
    ABC,
):

    @abstractmethod
    async def getUserIds(self) -> Collection[str]:
        pass
