from dataclasses import dataclass

from .twitchOutcomeColor import TwitchOutcomeColor
from .twitchOutcomePredictor import TwitchOutcomePredictor


@dataclass(frozen = True)
class TwitchOutcome():
    channelPoints: int
    users: int
    outcomeId: str
    title: str
    color: TwitchOutcomeColor
    topPredictors: list[TwitchOutcomePredictor] | None = None
