from dataclasses import dataclass

from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.tts.ttsRaidInfo import TtsRaidInfo


@dataclass(frozen = True)
class TtsEvent():
    message: str | None
    twitchChannel: str
    twitchChannelId: str
    userId: str
    userName: str
    donation: TtsDonation | None
    provider: TtsProvider
    raidInfo: TtsRaidInfo | None
