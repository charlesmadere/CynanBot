from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.tts.ttsRaidInfo import TtsRaidInfo


class TtsEvent():

    def __init__(
        self,
        message: str | None,
        twitchChannel: str,
        userId: str,
        userName: str,
        donation: TtsDonation | None,
        provider: TtsProvider,
        raidInfo: TtsRaidInfo | None
    ):
        if message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise TypeError(f'userName argument is malformed: \"{userName}\"')
        elif donation is not None and not isinstance(donation, TtsDonation):
            raise TypeError(f'donation argument is malformed: \"{donation}\"')
        elif not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')
        elif raidInfo is not None and not isinstance(raidInfo, TtsRaidInfo):
            raise TypeError(f'raidInfo argument is malformed: \"{raidInfo}\"')

        self.__message: str | None = message
        self.__twitchChannel: str = twitchChannel
        self.__userId: str = userId
        self.__userName: str = userName
        self.__donation: TtsDonation | None = donation
        self.__provider: TtsProvider = provider
        self.__raidInfo: TtsRaidInfo | None = raidInfo

    def getDonation(self) -> TtsDonation | None:
        return self.__donation

    def getMessage(self) -> str | None:
        return self.__message

    def getProvider(self) -> TtsProvider:
        return self.__provider

    def getRaidInfo(self) -> TtsRaidInfo | None:
        return self.__raidInfo

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel

    def getUserId(self) -> str:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'donation': self.__donation,
            'message': self.__message,
            'provider': self.__provider,
            'raidInfo': self.__raidInfo,
            'twitchChannel': self.__twitchChannel,
            'userId': self.__userId,
            'userName': self.__userName
        }
