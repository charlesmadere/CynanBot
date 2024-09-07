from dataclasses import dataclass
from datetime import datetime
from typing import Collection

from ..models.ttsMonsterVoice import TtsMonsterVoice


@dataclass(frozen = True)
class TtsMonsterStreamerVoicesCache:
    voices: Collection[TtsMonsterVoice]
    expirationDateTime: datetime
    twitchChannelId: str
