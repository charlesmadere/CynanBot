from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


class TwitchCommunitySubGift():

    def __init__(
        self,
        cumulativeTotal: int | None,
        total: int,
        communitySubGiftId: str,
        subTier: TwitchSubscriberTier
    ):
        if cumulativeTotal is not None and not utils.isValidInt(cumulativeTotal):
            raise TypeError(f'cumulativeTotal argument is malformed: \"{cumulativeTotal}\"')
        elif cumulativeTotal is not None and (cumulativeTotal < 0 or cumulativeTotal > utils.getLongMaxSafeSize()):
            raise ValueError(f'cumulativeTotal argument is out of bounds: {cumulativeTotal}')
        elif not utils.isValidInt(total):
            raise TypeError(f'total argument is malformed: \"{total}\"')
        elif total < 0 or total > utils.getLongMaxSafeSize():
            raise ValueError(f'total argument is out of bounds: {total}')
        elif not utils.isValidStr(communitySubGiftId):
            raise TypeError(f'communitySubGiftId argument is malformed: \"{communitySubGiftId}\"')
        elif not isinstance(subTier, TwitchSubscriberTier):
            raise TypeError(f'subTier argument is malformed: \"{subTier}\"')

        self.__cumulativeTotal: int | None = cumulativeTotal
        self.__total: int = total
        self.__communitySubGiftId: str = communitySubGiftId
        self.__subTier: TwitchSubscriberTier = subTier

    def getCommunitySubGiftId(self) -> str:
        return self.__communitySubGiftId

    def getCumulativeTotal(self) -> int | None:
        return self.__cumulativeTotal

    def getSubTier(self) -> TwitchSubscriberTier:
        return self.__subTier

    def getTotal(self) -> int:
        return self.__total

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'communitySubGiftId': self.__communitySubGiftId,
            'cumulativeTotal': self.__cumulativeTotal,
            'subTier': self.__subTier,
            'total': self.__total
        }
