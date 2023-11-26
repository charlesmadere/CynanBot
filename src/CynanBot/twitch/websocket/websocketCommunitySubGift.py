from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.twitchSubscriberTier import TwitchSubscriberTier


class WebsocketCommunitySubGift():

    def __init__(
        self,
        cumulativeTotal: Optional[int],
        total: int,
        communitySubGiftId: str,
        subTier: TwitchSubscriberTier
    ):
        if cumulativeTotal is not None and not utils.isValidInt(cumulativeTotal):
            raise ValueError(f'cumulativeTotal argument is malformed: \"{cumulativeTotal}\"')
        elif not utils.isValidInt(total):
            raise ValueError(f'total argument is malformed: \"{total}\"')
        elif not utils.isValidStr(communitySubGiftId):
            raise ValueError(f'communitySubGiftId argument is malformed: \"{communitySubGiftId}\"')
        elif not isinstance(subTier, TwitchSubscriberTier):
            raise ValueError(f'subTier argument is malformed: \"{subTier}\"')

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
