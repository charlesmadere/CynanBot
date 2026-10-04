import locale
from dataclasses import dataclass

from ...cuteness.models.preparedIncrementedCutenessResult import PreparedIncrementedCutenessResult
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class ToxicTriviaPunishment(TwitchUserInterface):
    numberOfPunishments: int
    punishedByPoints: int
    cutenessResult: PreparedIncrementedCutenessResult

    def getUserId(self) -> str:
        return self.cutenessResult.getUserId()

    def getUserLogin(self) -> str:
        return self.cutenessResult.getUserLogin()

    def getUserName(self) -> str:
        return self.cutenessResult.getUserName()

    @property
    def numberOfPunishmentsStr(self) -> str:
        return locale.format_string("%d", self.numberOfPunishments, grouping = True)

    @property
    def punishedByPointsStr(self) -> str:
        return locale.format_string("%d", self.punishedByPoints, grouping = True)
