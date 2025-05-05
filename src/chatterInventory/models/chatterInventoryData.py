from dataclasses import dataclass


@dataclass(frozen = True)
class ChatterInventoryData:
    chatterUserId: str
    twitchChannelId: str
