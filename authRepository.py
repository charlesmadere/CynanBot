import json
import os
from typing import Dict

import CynanBotCommon.utils as utils


class AuthRepository():

    def __init__(
        self,
        authFile: str = 'authRepository.json'
    ):
        if not utils.isValidStr(authFile):
            raise ValueError(f'authRepository argument is malformed: \"{authFile}\"')

        self.__authFile: str = authFile

    def getDeepLAuthKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('deepLAuthKey')

    def getMerriamWebsterApiKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('merriamWebsterApiKey')

    def getOneWeatherApiKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('oneWeatherApiKey')

    def getQuizApiKey(self) -> str:
        jsonContents = self.__readJson()
        return jsonContents.get('quizApiKey')

    def hasDeepLAuthKey(self) -> bool:
        return utils.isValidStr(self.getDeepLAuthKey())

    def hasMerriamWebsterApiKey(self) -> bool:
        return utils.isValidStr(self.getMerriamWebsterApiKey())

    def hasOneWeatherApiKey(self) -> bool:
        return utils.isValidStr(self.getOneWeatherApiKey())

    def hasQuizApiKey(self) -> bool:
        return utils.isValidStr(self.getQuizApiKey())

    def __readJson(self) -> Dict[str, object]:
        if not os.path.exists(self.__authFile):
            raise FileNotFoundError(f'Auth file not found: \"{self.__authFile}\"')

        with open(self.__authFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from auth file: \"{self.__authFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of auth file \"{self.__authFile}\" is empty')

        return jsonContents

    def requireDeepLAuthKey(self) -> str:
        deepLAuthKey = self.getDeepLAuthKey()

        if not utils.isValidStr(deepLAuthKey):
            raise ValueError(f'\"deepLAuthKey\" in auth file \"{self.__authFile}\" is malformed: \"{deepLAuthKey}\"')

        return deepLAuthKey

    def requireMerriamWebsterApiKey(self) -> str:
        merriamWebsterApiKey = self.getMerriamWebsterApiKey()

        if not utils.isValidStr(merriamWebsterApiKey):
            raise ValueError(f'\"merriamWebsterApiKey\" in auth file \"{self.__authFile}\" is malformed: \"{merriamWebsterApiKey}\"')

        return merriamWebsterApiKey

    def requireNick(self) -> str:
        jsonContents = self.__readJson()

        nick = jsonContents.get('nick')
        if not utils.isValidStr(nick):
            raise ValueError(f'\"nick\" in auth file \"{self.__authFile}\" is malformed: \"{nick}\"')

        return nick

    def requireOneWeatherApiKey(self) -> str:
        oneWeatherApiKey = self.getOneWeatherApiKey()

        if not utils.isValidStr(oneWeatherApiKey):
            raise ValueError(f'\"oneWeatherApiKey\" in auth file \"{self.__authFile}\" is malformed: \"{oneWeatherApiKey}\"')

        return oneWeatherApiKey

    def requireQuizApiKey(self) -> str:
        quizApiKey = self.getQuizApiKey()

        if not utils.isValidStr(quizApiKey):
            raise ValueError(f'\"quizApiKey\" in auth file \"{self.__authFile}\" is malformed: \"{quizApiKey}\"')

        return quizApiKey

    def requireTwitchClientId(self) -> str:
        jsonContents = self.__readJson()

        twitchClientId = jsonContents.get('twitchClientId')
        if not utils.isValidStr(twitchClientId):
            raise ValueError(f'\"twitchClientId\" in auth file \"{self.__authFile}\" is malformed: \"{twitchClientId}\"')

        return twitchClientId

    def requireTwitchClientSecret(self) -> str:
        jsonContents = self.__readJson()

        twitchClientSecret = jsonContents.get('twitchClientSecret')
        if not utils.isValidStr(twitchClientSecret):
            raise ValueError(f'\"twitchClientSecret\" in auth file \"{self.__authFile}\" is malformed: \"{twitchClientSecret}\"')

        return twitchClientSecret

    def requireTwitchIrcAuthToken(self) -> str:
        jsonContents = self.__readJson()

        twitchIrcAuthToken = jsonContents.get('twitchIrcAuthToken')
        if not utils.isValidStr(twitchIrcAuthToken):
            raise ValueError(f'\"twitchIrcAuthToken\" in auth file \"{self.__authFile}\" is malformed: \"{twitchIrcAuthToken}\"')

        return twitchIrcAuthToken
