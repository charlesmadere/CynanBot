import os
from urllib.parse import urlparse

class User:
    def __init__(
        self,
        handle: str,
        picOfTheDayFile: str,
        rewardId: str
    ):
        self.__handle = handle
        self.__picOfTheDayFile = picOfTheDayFile
        self.__rewardId = rewardId

    def fetchPicOfTheDay(self):
        potdText = ""

        if not os.path.exists(self.__picOfTheDayFile):
            raise FileNotFoundError(f'POTD file not found: \"{self.__picOfTheDayFile}\"')

        with open(self.__picOfTheDayFile, 'r') as file:
            potdText = file.read().replace('\n', '').lstrip().rstrip()

        if len(potdText) == 0 or potdText.isspace():
            raise ValueError('POTD text is malformed!')

        potdParsed = urlparse(potdText)
        potdUrl = potdParsed.geturl()

        if potdUrl == None or len(potdUrl) == 0 or potdUrl.isspace():
            raise ValueError(f'POTD URL is malformed: \"{potdUrl}\"')

        return potdUrl

    def getHandle(self):
        return self.__handle

    def getRewardId(self):
        return self.__rewardId
