from typing import Collection

from .administratorsProviderInterface import AdministratorsProviderInterface


class AdministratorsProvider(AdministratorsProviderInterface):

    def clearCaches(self):
        # TODO
        pass

    async def getAdministratorUserId(self) -> str:
        # TODO
        return ''

    async def getAdministratorUserName(self) -> str:
        # TODO
        return ''

    async def getUserIds(self) -> Collection[str]:
        # TODO
        return frozenset()
