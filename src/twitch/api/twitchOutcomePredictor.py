import locale
from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchOutcomePredictor:
    channelPointsUsed: int
    channelPointsWon: int | None
    userId: str
    userLogin: str
    userName: str

    @property
    def channelPointsWonStr(self) -> str:
        channelPointsWon = self.requireChannelPointsWon()
        return locale.format_string("%d", channelPointsWon, grouping = True)

    def requireChannelPointsWon(self) -> int:
        if self.channelPointsWon is None:
            raise ValueError(f'channelPointsWon has not been set: \"{self}\"')

        return self.channelPointsWon
