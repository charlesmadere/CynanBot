import os
import urllib
from datetime import tzinfo
from typing import List

import utils


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
        isWordOfTheDayEnabled: bool,
        discord: str,
        handle: str,
        increaseCutenessDoubleRewardId: str,
        increaseCutenessRewardId: str,
        locationId: str,
        picOfTheDayFile: str,
        picOfTheDayRewardId: str,
        speedrunProfile: str,
        twitter: str,
        timeZone: tzinfo
    ):
        if handle is None or len(handle) == 0:
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif isPicOfTheDayEnabled and (picOfTheDayFile is None or len(picOfTheDayFile) == 0):
            raise ValueError(f'picOfTheDayFile argument is malformed: \"{picOfTheDayFile}\"')

        self.__isAnalogueEnabled = isAnalogueEnabled
        self.__isCatJamEnabled = isCatJamEnabled
        self.__isCutenessEnabled = isCutenessEnabled
        self.__isGiveCutenessEnabled = isGiveCutenessEnabled
        self.__isJishoEnabled = isJishoEnabled
        self.__isJokesEnabled = isJokesEnabled
        self.__isPicOfTheDayEnabled = isPicOfTheDayEnabled
        self.__isWordOfTheDayEnabled = isWordOfTheDayEnabled
        self.__discord = discord
        self.__handle = handle
        self.__increaseCutenessDoubleRewardId = increaseCutenessDoubleRewardId
        self.__increaseCutenessRewardId = increaseCutenessRewardId
        self.__locationId = locationId
        self.__picOfTheDayFile = picOfTheDayFile
        self.__picOfTheDayRewardId = picOfTheDayRewardId
        self.__speedrunProfile = speedrunProfile
        self.__twitter = twitter
        self.__timeZone = timeZone

    def fetchPicOfTheDay(self):
        if not self.__isPicOfTheDayEnabled:
            raise RuntimeError(f'POTD is disabled for {self.__handle}')
        elif not os.path.exists(self.__picOfTheDayFile):
            raise FileNotFoundError(
                f'POTD file not found: \"{self.__picOfTheDayFile}\"')

        with open(self.__picOfTheDayFile, 'r') as file:
            potdText = utils.cleanStr(file.read())

        if not utils.isValidStr(potdText):
            raise ValueError(f'POTD text is malformed: \"{potdText}\"')

        potdParsed = urllib.parse.urlparse(potdText)
        potdUrl = potdParsed.geturl()

        if not utils.isValidStr(potdUrl):
            raise ValueError(f'POTD text ({potdText}) can\'t be parsed into URL: \"{potdUrl}\"')

        return potdUrl

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

    def getSpeedrunProfile(self):
        return self.__speedrunProfile

    def getTimeZone(self):
        return self.__timeZone

    def getTwitter(self):
        return self.__twitter

    def hasDiscord(self):
        return utils.isValidStr(self.__discord)

    def hasLocationId(self):
        return utils.isValidStr(self.__locationId)

    def hasSpeedrunProfile(self):
        return utils.isValidStr(self.__speedrunProfile)

    def hasTimeZone(self):
        return self.__timeZone is not None

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

    def isWordOfTheDayEnabled(self):
        return self.__isWordOfTheDayEnabled
