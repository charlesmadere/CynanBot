from dataclasses import dataclass

from .anivCopyMessageTimeoutScore import AnivCopyMessageTimeoutScore
from ...twitch.localModels.twitchUserInterface import TwitchUserInterface


@dataclass(frozen = True, slots = True)
class PreparedAnivCopyMessageTimeoutScore:
    score: AnivCopyMessageTimeoutScore
    twitchChannel: str
    chatterUserData: TwitchUserInterface

    @property
    def chatterUserId(self) -> str:
        return self.score.chatterUserId

    @property
    def dodgeScore(self) -> int:
        return self.score.dodgeScore

    @property
    def dodgeScoreStr(self) -> str:
        return self.score.dodgeScoreStr

    @property
    def timeoutScore(self) -> int:
        return self.score.timeoutScore

    @property
    def timeoutScoreStr(self) -> str:
        return self.score.timeoutScoreStr

    @property
    def twitchChannelId(self) -> str:
        return self.score.twitchChannelId
