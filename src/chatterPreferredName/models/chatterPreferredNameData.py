from dataclasses import dataclass


@dataclass(frozen = True)
class ChatterPreferredNameData:
    chatterUserId: str
    preferredName: str
    twitchChannelId: str
