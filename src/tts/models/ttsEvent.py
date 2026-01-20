from dataclasses import dataclass

from .ttsDonation import TtsDonation
from .ttsProvider import TtsProvider
from .ttsProviderOverridableStatus import TtsProviderOverridableStatus
from .ttsRaidInfo import TtsRaidInfo


@dataclass(frozen = True, slots = True)
class TtsEvent:
    message: str | None
    twitchChannel: str
    twitchChannelId: str
    userId: str
    userName: str
    donation: TtsDonation | None
    provider: TtsProvider
    providerOverridableStatus: TtsProviderOverridableStatus
    raidInfo: TtsRaidInfo | None
