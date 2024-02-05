from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchSubscriberTier import TwitchSubscriberTier


class TwitchSubGift():

    def __init__(
        self,
        cumulativeTotal: Optional[int],
        durationMonths: int,
        communityGiftId: Optional[str],
        recipientUserId: str,
        recipientUserLogin: str,
        recipientUserName: str,
        subTier: TwitchSubscriberTier
    ):
        if cumulativeTotal is not None and not utils.isValidInt(cumulativeTotal):
            raise TypeError(f'cumulativeTotal argument is malformed: \"{cumulativeTotal}\"')
        elif cumulativeTotal is not None and (cumulativeTotal < 1 or cumulativeTotal > utils.getIntMaxSafeSize()):
            raise TypeError(f'cumulativeTotal argument is out of bounds: {cumulativeTotal}')
        elif not utils.isValidInt(durationMonths):
            raise TypeError(f'durationMonths argument is malformed: \"{durationMonths}\"')
        elif durationMonths < 1 or durationMonths > utils.getIntMaxSafeSize():
            raise ValueError(f'durationMonths argument is out of boudns: {durationMonths}')
        elif communityGiftId is not None and not isinstance(communityGiftId, str):
            raise TypeError(f'communityGiftId argument is malformed: \"{communityGiftId}\"')
        elif not utils.isValidStr(recipientUserId):
            raise TypeError(f'recipientUserId argument is malformed: \"{recipientUserId}\"')
        elif not utils.isValidStr(recipientUserLogin):
            raise TypeError(f'recipientUserLogin argument is malformed: \"{recipientUserLogin}\"')
        elif not utils.isValidStr(recipientUserName):
            raise TypeError(f'recipientUserName argument is malformed: \"{recipientUserName}\"')
        elif not isinstance(subTier, TwitchSubscriberTier):
            raise TypeError(f'subTier argument is malformed: \"{subTier}\"')

        self.__cumulativeTotal: Optional[int] = cumulativeTotal
        self.__durationMonths: int = durationMonths
        self.__communityGiftId: Optional[str] = communityGiftId
        self.__recipientUserId: str = recipientUserId
        self.__recipientUserLogin: str = recipientUserLogin
        self.__recipientUserName: str = recipientUserName
        self.__subTier: TwitchSubscriberTier = subTier

    def getCommunityGiftId(self) -> Optional[str]:
        return self.__communityGiftId

    def getCumulativeTotal(self) -> Optional[int]:
        return self.__cumulativeTotal

    def getDurationMonths(self) -> int:
        return self.__durationMonths

    def getRecipientUserId(self) -> str:
        return self.__recipientUserId

    def getRecipientUserLogin(self) -> str:
        return self.__recipientUserLogin

    def getRecipientUserName(self) -> str:
        return self.__recipientUserName

    def getSubTier(self) -> TwitchSubscriberTier:
        return self.__subTier

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'communityGiftId': self.__communityGiftId,
            'cumulativeTotal': self.__cumulativeTotal,
            'durationMonths': self.__durationMonths,
            'recipientUserId': self.__recipientUserId,
            'recipientUserLogin': self.__recipientUserLogin,
            'recipientUserName': self.__recipientUserName,
            'subTier': self.__subTier
        }
