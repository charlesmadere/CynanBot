from dataclasses import dataclass
from datetime import datetime

from .cutenessEntry import CutenessEntry
from .incrementedCutenessResult import IncrementedCutenessResult
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class PreparedIncrementedCutenessResult(CutenessEntry, TwitchUserInterface):
    incrementedCutenessResult: IncrementedCutenessResult
    chatterUserLogin: str
    chatterUserName: str

    @property
    def chatterUserId(self) -> str:
        return self.incrementedCutenessResult.chatterUserId

    @property
    def cutenessDate(self) -> datetime:
        return self.incrementedCutenessResult.cutenessDate

    @property
    def cutenessStr(self) -> str:
        return self.incrementedCutenessResult.cutenessStr

    def getChatterUserId(self) -> str:
        return self.incrementedCutenessResult.getChatterUserId()

    def getCuteness(self) -> int:
        return self.incrementedCutenessResult.getCuteness()

    def getTwitchChannelId(self) -> str:
        return self.incrementedCutenessResult.getTwitchChannelId()

    def getUserId(self) -> str:
        return self.chatterUserId

    def getUserLogin(self) -> str:
        return self.chatterUserLogin

    def getUserName(self) -> str:
        return self.chatterUserName

    @property
    def previousCutenessStr(self) -> str:
        return self.incrementedCutenessResult.previousCutenessStr

    @property
    def twitchChannelId(self) -> str:
        return self.incrementedCutenessResult.twitchChannelId
