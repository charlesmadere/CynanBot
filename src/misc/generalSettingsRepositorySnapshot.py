from typing import Any

from . import utils as utils
from ..network.networkClientType import NetworkClientType
from ..network.networkJsonMapperInterface import NetworkJsonMapperInterface
from ..storage.databaseType import DatabaseType
from ..storage.storageJsonMapperInterface import StorageJsonMapperInterface


class GeneralSettingsRepositorySnapshot:

    def __init__(
        self,
        defaultDatabaseType: DatabaseType,
        defaultNetworkClientType: NetworkClientType,
        jsonContents: dict[str, Any],
        networkJsonMapper: NetworkJsonMapperInterface,
        storageJsonMapper: StorageJsonMapperInterface
    ):
        if not isinstance(defaultDatabaseType, DatabaseType):
            raise TypeError(f'defaultDatabaseType argument is malformed: \"{defaultDatabaseType}\"')
        elif not isinstance(defaultNetworkClientType, NetworkClientType):
            raise TypeError(f'defaultNetworkClientType argument is malformed: \"{defaultNetworkClientType}\"')
        elif not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')
        elif not isinstance(networkJsonMapper, NetworkJsonMapperInterface):
            raise TypeError(f'networkJsonMapper argument is malformed: \"{networkJsonMapper}\"')
        elif not isinstance(storageJsonMapper, StorageJsonMapperInterface):
            raise TypeError(f'storageJsonMapper argument is malformed: \"{storageJsonMapper}\"')

        self.__defaultDatabaseType: DatabaseType = defaultDatabaseType
        self.__defaultNetworkClientType: NetworkClientType = defaultNetworkClientType
        self.__jsonContents: dict[str, Any] = jsonContents
        self.__networkJsonMapper: NetworkJsonMapperInterface = networkJsonMapper
        self.__storageJsonMapper: StorageJsonMapperInterface = storageJsonMapper

    def getSuperTriviaGamePoints(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGamePoints', 25)

    def getSuperTriviaGameShinyMultiplier(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGameShinyMultiplier', 3)

    def getSuperTriviaGameToxicMultiplier(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGameToxicMultiplier', 2)

    def getSuperTriviaGamePerUserAttempts(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGamePerUserAttempts', 2)

    def getSuperTriviaGameToxicPunishmentMultiplier(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGameToxicPunishmentMultiplier', 2)

    def getTriviaGamePoints(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'triviaGamePoints', 5)

    def getTriviaGameShinyMultiplier(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'triviaGameShinyMultiplier', 5)

    def getWaitForSuperTriviaAnswerDelay(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'waitForSuperTriviaAnswerDelay', 45)

    def getWaitForTriviaAnswerDelay(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'waitForTriviaAnswerDelay', 30)

    def isCatJamMessageEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'catJamMessageEnabled', False)

    def isDebugLoggingEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'debugLoggingEnabled', True)

    def isDeerForceMessageEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'deerForceMessageEnabled', False)

    def isEventSubEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'eventSubEnabled', False)

    def isEyesMessageEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'eyesMessageEnabled', False)

    def isFuntoonApiEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'funtoonApiEnabled', True)

    def isFuntoonTwitchChatFallbackEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'funtoonTwitchChatFallbackEnabled', True)

    def isImytSlurpMessageEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'imytSlurpMessageEnabled', False)

    def isJamCatMessageEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'jamCatMessageEnabled', False)

    def isJishoEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'jishoEnabled', True)

    def isPersistAllUsersEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'persistAllUsersEnabled', False)

    def isPokepediaEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'pokepediaEnabled', True)

    def isPubSubPongLoggingEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'pubSubPongLoggingEnabled', False)

    def isRatJamMessageEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'ratJamMessageEnabled', False)

    def isRoachMessageEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'roachMessageEnabled', False)

    def isSchubertWalkMessageEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'schubertWalkMessageEnabled', False)

    def isSuperTriviaGameEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'superTriviaGameEnabled', False)

    def isTranslateEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'translateEnabled', True)

    def isTriviaGameEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'triviaGameEnabled', True)

    def isTwitchChatApiEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'twitchChatApiEnabled', False)

    def requireAdministrator(self) -> str:
        administrator = self.__jsonContents.get('administrator')

        if not utils.isValidStr(administrator):
            raise ValueError(f'\"administrator\" in General Settings file is malformed: \"{administrator}\"')

        return administrator

    def requireDatabaseType(self) -> DatabaseType:
        databaseType = self.__jsonContents.get('databaseType')

        if utils.isValidStr(databaseType):
            return self.__storageJsonMapper.parseDatabaseType(databaseType)
        else:
            return self.__defaultDatabaseType

    def requireNetworkClientType(self) -> NetworkClientType:
        networkClientType = self.__jsonContents.get('networkClientType')

        if utils.isValidStr(networkClientType):
            return self.__networkJsonMapper.parseClientType(networkClientType)
        else:
            return self.__defaultNetworkClientType
