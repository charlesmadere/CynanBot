from dataclasses import dataclass

@dataclass(frozen = True)
class TtsChatter:
    chatterUserId: str
    twitchChannelId: str
