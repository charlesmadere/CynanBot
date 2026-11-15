from typing import Any, Final

from . import utils as utils
from ..soundPlayerManager.jsonMapper.soundPlayerJsonMapperInterface import SoundPlayerJsonMapperInterface
from ..soundPlayerManager.soundPlayerType import SoundPlayerType


class GeneralSettingsRepositorySnapshot:

    def __init__(
        self,
        jsonContents: dict[str, Any],
        soundPlayerJsonMapper: SoundPlayerJsonMapperInterface,
        defaultSoundPlayerType: SoundPlayerType,
    ):
        if not isinstance(jsonContents, dict):
            raise TypeError(f'jsonContents argument is malformed: \"{jsonContents}\"')
        elif not isinstance(soundPlayerJsonMapper, SoundPlayerJsonMapperInterface):
            raise TypeError(f'soundPlayerJsonMapper argument is malformed: \"{soundPlayerJsonMapper}\"')
        elif not isinstance(defaultSoundPlayerType, SoundPlayerType):
            raise TypeError(f'defaultSoundPlayerType argument is malformed: \"{defaultSoundPlayerType}\"')

        self.__jsonContents: Final[dict[str, Any]] = jsonContents
        self.__soundPlayerJsonMapper: Final[SoundPlayerJsonMapperInterface] = soundPlayerJsonMapper
        self.__defaultSoundPlayerType: Final[SoundPlayerType] = defaultSoundPlayerType

    def getSuperTriviaGamePoints(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGamePoints', 25)

    def getSuperTriviaGameShinyMultiplier(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGameShinyMultiplier', 3)

    def getSuperTriviaGameToxicMultiplier(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGameToxicMultiplier', 2)

    def getSuperTriviaGamePerUserAttempts(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGamePerUserAttempts', 2)

    def getSuperTriviaGameToxicPunishmentMultiplier(self) -> int:
        return utils.getIntFromDict(self.__jsonContents, 'superTriviaGameToxicPunishmentMultiplier', 1)

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

    def isFuntoonApiEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'funtoonApiEnabled', True)

    def isFuntoonTwitchChatFallbackEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'funtoonTwitchChatFallbackEnabled', True)

    def isJishoEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'jishoEnabled', True)

    def isPokepediaEnabled(self) -> bool:
        return utils.getBoolFromDict(self.__jsonContents, 'pokepediaEnabled', True)

    def requireAdministrator(self) -> str:
        administrator = self.__jsonContents.get('administrator')

        if not utils.isValidStr(administrator):
            raise ValueError(f'\"administrator\" in General Settings file is malformed: \"{administrator}\"')

        return administrator

    def requireSoundPlayerType(self) -> SoundPlayerType:
        soundPlayerType = self.__jsonContents.get('soundPlayerType')

        if utils.isValidStr(soundPlayerType):
            return self.__soundPlayerJsonMapper.parseSoundPlayerType(soundPlayerType)
        else:
            return self.__defaultSoundPlayerType
