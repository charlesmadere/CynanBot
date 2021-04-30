import json
import os
from typing import Dict

import CynanBotCommon.utils as utils


class AuthHelper():

    def __init__(
        self,
        authFile: str = 'authFile.json'
    ):
        if not utils.isValidStr(authFile):
            raise ValueError(f'authFile argument is malformed: \"{authFile}\"')

        self.__authFile = authFile

    def getIqAirApiKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('iqAirApiKey')

    def getMerriamWebsterApiKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('merriamWebsterApiKey')

    def getOneWeatherApiKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('oneWeatherApiKey')

    def __readJson(self) -> Dict:
        if not os.path.exists(self.__authFile):
            raise FileNotFoundError(f'Auth file not found: \"{self.__authFile}\"')

        with open(self.__authFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from auth file: \"{self.__authFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of auth file \"{self.__authFile}\" is empty')

        return jsonContents

    def requireIqAirApiKey(self) -> str:
        iqAirApiKey = self.getIqAirApiKey()

        if not utils.isValidStr(iqAirApiKey):
            raise ValueError(f'\"iqAirApiKey\" in auth file \"{self.__authFile}\" is malformed: \"{iqAirApiKey}\"')

        return iqAirApiKey

    def requireMerriamWebsterApiKey(self) -> str:
        merriamWebsterApiKey = self.getMerriamWebsterApiKey()

        if not utils.isValidStr(merriamWebsterApiKey):
            raise ValueError(f'\"merriamWebsterApiKey\" in auth file \"{self.__authFile}\" is malformed: \"{merriamWebsterApiKey}\"')

        return merriamWebsterApiKey

    def requireOneWeatherApiKey(self) -> str:
        oneWeatherApiKey = self.getOneWeatherApiKey()

        if not utils.isValidStr(oneWeatherApiKey):
            raise ValueError(f'\"oneWeatherApiKey\" in auth file \"{self.__authFile}\" is malformed: \"{oneWeatherApiKey}\"')

        return oneWeatherApiKey

    def requireTwitchClientId(self) -> str:
        jsonContents = self.__readJson()

        twitchClientId = jsonContents.get('twitchClientId')
        if not utils.isValidStr(twitchClientId):
            raise ValueError(f'\"twitchClientId\" in auth file \"{self.__authFile}\" is malformed: \"{twitchClientId}\"')

        return twitchClientId

    def requireTwitchIrcAuthToken(self) -> str:
        jsonContents = self.__readJson()

        twitchIrcAuthToken = jsonContents.get('twitchIrcAuthToken')
        if not utils.isValidStr(twitchIrcAuthToken):
            raise ValueError(f'\"twitchIrcAuthToken\" in auth file \"{self.__authFile}\" is malformed: \"{twitchIrcAuthToken}\"')

        return twitchIrcAuthToken

    def requireTwitchClientSecret(self) -> str:
        jsonContents = self.__readJson()

        twitchClientSecret = jsonContents.get('twitchClientSecret')
        if not utils.isValidStr(twitchClientSecret):
            raise ValueError(f'\"twitchClientSecret\" in auth file \"{self.__authFile}\" is malformed: \"{twitchClientSecret}\"')

        return twitchClientSecret
