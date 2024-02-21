import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


class TwitchUserSubscriptionDetails():

    def __init__(
        self,
        isGift: bool,
        userId: str,
        userName: str,
        subscriberTier: TwitchSubscriberTier
    ):
        if not utils.isValidBool(isGift):
            raise ValueError(f'isGift argument is malformed: \"{isGift}\"')
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        assert isinstance(subscriberTier, TwitchSubscriberTier), f"malformed {subscriberTier=}"

        self.__isGift: bool = isGift
        self.__userId: str = userId
        self.__userName: str = userName
        self.__subscriberTier: TwitchSubscriberTier = subscriberTier

    def getSubscriberTier(self) -> TwitchSubscriberTier:
        return self.__subscriberTier

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def isGift(self) -> bool:
        return self.__isGift
