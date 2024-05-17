from dataclasses import dataclass

from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.tts.ttsEvent import TtsEvent


@dataclass(frozen = True)
class StreamAlert():
    soundAlert: SoundAlert | None
    twitchChannel: str
    twitchChannelId: str
    ttsEvent: TtsEvent | None
