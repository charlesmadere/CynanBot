from dataclasses import dataclass

from .ttsDonation import TtsDonation
from .ttsDonationType import TtsDonationType
from ..twitch.api.models.twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TtsSubscriptionDonation(TtsDonation):
    isAnonymous: bool
    cumulativeMonths: int | None
    durationMonths: int | None
    numberOfGiftedSubs: int | None
    tier: TwitchSubscriberTier

    @property
    def donationType(self) -> TtsDonationType:
        return TtsDonationType.SUBSCRIPTION
