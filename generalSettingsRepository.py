import json
import os
from typing import Dict, List

import aiofile

import CynanBotCommon.utils as utils
from persistence.generalSettingsSnapshot import GeneralSettingsSnapshot


class GeneralSettingsRepository():

    def __init__(
        self,
        generalSettingsFile: str = 'generalSettingsRepository.json'
    ):
        if not utils.isValidStr(generalSettingsFile):
            raise ValueError(f'generalSettingsFile argument is malformed: \"{generalSettingsFile}\"')

        self.__generalSettingsFile: str = generalSettingsFile

    def getAll(self) -> GeneralSettingsSnapshot:
        jsonContents = self.__readJson()
        return GeneralSettingsSnapshot(jsonContents)

    async def getAllAsync(self) -> GeneralSettingsSnapshot:
        jsonContents = await self.__readJsonAsync()
        return GeneralSettingsSnapshot(jsonContents)

    def getEventSubPort(self) -> int:
        snapshot = self.getAll()
        return snapshot.getEventSubPort()

    def getGlobalSuperTriviaGameControllers(self) -> List[str]:
        snapshot = self.getAll()
        return snapshot.getGlobalSuperTriviaGameControllers()

    def getRaidLinkMessagingDelay(self) -> int:
        snapshot = self.getAll()
        return snapshot.getRaidLinkMessagingDelay()

    def getRefreshPubSubTokensSeconds(self) -> int:
        snapshot = self.getAll()
        return snapshot.getRefreshPubSubTokensSeconds()

    def getSuperTriviaGameMultiplier(self) -> int:
        snapshot = self.getAll()
        return snapshot.getSuperTriviaGameMultiplier()

    def getSuperTriviaGamePerUserAttempts(self) -> int:
        snapshot = self.getAll()
        return snapshot.getSuperTriviaGamePerUserAttempts()

    def getTriviaGamePoints(self) -> int:
        snapshot = self.getAll()
        return snapshot.getTriviaGamePoints()

    def getTriviaGameTutorialCutenessThreshold(self) -> int:
        snapshot = self.getAll()
        return snapshot.getTriviaGameTutorialCutenessThreshold()

    def getWaitForSuperTriviaAnswerDelay(self) -> int:
        snapshot = self.getAll()
        return snapshot.getWaitForSuperTriviaAnswerDelay()

    def getWaitForTriviaAnswerDelay(self) -> int:
        snapshot = self.getAll()
        return snapshot.getWaitForTriviaAnswerDelay()

    def isAnalogueEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isAnalogueEnabled()

    def isCatJamMessageEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isCatJamMessageEnabled()

    def isChatBandEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isChatBandEnabled()

    def isCynanMessageEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isCynanMessageEnabled()

    def isDebugLoggingEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isDebugLoggingEnabled()

    def isDeerForceMessageEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isDeerForceMessageEnabled()

    def isEventSubEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isEventSubEnabled()

    def isEyesMessageEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isEyesMessageEnabled()

    def isFuntoonApiEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isFuntoonApiEnabled()

    def isFuntoonTwitchChatFallbackEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isFuntoonTwitchChatFallbackEnabled()

    def isGiftSubscriptionThanksMessageEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isGiftSubscriptionThanksMessageEnabled()

    def isImytSlurpMessageEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isImytSlurpMessageEnabled()

    def isJamCatMessageEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isJamCatMessageEnabled()

    def isJishoEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isJishoEnabled()

    def isPersistAllUsersEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isPersistAllUsersEnabled()

    def isPokepediaEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isPokepediaEnabled()

    def isPubSubEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isPubSubEnabled()

    def isPubSubPongLoggingEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isPubSubPongLoggingEnabled()

    def isRaidLinkMessagingEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isRaidLinkMessagingEnabled()

    def isRatJamMessageEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isRatJamMessageEnabled()

    def isRewardIdPrintingEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isRewardIdPrintingEnabled()

    def isSubGiftThankingEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isSubGiftThankingEnabled()

    def isSuperTriviaGameEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isSuperTriviaGameEnabled()

    def isTamalesEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isTamalesEnabled()

    def isTranslateEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isTranslateEnabled()

    def isTriviaEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isTriviaEnabled()

    def isTriviaGameEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isTriviaGameEnabled()

    def isWeatherEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isWeatherEnabled()

    def isWordOfTheDayEnabled(self) -> bool:
        snapshot = self.getAll()
        return snapshot.isWordOfTheDayEnabled()

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

    async def __readJsonAsync(self) -> Dict[str, object]:
        if not os.path.exists(self.__generalSettingsFile):
            raise FileNotFoundError(f'General settings file not found: \"{self.__generalSettingsFile}\"')

        async with aiofile.async_open(self.__generalSettingsFile, 'r') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from general settings file: \"{self.__generalSettingsFile}\"')
        elif len(jsonContents) == 0:
            raise ValueError(f'JSON contents of general settings file \"{self.__generalSettingsFile}\" is empty')

        return jsonContents
