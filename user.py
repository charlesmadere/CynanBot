import os
import pytz
from urllib.parse import urlparse

class User:
    __timeZones = dict()

    def __init__(
        self,
        handle: str,
        picOfTheDayFile: str,
        picOfTheDayRewardId: str,
        timeZone: str
    ):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif picOfTheDayFile == None or len(picOfTheDayFile) == 0 or picOfTheDayFile.isspace():
            raise ValueError(f'picOfTheDayFile argument is malformed: \"{picOfTheDayFile}\"')

        self.__handle = handle
        self.__picOfTheDayFile = picOfTheDayFile
        self.__picOfTheDayRewardId = picOfTheDayRewardId

        if timeZone == None or len(timeZone) == 0 or timeZone.isspace():
            self.__timeZone = None
        else:
            if timeZone not in self.__timeZones:
                self.__timeZones[timeZone] = pytz.timezone(timeZone)

            self.__timeZone = self.__timeZones[timeZone]

    def fetchPicOfTheDay(self):
        if not os.path.exists(self.__picOfTheDayFile):
            raise FileNotFoundError(f'POTD file not found: \"{self.__picOfTheDayFile}\"')

        potdText = None

        with open(self.__picOfTheDayFile, 'r') as file:
            potdText = file.read().replace('\n', '').lstrip().rstrip()

        if potdText == None or len(potdText) == 0 or potdText.isspace():
            raise ValueError(f'POTD text is malformed: \"{potdText}\"')

        potdParsed = urlparse(potdText)
        potdUrl = potdParsed.geturl()

        if potdUrl == None or len(potdUrl) == 0 or potdUrl.isspace():
            raise ValueError(f'POTD URL is malformed: \"{potdUrl}\"')

        return potdUrl

    def getHandle(self):
        return self.__handle

    def getPicOfTheDayRewardId(self):
        return self.__picOfTheDayRewardId

    def getTimeZone(self):
        return self.__timeZone
