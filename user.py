from os import path

class User:
    def __init__(
        self,
        twitchHandle: str,
        picOfTheDayFile: str
    ):
        self.twitchHandle = twitchHandle
        self.picOfTheDayFile = picOfTheDayFile

        if not path.exists(picOfTheDayFile):
            raise RuntimeError(f'POTD file not found: \"{picOfTheDayFile}\"')

    def getPicOfTheDay(self):
        picOfTheDay = ""

        with open(self.picOfTheDayFile, 'r') as file:
            picOfTheDay = file.read().replace('\n', '')

        return picOfTheDay
