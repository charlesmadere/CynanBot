from dataclasses import dataclass

from frozenlist import FrozenList

from .twitchOutcomeColor import TwitchOutcomeColor
from .twitchOutcomePredictor import TwitchOutcomePredictor


@dataclass(frozen = True, slots = True)
class TwitchOutcome:
    topPredictors: FrozenList[TwitchOutcomePredictor]
    channelPoints: int
    users: int
    outcomeId: str
    title: str
    color: TwitchOutcomeColor
