from os import path
from urllib.parse import urlparse

class User:
    def __init__(
        self,
        twitchHandle: str,
        picOfTheDayFile: str
    ):
        self.twitchHandle = twitchHandle
        self.picOfTheDayFile = picOfTheDayFile

        if not path.exists(picOfTheDayFile):
            raise FileNotFoundError(f'POTD file not found: \"{picOfTheDayFile}\"')

    def getPicOfTheDay(self):
        potdText = ""

        with open(self.picOfTheDayFile, 'r') as file:
            potdText = file.read().replace('\n', '').lstrip().rstrip()

        if len(potdText) == 0 or potdText.isspace():
            raise RuntimeError('POTD text is empty or blank')

        potdParsed = urlparse(potdText)
        potdUrl = potdParsed.geturl()

        if len(potdUrl) == 0 or potdUrl.isspace():
            raise RuntimeError('POTD URL is nil or empty or blank')

        return potdUrl
