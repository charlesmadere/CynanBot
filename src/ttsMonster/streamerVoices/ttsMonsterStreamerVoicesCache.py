from dataclasses import dataclass
from datetime import datetime

from ..models.ttsMonsterVoice import TtsMonsterVoice


@dataclass(frozen = True)
class TtsMonsterStreamerVoicesCache:
    expirationDateTime: datetime
    voices: frozenset[TtsMonsterVoice]
    twitchChannelId: str
