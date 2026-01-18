import locale
from dataclasses import dataclass

from ...localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True)
class TwitchOutcomePredictor(TwitchUserInterface):
    channelPointsUsed: int
    channelPointsWon: int | None
    userId: str
    userLogin: str
    userName: str

    @property
    def channelPointsWonStr(self) -> str:
        channelPointsWon = self.requireChannelPointsWon()
        return locale.format_string("%d", channelPointsWon, grouping = True)

    def getUserId(self) -> str:
        return self.userId

    def getUserLogin(self) -> str:
        return self.userLogin

    def getUserName(self) -> str:
        return self.userName

    def requireChannelPointsWon(self) -> int:
        if self.channelPointsWon is None:
            raise ValueError(f'channelPointsWon has not been set: \"{self}\"')

        return self.channelPointsWon
