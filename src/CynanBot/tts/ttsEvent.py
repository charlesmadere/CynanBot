from typing import Any, Dict, Optional

import misc.utils as utils
from tts.ttsDonation import TtsDonation
from tts.ttsRaidInfo import TtsRaidInfo


class TtsEvent():

    def __init__(
        self,
        message: Optional[str],
        twitchChannel: str,
        userId: str,
        userName: str,
        donation: Optional[TtsDonation],
        raidInfo: Optional[TtsRaidInfo]
    ):
        if message is not None and not isinstance(message, str):
            raise ValueError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif donation is not None and not isinstance(donation, TtsDonation):
            raise ValueError(f'donation argument is malformed: \"{donation}\"')
        elif raidInfo is not None and not isinstance(raidInfo, TtsRaidInfo):
            raise ValueError(f'raidInfo argument is malformed: \"{raidInfo}\"')

        self.__message: Optional[str] = message
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId
        self.__userName: str = userName
        self.__donation: Optional[TtsDonation] = donation
        self.__raidInfo: Optional[TtsRaidInfo] = raidInfo

    def getDonation(self) -> Optional[TtsDonation]:
        return self.__donation

    def getMessage(self) -> Optional[str]:
        return self.__message

    def getRaidInfo(self) -> Optional[TtsRaidInfo]:
        return self.__raidInfo

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __repr__(self) -> str:
        dictionary: Dict[str, Any] = {
            'message': self.__message,
            'twitchChannel': self.__twitchChannel,
            'userId': self.__userId,
            'userName': self.__userName
        }

        if self.__donation is not None:
            dictionary['donation'] = self.__donation.toDictionary()

        if self.__raidInfo is not None:
            dictionary['raidInfo'] = self.__raidInfo.toDictionary()

        return f'{dictionary}'
