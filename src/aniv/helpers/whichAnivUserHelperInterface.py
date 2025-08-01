from abc import ABC, abstractmethod
from dataclasses import dataclass

from frozendict import frozendict

from ...users.aniv.whichAnivUser import WhichAnivUser


class WhichAnivUserHelperInterface(ABC):

    @dataclass(frozen = True)
    class Result:
        userId: str
        userName: str
        whichAnivUser: WhichAnivUser

    @abstractmethod
    async def getAllAnivUserIds(self) -> frozendict[WhichAnivUser, str | None]:
        pass

    @abstractmethod
    async def getAnivUser(
        self,
        twitchChannelId: str,
        whichAnivUser: WhichAnivUser | None,
    ) -> Result | None:
        pass
