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
        isGiveCutenessEnabled: bool,
        isJishoEnabled: bool,
        isJokesEnabled: bool,
        isPicOfTheDayEnabled: bool,
        isPkmnEnabled: bool,
        isRatJamEnabled: bool,
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
        self.__isGiveCutenessEnabled = isGiveCutenessEnabled
        self.__isJishoEnabled = isJishoEnabled
        self.__isJokesEnabled = isJokesEnabled
        self.__isPicOfTheDayEnabled = isPicOfTheDayEnabled
        self.__isPkmnEnabled = isPkmnEnabled
        self.__isRatJamEnabled = isRatJamEnabled
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

    def fetchPicOfTheDay(self):
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

    def getDiscord(self):
        return self.__discord

    def getHandle(self):
        return self.__handle

    def getIncreaseCutenessDoubleRewardId(self):
        return self.__increaseCutenessDoubleRewardId

    def getIncreaseCutenessRewardId(self):
        return self.__increaseCutenessRewardId

    def getLocationId(self):
        return self.__locationId

    def getPicOfTheDayRewardId(self):
        return self.__picOfTheDayRewardId

    def getPkmnBattleRewardId(self):
        return self.__pkmnBattleRewardId

    def getPkmnCatchRewardId(self):
        return self.__pkmnCatchRewardId

    def getPkmnEvolveRewardId(self):
        return self.__pkmnEvolveRewardId

    def getPkmnShinyRewardId(self):
        return self.__pkmnShinyRewardId

    def getSpeedrunProfile(self):
        return self.__speedrunProfile

    def getTimeZones(self):
        return self.__timeZones

    def getTwitter(self):
        return self.__twitter

    def hasDiscord(self):
        return utils.isValidStr(self.__discord)

    def hasLocationId(self):
        return utils.isValidStr(self.__locationId)

    def hasSpeedrunProfile(self):
        return utils.isValidStr(self.__speedrunProfile)

    def hasTimeZones(self):
        return self.__timeZones is not None and len(self.__timeZones) >= 1

    def hasTwitter(self):
        return utils.isValidStr(self.__twitter)

    def isAnalogueEnabled(self):
        return self.__isAnalogueEnabled

    def isCatJamEnabled(self):
        return self.__isCatJamEnabled

    def isCutenessEnabled(self):
        return self.__isCutenessEnabled

    def isGiveCutenessEnabled(self):
        return self.__isGiveCutenessEnabled

    def isJishoEnabled(self):
        return self.__isJishoEnabled

    def isJokesEnabled(self):
        return self.__isJokesEnabled

    def isPicOfTheDayEnabled(self):
        return self.__isPicOfTheDayEnabled

    def isPkmnEnabled(self):
        return self.__isPkmnEnabled

    def isRatJamEnabled(self):
        return self.__isRatJamEnabled

    def isWordOfTheDayEnabled(self):
        return self.__isWordOfTheDayEnabled
