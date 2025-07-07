from abc import ABC, abstractmethod
from dataclasses import dataclass

from ...users.aniv.whichAnivUser import WhichAnivUser


class WhichAnivUserHelperInterface(ABC):

    @dataclass(frozen = True)
    class Result:
        userId: str
        userName: str
        whichAnivUser: WhichAnivUser

    @abstractmethod
    async def getAnivUser(
        self,
        twitchChannelId: str,
        whichAnivUser: WhichAnivUser | None,
    ) -> Result | None:
        pass
