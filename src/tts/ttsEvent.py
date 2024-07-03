from dataclasses import dataclass

from .ttsDonation import TtsDonation
from .ttsProvider import TtsProvider
from .ttsRaidInfo import TtsRaidInfo


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
