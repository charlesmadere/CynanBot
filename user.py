import os
from urllib.parse import urlparse

class User:
    def __init__(
        self,
        handle: str,
        picOfTheDayFile: str,
        rewardId: str,
        timeZone: str
    ):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif picOfTheDayFile == None or len(picOfTheDayFile) == 0 or picOfTheDayFile.isspace():
            raise ValueError(f'picOfTheDayFile argument is malformed: \"{picOfTheDayFile}\"')

        self.__handle = handle
        self.__picOfTheDayFile = picOfTheDayFile
        self.__rewardId = rewardId
        self.__timeZone = timeZone

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

    def getRewardId(self):
        return self.__rewardId
