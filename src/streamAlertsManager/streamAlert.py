from dataclasses import dataclass

from ..soundPlayerManager.soundAlert import SoundAlert
from ..tts.models.ttsEvent import TtsEvent


@dataclass(frozen = True, slots = True)
class StreamAlert:
    soundAlert: SoundAlert | None
    twitchChannel: str
    twitchChannelId: str
    ttsEvent: TtsEvent | None
