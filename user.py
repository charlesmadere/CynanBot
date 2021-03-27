import os
import urllib
from datetime import tzinfo
from typing import List

import CynanBotCommon.utils as utils


class User:

    def __init__(
        self,
        isAnalogueEnabled: bool,
        isCatJamEnabled: bool,
        isCutenessEnabled: bool,
        isDiccionarioEnabled: bool,
        isGiveCutenessEnabled: bool,
        isJishoEnabled: bool,
        isJokesEnabled: bool,
        isPicOfTheDayEnabled: bool,
        isPkmnEnabled: bool,
        isPokepediaEnabled: bool,
        isRaidLinkMessagingEnabled: bool,
        isRatJamEnabled: bool,
        isTamalesEnabled: bool,
        isTriviaEnabled: bool,
        isWeatherEnabled: bool,
        isWordOfTheDayEnabled: bool,
        discord: str,
        handle: str,
        increaseCutenessDoubleRewardId: str,
        increaseCutenessRewardId: str,
        locationId: str,
        picOfTheDayFile: str,
        picOfTheDayRewardId: str,
        pkmnBattleRewardId: str,
        pkmnCatchRewardId: str,
        pkmnEvolveRewardId: str,
        pkmnShinyRewardId: str,
        speedrunProfile: str,
        twitter: str,
        timeZones: List[tzinfo]
    ):
        if not utils.isValidStr(handle):
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif isPicOfTheDayEnabled and not utils.isValidStr(picOfTheDayFile):
            raise ValueError(f'picOfTheDayFile argument is malformed: \"{picOfTheDayFile}\"')

        self.__isAnalogueEnabled = isAnalogueEnabled
        self.__isCatJamEnabled = isCatJamEnabled
        self.__isCutenessEnabled = isCutenessEnabled
        self.__isDiccionarioEnabled = isDiccionarioEnabled
        self.__isGiveCutenessEnabled = isGiveCutenessEnabled
        self.__isJishoEnabled = isJishoEnabled
        self.__isJokesEnabled = isJokesEnabled
        self.__isPicOfTheDayEnabled = isPicOfTheDayEnabled
        self.__isPkmnEnabled = isPkmnEnabled
        self.__isPokepediaEnabled = isPokepediaEnabled
        self.__isRaidLinkMessagingEnabled = isRaidLinkMessagingEnabled
        self.__isRatJamEnabled = isRatJamEnabled
        self.__isTamalesEnabled = isTamalesEnabled
        self.__isTriviaEnabled = isTriviaEnabled
        self.__isWeatherEnabled = isWeatherEnabled
        self.__isWordOfTheDayEnabled = isWordOfTheDayEnabled
        self.__discord = discord
        self.__handle = handle
        self.__increaseCutenessDoubleRewardId = increaseCutenessDoubleRewardId
        self.__increaseCutenessRewardId = increaseCutenessRewardId
        self.__locationId = locationId
        self.__picOfTheDayFile = picOfTheDayFile
        self.__picOfTheDayRewardId = picOfTheDayRewardId
        self.__pkmnBattleRewardId = pkmnBattleRewardId
        self.__pkmnCatchRewardId = pkmnCatchRewardId
        self.__pkmnEvolveRewardId = pkmnEvolveRewardId
        self.__pkmnShinyRewardId = pkmnShinyRewardId
        self.__speedrunProfile = speedrunProfile
        self.__twitter = twitter
        self.__timeZones = timeZones

    def fetchPicOfTheDay(self) -> str:
        if not self.__isPicOfTheDayEnabled:
            raise RuntimeError(f'POTD is disabled for {self.__handle}')
        elif not os.path.exists(self.__picOfTheDayFile):
            raise FileNotFoundError(f'POTD file not found: \"{self.__picOfTheDayFile}\"')

        with open(self.__picOfTheDayFile, 'r') as file:
            potdText = utils.cleanStr(file.read())

        if not utils.isValidUrl(potdText):
            raise ValueError(f'POTD text is malformed: \"{potdText}\"')

        potdParsed = urllib.parse.urlparse(potdText)
        return potdParsed.geturl()

    def getDiscord(self) -> str:
        return self.__discord

    def getHandle(self) -> str:
        return self.__handle

    def getIncreaseCutenessDoubleRewardId(self) -> str:
        return self.__increaseCutenessDoubleRewardId

    def getIncreaseCutenessRewardId(self) -> str:
        return self.__increaseCutenessRewardId

    def getLocationId(self) -> str:
        return self.__locationId

    def getPicOfTheDayRewardId(self) -> str:
        return self.__picOfTheDayRewardId

    def getPkmnBattleRewardId(self) -> str:
        return self.__pkmnBattleRewardId

    def getPkmnCatchRewardId(self) -> str:
        return self.__pkmnCatchRewardId

    def getPkmnEvolveRewardId(self) -> str:
        return self.__pkmnEvolveRewardId

    def getPkmnShinyRewardId(self) -> str:
        return self.__pkmnShinyRewardId

    def getSpeedrunProfile(self) -> str:
        return self.__speedrunProfile

    def getTimeZones(self) -> List[tzinfo]:
        return self.__timeZones

    def getTwitter(self) -> str:
        return self.__twitter

    def hasDiscord(self) -> bool:
        return utils.isValidStr(self.__discord)

    def hasLocationId(self) -> bool:
        return utils.isValidStr(self.__locationId)

    def hasSpeedrunProfile(self) -> bool:
        return utils.isValidStr(self.__speedrunProfile)

    def hasTimeZones(self) -> bool:
        return utils.hasItems(self.__timeZones)

    def hasTwitter(self) -> bool:
        return utils.isValidStr(self.__twitter)

    def isAnalogueEnabled(self) -> bool:
        return self.__isAnalogueEnabled

    def isCatJamEnabled(self) -> bool:
        return self.__isCatJamEnabled

    def isCutenessEnabled(self) -> bool:
        return self.__isCutenessEnabled

    def isDiccionarioEnabled(self) -> bool:
        return self.__isDiccionarioEnabled

    def isGiveCutenessEnabled(self) -> bool:
        return self.__isGiveCutenessEnabled

    def isJishoEnabled(self) -> bool:
        return self.__isJishoEnabled

    def isJokesEnabled(self) -> bool:
        return self.__isJokesEnabled

    def isPicOfTheDayEnabled(self) -> bool:
        return self.__isPicOfTheDayEnabled

    def isPkmnEnabled(self) -> bool:
        return self.__isPkmnEnabled

    def isPokepediaEnabled(self) -> bool:
        return self.__isPokepediaEnabled

    def isRaidLinkMessagingEnabled(self) -> bool:
        return self.__isRaidLinkMessagingEnabled

    def isRatJamEnabled(self) -> bool:
        return self.__isRatJamEnabled

    def isTamalesEnabled(self) -> bool:
        return self.__isTamalesEnabled

    def isTriviaEnabled(self) -> bool:
        return self.__isTriviaEnabled

    def isWeatherEnabled(self) -> bool:
        return self.__isWeatherEnabled

    def isWordOfTheDayEnabled(self) -> bool:
        return self.__isWordOfTheDayEnabled
