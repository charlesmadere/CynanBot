from dataclasses import dataclass

from .ttsDonation import TtsDonation
from .ttsDonationType import TtsDonationType
from .ttsSubscriptionDonationGiftType import TtsSubscriptionDonationGiftType
from ..twitch.api.twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TtsSubscriptionDonation(TtsDonation):
    isAnonymous: bool
    cumulativeMonths: int | None
    durationMonths: int | None
    numberOfGiftedSubs: int | None
    subGiftGiverDisplayName: str | None
    giftType: TtsSubscriptionDonationGiftType | None
    tier: TwitchSubscriberTier

    @property
    def donationType(self) -> TtsDonationType:
        return TtsDonationType.SUBSCRIPTION
