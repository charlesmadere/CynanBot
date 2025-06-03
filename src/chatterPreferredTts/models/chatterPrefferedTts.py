from dataclasses import dataclass

from .absTtsProperties import AbsTtsProperties


@dataclass(frozen = True)
class ChatterPreferredTts:
    properties: AbsTtsProperties
    chatterUserId: str
    twitchChannelId: str
