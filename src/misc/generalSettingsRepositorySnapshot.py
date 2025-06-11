from typing import Any

from . import utils as utils
from ..network.networkClientType import NetworkClientType
from ..network.networkJsonMapperInterface import NetworkJsonMapperInterface
from ..soundPlayerManager.jsonMapper.soundPlayerJsonMapperInterface import SoundPlayerJsonMapperInterface
from ..soundPlayerManager.soundPlayerType import SoundPlayerType
from ..storage.databaseType import DatabaseType
from ..storage.storageJsonMapperInterface import StorageJsonMapperInterface


class GeneralSettingsRepositorySnapshot:

    def __init__(
        self,
        defaultDatabaseType: DatabaseType,
        defaultNetworkClientType: NetworkClientType,
        jsonContents: dict[str, Any],
        networkJsonMapper: NetworkJsonMapperInterface,
        soundPlayerJsonMapper: SoundPlayerJsonMapperInterface,
        defaultSoundPlayerType: SoundPlayerType,
        storageJsonMapper: StorageJsonMapperInterface,
    ):
        if not isinstance(defaultDatabaseType, DatabaseType):
            raise TypeError(f'defaultDatabaseType argument is malformed: \"{defaultDatabaseType}\"')
        elif not isinstance(defaultNetworkClientType, NetworkClientType):
            raise TypeError(f'defaultNetworkClientType argument is malformed: \"{defaultNetworkClientType}\"')
        elif not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')
        elif not isinstance(networkJsonMapper, NetworkJsonMapperInterface):
            raise TypeError(f'networkJsonMapper argument is malformed: \"{networkJsonMapper}\"')
        elif not isinstance(soundPlayerJsonMapper, SoundPlayerJsonMapperInterface):
            raise TypeError(f'soundPlayerJsonMapper argument is malformed: \"{soundPlayerJsonMapper}\"')
        elif not isinstance(defaultSoundPlayerType, SoundPlayerType):
            raise TypeError(f'defaultSoundPlayerType argument is malformed: \"{defaultSoundPlayerType}\"')
        elif not isinstance(storageJsonMapper, StorageJsonMapperInterface):
            raise TypeError(f'storageJsonMapper argument is malformed: \"{storageJsonMapper}\"')

        self.__defaultDatabaseType: DatabaseType = defaultDatabaseType
        self.__defaultNetworkClientType: NetworkClientType = defaultNetworkClientType
        self.__jsonContents: dict[str, Any] = jsonContents
        self.__networkJsonMapper: NetworkJsonMapperInterface = networkJsonMapper
        self.__soundPlayerJsonMapper: SoundPlayerJsonMapperInterface = soundPlayerJsonMapper
        self.__defaultSoundPlayerType: SoundPlayerType = defaultSoundPlayerType
        self.__storageJsonMapper: StorageJsonMapperInterface = storageJsonMapper

    def getSuperTriviaGamePoints(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGamePoints', 25)

    def getSuperTriviaGameShinyMultiplier(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGameShinyMultiplier', 3)

    def getSuperTriviaGameToxicMultiplier(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGameToxicMultiplier', 8)

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

    def isDebugLoggingEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'debugLoggingEnabled', True)

    def isEventSubEnabled(self) -> bool:
        return utils.getBoolFromDict(
            d = self.__jsonContents,
            key = 'eventSubEnabled',
            fallback = False
        )

    def isFuntoonApiEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'funtoonApiEnabled', True)

    def isFuntoonTwitchChatFallbackEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'funtoonTwitchChatFallbackEnabled', True)

    def isJishoEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'jishoEnabled', True)

    def isPersistAllUsersEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'persistAllUsersEnabled', False)

    def isPokepediaEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'pokepediaEnabled', True)

    def isPubSubPongLoggingEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'pubSubPongLoggingEnabled', False)

    def isSuperTriviaGameEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'superTriviaGameEnabled', False)

    def isTriviaGameEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'triviaGameEnabled', True)

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

    def requireSoundPlayerType(self) -> SoundPlayerType:
        soundPlayerType = self.__jsonContents.get('soundPlayerType')

        if utils.isValidStr(soundPlayerType):
            return self.__soundPlayerJsonMapper.parseSoundPlayerType(soundPlayerType)
        else:
            return self.__defaultSoundPlayerType
