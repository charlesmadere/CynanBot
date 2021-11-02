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
        return utils.getIntFromDict(jsonContents, 'raidLinkMessagingDelay')

    def getTriviaGamePoints(self) -> int:
        jsonContents = self.__readJson()
        return utils.getIntFromDict(jsonContents, 'triviaGamePoints')

    def getTriviaGameTutorialCutenessThreshold(self) -> int:
        jsonContents = self.__readJson()
        return utils.getIntFromDict(jsonContents, 'triviaGameTutorialCutenessThreshold', 25)

    def getWaitForTriviaAnswerDelay(self) -> int:
        jsonContents = self.__readJson()
        return utils.getIntFromDict(jsonContents, 'waitForTriviaAnswerDelay')

    def isCatJamMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'catJamMessageEnabled', False)

    def isChatBandEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'chatBandEnabled', False)

    def isCynanMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'cynanMessageEnabled', True)

    def isDebugLoggingEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'debugLoggingEnabled', False)

    def isDeerForceMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'deerForceMessageEnabled', False)

    def isFuntoonApiEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'funtoonApiEnabled', False)

    def isFuntoonTwitchChatFallbackEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'funtoonTwitchChatFallbackEnabled', True)

    def isJamCatMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'jamCatMessageEnabled', False)

    def isRaidLinkMessagingEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'raidLinkMessagingEnabled', False)

    def isRatJamMessageEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'ratJamMessageEnabled', False)

    def isRewardIdPrintingEnabled(self) -> bool:
        jsonContents = self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'rewardIdPrintingEnabled', False)

    def __readJson(self) -> Dict:
        if not os.path.exists(self.__generalSettingsFile):
            raise FileNotFoundError(f'General settings file not found: \"{self.__generalSettingsFile}\"')

        with open(self.__generalSettingsFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents is None:
            raise IOError(f'Error reading from general settings file: \"{self.__generalSettingsFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of general settings file \"{self.__generalSettingsFile}\" is empty')

        return jsonContents
