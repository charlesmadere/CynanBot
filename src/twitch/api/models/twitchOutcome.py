from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchOutcomeColor import TwitchOutcomeColor
from .twitchOutcomePredictor import TwitchOutcomePredictor


@dataclass(frozen = True)
class TwitchOutcome:
    topPredictors: FrozenList[TwitchOutcomePredictor] | None
    channelPoints: int
    users: int
    outcomeId: str
    title: str
    color: TwitchOutcomeColor
