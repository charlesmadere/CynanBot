import json
import os
from typing import Dict

import CynanBotCommon.utils as utils


class GeneralSettingsRepository():

    def __init__(
        self,
        generalSettingsFile: str = 'generalSettingsRepository.json'
    ):
        if not utils.isValidStr(generalSettingsFile):
            raise ValueError(f'generalSettingsFile argument is malformed: \"{generalSettingsFile}\"')

        self.__generalSettingsFile: str = generalSettingsFile

    def getRaidLinkMessagingDelay(self) -> int:
        jsonContents = self.__readJson()
        return utils.getIntFromDict(jsonContents, 'raidLinkMessagingDelay', 60)

    def getRefreshPubSubTokensSeconds(self) -> int:
        jsonContents = self.__readJson()

        refreshPubSubTokensSeconds = utils.getIntFromDict(jsonContents, 'refreshPubSubTokensSeconds', 120)
        if refreshPubSubTokensSeconds < 30:
            raise ValueError(f'\"refreshPubSubTokensSeconds\" value is too aggressive: {refreshPubSubTokensSeconds}')

        return refreshPubSubTokensSeconds

    def getSuperTriviaGameMultiplier(self) -> int:
        jsonContents = self.__readJson()
        return utils.getIntFromDict(jsonContents, 'superTriviaGameMultiplier', 5)

    def getTriviaGamePoints(self) -> int:
        jsonContents = self.__readJson()
        return utils.getIntFromDict(jsonContents, 'triviaGamePoints', 5)

    def getTriviaGameTutorialCutenessThreshold(self) -> int:
        jsonContents = self.__readJson()
        return utils.getIntFromDict(jsonContents, 'triviaGameTutorialCutenessThreshold', 10)

    def getWaitForTriviaAnswerDelay(self) -> int:
        jsonContents = self.__readJson()
        return utils.getIntFromDict(jsonContents, 'waitForTriviaAnswerDelay', 45)

    def isAnalogueEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'analogueEnabled', True)

    def isCatJamMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'catJamMessageEnabled', True)

    def isChatBandEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'chatBandEnabled', False)

    def isCynanMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'cynanMessageEnabled', False)

    def isDebugLoggingEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'debugLoggingEnabled', True)

    def isDeerForceMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'deerForceMessageEnabled', False)

    def isEyesMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'eyesMessageEnabled', False)

    def isFuntoonApiEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'funtoonApiEnabled', True)

    def isFuntoonTwitchChatFallbackEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'funtoonTwitchChatFallbackEnabled', True)

    def isGiftSubscriptionThanksMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'giftSubscriptionThanksMessageEnabled', True)

    def isImytSlurpMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'imytSlurpMessageEnabled', False)

    def isJamCatMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'jamCatMessageEnabled', False)

    def isJishoEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'jishoEnabled', True)

    def isPersistAllUsersEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'persistAllUsersEnabled', False)

    def isPokepediaEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'pokepediaEnabled', True)

    def isRaidLinkMessagingEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'raidLinkMessagingEnabled', True)

    def isRatJamMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'ratJamMessageEnabled', False)

    def isRewardIdPrintingEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'rewardIdPrintingEnabled', False)

    def isSubGiftThankingEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'subGiftThankingEnabled', True)

    def isTamalesEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'tamalesEnabled', True)

    def isTranslateEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'translateEnabled', True)

    def isTriviaEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'triviaEnabled', True)

    def isTriviaGameEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'triviaGameEnabled', True)

    def isWeatherEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'weatherEnabled', True)

    def isWordOfTheDayEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'wordOfTheDayEnabled', True)

    def __readJson(self) -> Dict[str, object]:
        if not os.path.exists(self.__generalSettingsFile):
            raise FileNotFoundError(f'General settings file not found: \"{self.__generalSettingsFile}\"')

        with open(self.__generalSettingsFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from general settings file: \"{self.__generalSettingsFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of general settings file \"{self.__generalSettingsFile}\" is empty')

        return jsonContents
