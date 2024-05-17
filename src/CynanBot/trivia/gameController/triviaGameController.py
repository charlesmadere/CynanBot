from dataclasses import dataclass


@dataclass(frozen = True)
class TriviaGameController():
    twitchChannel: str
    twitchChannelId: str
    userId: str
    userName: str
