from dataclasses import dataclass


@dataclass(frozen = True)
class TtsMonsterKeyAndUserId:
    key: str
    twitchChannelId: str
    userId: str
