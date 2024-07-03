from typing import Any

from . import utils as utils
from ..network.networkClientType import NetworkClientType
from ..storage.databaseType import DatabaseType


class GeneralSettingsRepositorySnapshot():

    def __init__(self, jsonContents: dict[str, Any]):
        if not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')

        self.__jsonContents: dict[str, Any] = jsonContents

    def getEventSubPort(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'eventSubPort', 33239)

    def getRaidLinkMessagingDelay(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'raidLinkMessagingDelay', 60)

    def getRefreshPubSubTokensSeconds(self) -> int:
        refreshPubSubTokensSeconds = utils.getIntFromDict(self.__jsonContents, 'refreshPubSubTokensSeconds', 120)

        if refreshPubSubTokensSeconds < 30:
            raise ValueError(f'\"refreshPubSubTokensSeconds\" value in General Settings file is too aggressive: {refreshPubSubTokensSeconds}')

        return refreshPubSubTokensSeconds

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

    def isChatBandEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'chatBandEnabled', False)

    def isCommandsChatCommandEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'commandsChatCommandEnabled', True)

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

    def isPubSubEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'pubSubEnabled', False)

    def isPubSubPongLoggingEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'pubSubPongLoggingEnabled', False)

    def isRaidLinkMessagingEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'raidLinkMessagingEnabled', True)

    def isRatJamMessageEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'ratJamMessageEnabled', False)

    def isRawEventDataLoggingEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'rawEventDataLoggingEnabled', False)

    def isRewardIdPrintingEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'rewardIdPrintingEnabled', False)

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

    def isWeatherEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'weatherEnabled', False)

    def isWordOfTheDayEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'wordOfTheDayEnabled', False)

    def requireAdministrator(self) -> str:
        administrator = self.__jsonContents.get('administrator')

        if not utils.isValidStr(administrator):
            raise ValueError(f'\"administrator\" in General Settings file is malformed: \"{administrator}\"')

        return administrator

    def requireDatabaseType(self) -> DatabaseType:
        databaseType = self.__jsonContents.get('databaseType')

        if not utils.isValidStr(databaseType):
            raise ValueError(f'\"databaseType\" in General Settings file is malformed: \"{databaseType}\"')

        return DatabaseType.fromStr(databaseType)

    def requireNetworkClientType(self) -> NetworkClientType:
        networkClientType = self.__jsonContents.get('networkClientType')

        if not utils.isValidStr(networkClientType):
            raise ValueError(f'\"networkClientType\" in General Settings file is malformed: \"{networkClientType}\"')

        return NetworkClientType.fromStr(networkClientType)
