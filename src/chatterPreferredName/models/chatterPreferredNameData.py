from dataclasses import dataclass


@dataclass(frozen = True, slots = True)
class ChatterPreferredNameData:
    chatterUserId: str
    preferredName: str
    twitchChannelId: str
