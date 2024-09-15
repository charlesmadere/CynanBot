from dataclasses import dataclass


@dataclass(frozen = True)
class TtsMonsterKeyAndUserId:
    key: str
    twitchChannel: str
    userId: str
