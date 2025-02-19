from dataclasses import dataclass

from .absPreferredTts import AbsPreferredTts


@dataclass(frozen = True)
class ChatterPreferredTts:
    preferredTts: AbsPreferredTts
    chatterUserId: str
    twitchChannelId: str
