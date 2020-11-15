import os
import urllib
from datetime import tzinfo


class User:

    def __init__(
        self,
        isAnalogueEnabled: bool,
        isCatJamEnabled: bool,
        isCutenessEnabled: bool,
        isGiveCutenessEnabled: bool,
        isJishoEnabled: bool,
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
        if handle == None or len(handle) == 0:
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif isPicOfTheDayEnabled and (picOfTheDayFile == None or len(picOfTheDayFile) == 0):
            raise ValueError(f'picOfTheDayFile argument is malformed: \"{picOfTheDayFile}\"')

        self.__isAnalogueEnabled = isAnalogueEnabled
        self.__isCatJamEnabled = isCatJamEnabled
        self.__isCutenessEnabled = isCutenessEnabled
        self.__isGiveCutenessEnabled = isGiveCutenessEnabled
        self.__isJishoEnabled = isJishoEnabled
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
            raise FileNotFoundError(f'POTD file not found: \"{self.__picOfTheDayFile}\"')

        with open(self.__picOfTheDayFile, 'r') as file:
            potdText = file.read().replace('\n', '').strip()

        if potdText == None or len(potdText) == 0 or potdText.isspace():
            raise ValueError(f'POTD text is malformed: \"{potdText}\"')

        potdParsed = urllib.parse.urlparse(potdText)
        potdUrl = potdParsed.geturl()

        if potdUrl == None or len(potdUrl) == 0 or potdUrl.isspace():
            raise ValueError(f'POTD URL is malformed: \"{potdUrl}\"')

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
        return self.__discord != None and len(self.__discord) != 0

    def hasLocationId(self):
        return self.__locationId != None and len(self.__locationId) != 0

    def hasSpeedrunProfile(self):
        return self.__speedrunProfile != None and len(self.__speedrunProfile) != 0

    def hasTimeZone(self):
        return self.__timeZone != None

    def hasTwitter(self):
        return self.__twitter != None and len(self.__twitter) != 0

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

    def isPicOfTheDayEnabled(self):
        return self.__isPicOfTheDayEnabled

    def isWordOfTheDayEnabled(self):
        return self.__isWordOfTheDayEnabled
