from dataclasses import dataclass


@dataclass(frozen = True)
class TwitchOutcomePredictor:
    channelPointsUsed: int
    channelPointsWon: int | None
    userId: str
    userLogin: str
    userName: str
