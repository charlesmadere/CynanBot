import os
from urllib.parse import urlparse

class User:
    def __init__(
        self,
        isAnalogueEnabled: bool,
        isDeWordOfTheDayEnabled: bool,
        isEnEsWordOfTheDayEnabled: bool,
        isEnPtWordOfTheDayEnabled: bool,
        isEsWordOfTheDayEnabled: bool,
        isFrWordOfTheDayEnabled: bool,
        isIncreaseCutenessEnabled: bool,
        isItWordOfTheDayEnabled: bool,
        isJaWordOfTheDayEnabled: bool,
        isKoWordOfTheDayEnabled: bool,
        isNoWordOfTheDayEnabled: bool,
        isPicOfTheDayEnabled: bool,
        isPtWordOfTheDayEnabled: bool,
        isRuWordOfTheDayEnabled: bool,
        isSvWordOfTheDayEnabled: bool,
        isZhWordOfTheDayEnabled: bool,
        discord: str,
        handle: str,
        increaseCutenessRewardId: str,
        picOfTheDayFile: str,
        picOfTheDayRewardId: str,
        speedrunProfile: str,
        twitter: str,
        timeZone
    ):
        if handle == None or len(handle) == 0:
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif isPicOfTheDayEnabled and (picOfTheDayFile == None or len(picOfTheDayFile) == 0):
            raise ValueError(f'picOfTheDayFile argument is malformed: \"{picOfTheDayFile}\"')

        self.__isAnalogueEnabled = isAnalogueEnabled
        self.__isDeWordOfTheDayEnabled = isDeWordOfTheDayEnabled
        self.__isEnEsWordOfTheDayEnabled = isEnEsWordOfTheDayEnabled
        self.__isEnPtWordOfTheDayEnabled = isEnPtWordOfTheDayEnabled
        self.__isEsWordOfTheDayEnabled = isEsWordOfTheDayEnabled
        self.__isFrWordOfTheDayEnabled = isFrWordOfTheDayEnabled
        self.__isIncreaseCutenessEnabled = isIncreaseCutenessEnabled
        self.__isItWordOfTheDayEnabled = isItWordOfTheDayEnabled
        self.__isJaWordOfTheDayEnabled = isJaWordOfTheDayEnabled
        self.__isKoWordOfTheDayEnabled = isKoWordOfTheDayEnabled
        self.__isNoWordOfTheDayEnabled = isNoWordOfTheDayEnabled
        self.__isPicOfTheDayEnabled = isPicOfTheDayEnabled
        self.__isPtWordOfTheDayEnabled = isPtWordOfTheDayEnabled
        self.__isRuWordOfTheDayEnabled = isRuWordOfTheDayEnabled
        self.__isSvWordOfTheDayEnabled = isSvWordOfTheDayEnabled
        self.__isZhWordOfTheDayEnabled = isZhWordOfTheDayEnabled
        self.__discord = discord
        self.__handle = handle
        self.__increaseCutenessRewardId = increaseCutenessRewardId
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

        potdParsed = urlparse(potdText)
        potdUrl = potdParsed.geturl()

        if potdUrl == None or len(potdUrl) == 0 or potdUrl.isspace():
            raise ValueError(f'POTD URL is malformed: \"{potdUrl}\"')

        return potdUrl

    def getDiscord(self):
        return self.__discord

    def getHandle(self):
        return self.__handle

    def getIncreaseCutenessRewardId(self):
        return self.__increaseCutenessRewardId

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

    def hasSpeedrunProfile(self):
        return self.__speedrunProfile != None and len(self.__speedrunProfile) != 0

    def hasTimeZone(self):
        return self.__timeZone != None

    def hasTwitter(self):
        return self.__twitter != None and len(self.__twitter) != 0

    def isAnalogueEnabled(self):
        return self.__isAnalogueEnabled

    def isDeWordOfTheDayEnabled(self):
        return self.__isDeWordOfTheDayEnabled

    def isEnEsWordOfTheDayEnabled(self):
        return self.__isEnEsWordOfTheDayEnabled

    def isEnPtWordOfTheDayEnabled(self):
        return self.__isEnPtWordOfTheDayEnabled

    def isEsWordOfTheDayEnabled(self):
        return self.__isEsWordOfTheDayEnabled

    def isFrWordOfTheDayEnabled(self):
        return self.__isFrWordOfTheDayEnabled

    def isIncreaseCutenessEnabled(self):
        return self.__isIncreaseCutenessEnabled

    def isItWordOfTheDayEnabled(self):
        return self.__isItWordOfTheDayEnabled

    def isJaWordOfTheDayEnabled(self):
        return self.__isJaWordOfTheDayEnabled

    def isKoWordOfTheDayEnabled(self):
        return self.__isKoWordOfTheDayEnabled

    def isNoWordOfTheDayEnabled(self):
        return self.__isNoWordOfTheDayEnabled

    def isPicOfTheDayEnabled(self):
        return self.__isPicOfTheDayEnabled

    def isPtWordOfTheDayEnabled(self):
        return self.__isPtWordOfTheDayEnabled

    def isRuWordOfTheDayEnabled(self):
        return self.__isRuWordOfTheDayEnabled

    def isSvWordOfTheDayEnabled(self):
        return self.__isSvWordOfTheDayEnabled

    def isZhWordOfTheDayEnabled(self):
        return self.__isZhWordOfTheDayEnabled
