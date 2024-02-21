from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsDonationType import TtsDonationType
from CynanBot.tts.ttsSubscriptionDonationGiftType import \
    TtsSubscriptionDonationGiftType
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


class TtsSubscriptionDonation(TtsDonation):

    def __init__(
        self,
        isAnonymous: bool,
        giftType: Optional[TtsSubscriptionDonationGiftType],
        tier: TwitchSubscriberTier
    ):
        if not utils.isValidBool(isAnonymous):
            raise TypeError(f'isAnonymous argument is malformed: \"{isAnonymous}\"')
        assert giftType is None or isinstance(giftType, TtsSubscriptionDonationGiftType), f"malformed {giftType=}"
        assert isinstance(tier, TwitchSubscriberTier), f"malformed {tier=}"

        self.__isAnonymous: bool = isAnonymous
        self.__giftType: Optional[TtsSubscriptionDonationGiftType] = giftType
        self.__tier: TwitchSubscriberTier = tier

    def getGiftType(self) -> Optional[TtsSubscriptionDonationGiftType]:
        return self.__giftType

    def getTier(self) -> TwitchSubscriberTier:
        return self.__tier

    def getType(self) -> TtsDonationType:
        return TtsDonationType.SUBSCRIPTION

    def isAnonymous(self) -> bool:
        return self.__isAnonymous

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'giftType': self.__giftType,
            'isAnonymous': self.__isAnonymous,
            'tier': self.__tier,
            'type': self.getType()
        }
