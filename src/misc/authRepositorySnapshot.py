from typing import Any, Final

from frozendict import frozendict

from . import utils as utils


class AuthRepositorySnapshot:

    def __init__(self, jsonContents: frozendict[str, Any]):
        if not isinstance(jsonContents, frozendict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        self.__jsonContents: Final[frozendict[str, Any]] = jsonContents

    def getDeepLAuthKey(self) -> str | None:
        return utils.getStrFromDict(self.__jsonContents, 'deepLAuthKey', fallback = '')

    def getMerriamWebsterApiKey(self) -> str:
        return utils.getStrFromDict(self.__jsonContents, 'merriamWebsterApiKey', fallback = '')

    def getOpenWeatherApiKey(self) -> str:
        return utils.getStrFromDict(self.__jsonContents, 'openWeatherApiKey', fallback = '')

    def getQuizApiKey(self) -> str:
        return utils.getStrFromDict(self.__jsonContents, 'quizApiKey', fallback = '')

    def hasDeepLAuthKey(self) -> bool:
        return utils.isValidStr(self.getDeepLAuthKey())

    def hasMerriamWebsterApiKey(self) -> bool:
        return utils.isValidStr(self.getMerriamWebsterApiKey())

    def hasQuizApiKey(self) -> bool:
        return utils.isValidStr(self.getQuizApiKey())

    def requireDeepLAuthKey(self) -> str:
        deepLAuthKey = self.getDeepLAuthKey()

        if not utils.isValidStr(deepLAuthKey):
            raise ValueError(f'\"deepLAuthKey\" in Auth Repository file is malformed: \"{deepLAuthKey}\"')

        return deepLAuthKey

    def getGoogleCloudProjectKeyId(self) -> str | None:
        return utils.getStrFromDict(self.__jsonContents, 'googleCloudProjectKeyId', fallback = '')

    def getGoogleCloudProjectId(self) -> str | None:
        return utils.getStrFromDict(self.__jsonContents, 'googleCloudProjectId', fallback = '')

    def getGoogleCloudProjectPrivateKey(self) -> str | None:
        return utils.getStrFromDict(self.__jsonContents, 'googleCloudProjectPrivateKey', fallback = '')

    def getGoogleCloudServiceAccountEmail(self) -> str | None:
        return utils.getStrFromDict(self.__jsonContents, 'googleCloudServiceAccountEmail', fallback = '')

    def requireMerriamWebsterApiKey(self) -> str:
        merriamWebsterApiKey = self.getMerriamWebsterApiKey()

        if not utils.isValidStr(merriamWebsterApiKey):
            raise ValueError(f'\"merriamWebsterApiKey\" in Auth Repository file is malformed: \"{merriamWebsterApiKey}\"')

        return merriamWebsterApiKey

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
