from authHelper import AuthHelper
from channelIdsRepository import ChannelIdsRepository
import json
import os
import requests
from urllib.parse import urlparse

class User:
    def __init__(
        self,
        authHelper: AuthHelper,
        channelIdsRepository: ChannelIdsRepository,
        handle: str,
        picOfTheDayFile: str,
        rewardId: str
    ):
        self.__authHelper = authHelper
        self.__handle = handle
        self.__picOfTheDayFile = picOfTheDayFile
        self.__rewardId = rewardId
        self.__channelIdsRepository = channelIdsRepository

        if not os.path.exists(picOfTheDayFile):
            raise FileNotFoundError(f'POTD file not found: \"{picOfTheDayFile}\"')

    def fetchChannelId(self):
        channelId = self.__channelIdsRepository.getChannelId(handle = self.getHandle())

        if channelId != None:
            return channelId

        headers = {
            'Client-ID': self.__authHelper.getClientId(),
            'Authorization': f'Bearer {self.getAccessToken()}'
        }

        rawResponse = requests.get(
            url = f'https://api.twitch.tv/helix/users?login={self.getHandle()}',
            headers = headers
        )

        jsonResponse = json.loads(rawResponse.content)

        if 'error' in jsonResponse and len(jsonResponse['error']) >= 1:
            raise ValueError(f'Received an error when fetching channel ID for {self.getHandle()}: {jsonResponse}')

        channelId = jsonResponse['data'][0]['id']

        if channelId == None or len(channelId) == 0 or channelId.isspace():
            raise ValueError(f'Unable to fetch channel ID for {self.getHandle()}: {jsonResponse}')

        self.__channelIdsRepository.setChannelId(
            handle = self.getHandle(),
            channelId = channelId
        )

        return channelId

    def fetchPicOfTheDay(self):
        potdText = ""

        if not os.path.exists(self.__picOfTheDayFile):
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

    def getAccessToken(self):
        return self.__authHelper.getAccessToken(self.getHandle())

    def getHandle(self):
        return self.__handle

    def getRewardId(self):
        return self.__rewardId
