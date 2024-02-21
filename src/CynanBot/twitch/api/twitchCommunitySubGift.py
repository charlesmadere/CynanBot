from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


class TwitchCommunitySubGift():

    def __init__(
        self,
        cumulativeTotal: Optional[int],
        total: int,
        communitySubGiftId: str,
        subTier: TwitchSubscriberTier
    ):
        if cumulativeTotal is not None and not utils.isValidInt(cumulativeTotal):
            raise TypeError(f'cumulativeTotal argument is malformed: \"{cumulativeTotal}\"')
        if not utils.isValidInt(total):
            raise TypeError(f'total argument is malformed: \"{total}\"')
        if not utils.isValidStr(communitySubGiftId):
            raise TypeError(f'communitySubGiftId argument is malformed: \"{communitySubGiftId}\"')
        assert isinstance(subTier, TwitchSubscriberTier), f"malformed {subTier=}"

        self.__cumulativeTotal: Optional[int] = cumulativeTotal
        self.__total: int = total
        self.__communitySubGiftId: str = communitySubGiftId
        self.__subTier: TwitchSubscriberTier = subTier

    def getCommunitySubGiftId(self) -> str:
        return self.__communitySubGiftId

    def getCumulativeTotal(self) -> Optional[int]:
        return self.__cumulativeTotal

    def getSubTier(self) -> TwitchSubscriberTier:
        return self.__subTier

    def getTotal(self) -> int:
        return self.__total

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'communitySubGiftId': self.__communitySubGiftId,
            'cumulativeTotal': self.__cumulativeTotal,
            'subTier': self.__subTier,
            'total': self.__total
        }
