from dataclasses import dataclass

from ..soundPlayerManager.soundAlert import SoundAlert
from ..tts.ttsEvent import TtsEvent


@dataclass(frozen = True)
class StreamAlert():
    soundAlert: SoundAlert | None
    twitchChannel: str
    twitchChannelId: str
    ttsEvent: TtsEvent | None
