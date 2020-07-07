import json
import requests
from os import path
from urllib.parse import urlparse

class User:
    def __init__(
        self,
        twitchHandle: str,
        picOfTheDayFile: str,
        accessToken: str,
        refreshToken: str,
        rewardId: str
    ):
        self.twitchHandle = twitchHandle
        self.__picOfTheDayFile = picOfTheDayFile
        self.accessToken = accessToken
        self.__refreshToken = refreshToken
        self.rewardId = rewardId
        self.__channelId = None

        if not path.exists(picOfTheDayFile):
            raise FileNotFoundError(f'POTD file not found: \"{picOfTheDayFile}\"')

    def fetchChannelId(self, clientId: str):
        if self.__channelId != None:
            return self.__channelId

        headers = {
            'Client-ID': clientId,
            'Authorization': f'Bearer {self.accessToken}'
        }

        data = requests.get(
            url = f'https://api.twitch.tv/helix/users?login={self.twitchHandle}',
            headers = headers
        )

        jsonResponse = json.loads(data.content)

        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            raise ValueError(f'Received an error when fetching channel ID for {self.twitchHandle}: {jsonResponse}')

        channelId = jsonResponse['data'][0]['id']

        if len(channelId) == 0 or channelId.isspace():
            raise ValueError(f'Unable to fetch channel ID for {self.twitchHandle}: {jsonResponse}')
        else:
            self.__channelId = channelId

        return channelId

    def fetchPicOfTheDay(self):
        potdText = ""

        if not path.exists(self.__picOfTheDayFile):
            raise FileNotFoundError(f'POTD file not found: \"{self.__picOfTheDayFile}\"')

        with open(self.__picOfTheDayFile, 'r') as file:
            potdText = file.read().replace('\n', '').lstrip().rstrip()

        if len(potdText) == 0 or potdText.isspace():
            raise ValueError('POTD text is empty or blank')

        potdParsed = urlparse(potdText)
        potdUrl = potdParsed.geturl()

        if len(potdUrl) == 0 or potdUrl.isspace():
            raise ValueError('POTD URL is empty or blank')

        return potdUrl
