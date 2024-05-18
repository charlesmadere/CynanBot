from dataclasses import dataclass

from CynanBot.twitch.api.twitchOutcomeColor import TwitchOutcomeColor
from CynanBot.twitch.api.twitchOutcomePredictor import TwitchOutcomePredictor


@dataclass(frozen = True)
class TwitchOutcome():
    channelPoints: int
    users: int
    outcomeId: str
    title: str
    color: TwitchOutcomeColor
    topPredictors: list[TwitchOutcomePredictor] | None = None
