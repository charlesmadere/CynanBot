from dataclasses import dataclass

from .cutenessResult import CutenessResult
from ..cutenessDate import CutenessDate
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class PreparedCutenessResult(TwitchUserInterface):
    cutenessResult: CutenessResult
    userLogin: str
    userName: str

    @property
    def cutenessDate(self) -> CutenessDate:
        return self.cutenessResult.cutenessDate

    @property
    def cutenessStr(self) -> str:
        return self.cutenessResult.cutenessStr

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName

    def requireCuteness(self) -> int:
        return self.cutenessResult.requireCuteness()

    @property
    def twitchChannelId(self) -> str:
        return self.cutenessResult.twitchChannelId

    @property
    def userId(self) -> str:
        return self.cutenessResult.userId
