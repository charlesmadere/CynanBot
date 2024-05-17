from dataclasses import dataclass

from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsDonationType import TtsDonationType
from CynanBot.tts.ttsSubscriptionDonationGiftType import \
    TtsSubscriptionDonationGiftType
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


@dataclass(frozen = True)
class TtsSubscriptionDonation(TtsDonation):
    isAnonymous: bool
    giftType: TtsSubscriptionDonationGiftType | None
    tier: TwitchSubscriberTier

    @property
    def donationType(self) -> TtsDonationType:
        return TtsDonationType.SUBSCRIPTION
