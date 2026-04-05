from dataclasses import dataclass
from datetime import datetime

from .cutenessResult import CutenessResult
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class PreparedCutenessResult(TwitchUserInterface):
    cutenessResult: CutenessResult
    chatterUserLogin: str
    chatterUserName: str

    @property
    def chatterUserId(self) -> str:
        return self.cutenessResult.chatterUserId

    @property
    def cutenessDate(self) -> datetime:
        return self.cutenessResult.cutenessDate

    @property
    def cutenessStr(self) -> str:
        return self.cutenessResult.cutenessStr

    def getUserId(self) -> str:
        return self.chatterUserId

    def getUserLogin(self) -> str:
        return self.chatterUserLogin

    def getUserName(self) -> str:
        return self.chatterUserName

    def requireCuteness(self) -> int:
        return self.cutenessResult.requireCuteness()

    @property
    def twitchChannelId(self) -> str:
        return self.cutenessResult.twitchChannelId
