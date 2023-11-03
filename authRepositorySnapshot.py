from typing import Any, Dict

import CynanBotCommon.utils as utils


class AuthRepositorySnapshot():

    def __init__(self, jsonContents: Dict[str, Any]):
        if not utils.hasItems(jsonContents):
            raise ValueError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        self.__jsonContents: Dict[str, Any] = jsonContents

    def getDeepLAuthKey(self) -> str:
        return utils.getStrFromDict(self.__jsonContents, 'deepLAuthKey', '')

    def getMerriamWebsterApiKey(self) -> str:
        return utils.getStrFromDict(self.__jsonContents, 'merriamWebsterApiKey', '')

    def getOneWeatherApiKey(self) -> str:
        return utils.getStrFromDict(self.__jsonContents, 'oneWeatherApiKey', '')

    def getQuizApiKey(self) -> str:
        return utils.getStrFromDict(self.__jsonContents, 'quizApiKey', '')

    def hasDeepLAuthKey(self) -> bool:
        return utils.isValidStr(self.getDeepLAuthKey())

    def hasMerriamWebsterApiKey(self) -> bool:
        return utils.isValidStr(self.getMerriamWebsterApiKey())

    def hasOneWeatherApiKey(self) -> bool:
        return utils.isValidStr(self.getOneWeatherApiKey())

    def hasQuizApiKey(self) -> bool:
        return utils.isValidStr(self.getQuizApiKey())

    def requireDeepLAuthKey(self) -> str:
        deepLAuthKey = self.getDeepLAuthKey()

        if not utils.isValidStr(deepLAuthKey):
            raise ValueError(f'\"deepLAuthKey\" in Auth Repository file is malformed: \"{deepLAuthKey}\"')

        return deepLAuthKey

    def requireMerriamWebsterApiKey(self) -> str:
        merriamWebsterApiKey = self.getMerriamWebsterApiKey()

        if not utils.isValidStr(merriamWebsterApiKey):
            raise ValueError(f'\"merriamWebsterApiKey\" in Auth Repository file is malformed: \"{merriamWebsterApiKey}\"')

        return merriamWebsterApiKey

    def requireOneWeatherApiKey(self) -> str:
        oneWeatherApiKey = self.getOneWeatherApiKey()

        if not utils.isValidStr(oneWeatherApiKey):
            raise ValueError(f'\"oneWeatherApiKey\" in Auth Repository file is malformed: \"{oneWeatherApiKey}\"')

        return oneWeatherApiKey

    def requireQuizApiKey(self) -> str:
        quizApiKey = self.getQuizApiKey()

        if not utils.isValidStr(quizApiKey):
            raise ValueError(f'\"quizApiKey\" in Auth Repository file is malformed: \"{quizApiKey}\"')

        return quizApiKey

    def requireTwitchClientId(self) -> str:
        twitchClientId = self.__jsonContents.get('twitchClientId')

        if not utils.isValidStr(twitchClientId):
            raise ValueError(f'\"twitchClientId\" in Auth Repository file is malformed: \"{twitchClientId}\"')

        return twitchClientId

    def requireTwitchClientSecret(self) -> str:
        twitchClientSecret = self.__jsonContents.get('twitchClientSecret')

        if not utils.isValidStr(twitchClientSecret):
            raise ValueError(f'\"twitchClientSecret\" in Auth Repository file is malformed: \"{twitchClientSecret}\"')

        return twitchClientSecret

    def requireTwitchHandle(self) -> str:
        twitchHandle = self.__jsonContents.get('twitchHandle')

        if not utils.isValidStr(twitchHandle):
            raise ValueError(f'\"twitchHandle\" in Auth Repository file is malformed: \"{twitchHandle}\"')

        return twitchHandle

    def requireTwitchIrcAuthToken(self) -> str:
        twitchIrcAuthToken = self.__jsonContents.get('twitchIrcAuthToken')

        if not utils.isValidStr(twitchIrcAuthToken):
            raise ValueError(f'\"twitchIrcAuthToken\" in Auth Repository file is malformed: \"{twitchIrcAuthToken}\"')

        return twitchIrcAuthToken
