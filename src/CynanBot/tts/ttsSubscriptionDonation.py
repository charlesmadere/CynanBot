from typing import Any, Dict

import CynanBot.misc.utils as utils
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsDonationType import TtsDonationType
from CynanBot.twitch.twitchSubscriberTier import TwitchSubscriberTier


class TtsSubscriptionDonation(TtsDonation):

    def __init__(
        self,
        isAnonymous: bool,
        isGift: bool,
        tier: TwitchSubscriberTier
    ):
        if not utils.isValidBool(isAnonymous):
            raise ValueError(f'isAnonymous argument is malformed: \"{isAnonymous}\"')
        elif not utils.isValidBool(isGift):
            raise ValueError(f'isGift argument is malformed: \"{isGift}\"')
        elif not isinstance(tier, TwitchSubscriberTier):
            raise ValueError(f'tier argument is malformed: \"{tier}\"')

        self.__isAnonymous: bool = isAnonymous
        self.__isGift: bool = isGift
        self.__tier: TwitchSubscriberTier = tier

    def getTier(self) -> TwitchSubscriberTier:
        return self.__tier

    def getType(self) -> TtsDonationType:
        return TtsDonationType.SUBSCRIPTION

    def isAnonymous(self) -> bool:
        return self.__isAnonymous

    def isGift(self) -> bool:
        return self.__isGift

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'isAnonymous': self.__isAnonymous,
            'isGift': self.__isGift,
            'tier': self.__tier,
            'type': self.getType()
        }
