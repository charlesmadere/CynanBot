from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TriviaSettingsRepository(TriviaSettingsRepositoryInterface):

    def __init__(self, settingsJsonReader: JsonReaderInterface):
        assert isinstance(settingsJsonReader, JsonReaderInterface), f"malformed {settingsJsonReader=}"

        self.__settingsJsonReader: JsonReaderInterface = settingsJsonReader

        self.__cache: Optional[Dict[str, Any]] = None

    async def areAdditionalTriviaAnswersEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'additional_trivia_answers_enabled', True)

    async def areShinyTriviasEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'shiny_trivias_enabled', True)

    async def areToxicTriviasEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'toxic_trivias_enabled', True)

    async def clearCaches(self):
        self.__cache = None

    async def getAvailableTriviaSourcesAndWeights(self) -> Dict[TriviaSource, int]:
        jsonContents = await self.__readJson()

        triviaSourcesJson: Dict[str, Any] = jsonContents['trivia_sources']
        if not utils.hasItems(triviaSourcesJson):
            raise RuntimeError(f'\"trivia_sources\" field is malformed: \"{triviaSourcesJson}\"')

        triviaSources: Dict[TriviaSource, int] = dict()

        for key, triviaSourceJson in triviaSourcesJson.items():
            triviaSource = TriviaSource.fromStr(key)

            isEnabled = utils.getBoolFromDict(triviaSourceJson, 'is_enabled', False)
            if not isEnabled:
                continue

            weight = utils.getIntFromDict(triviaSourceJson, 'weight', 1)
            if weight < 1:
                raise ValueError(f'triviaSource \"{triviaSource}\" has an invalid weight: \"{weight}\"')

            triviaSources[triviaSource] = weight

        if not utils.hasItems(triviaSources):
            raise RuntimeError(f'triviaSources is empty: \"{triviaSources}\"')

        return triviaSources

    async def getLevenshteinThresholdGrowthRate(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'levenshtein_threshold_growth_rate', 7)

    async def getMaxAdditionalTriviaAnswerLength(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_additional_trivia_answer_length', 48)

    async def getMaxAdditionalTriviaAnswers(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_additional_trivia_answers', 5)

    async def getMaxAnswerLength(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_answer_length', 80)

    async def getMaxMultipleChoiceResponses(self) -> int:
        jsonContents = await self.__readJson()
        maxMultipleChoiceResponses = utils.getIntFromDict(jsonContents, 'max_multiple_choice_responses', 6)
        minMultipleChoiceResponses = utils.getIntFromDict(jsonContents, 'min_multiple_choice_responses', 2)

        if minMultipleChoiceResponses < 2 or minMultipleChoiceResponses > utils.getIntMaxSafeSize():
            raise ValueError(f'\"min_multiple_choice_responses\" is out of bounds: {minMultipleChoiceResponses}')
        if maxMultipleChoiceResponses < minMultipleChoiceResponses:
            raise ValueError(f'\"min_multiple_choice_responses\" ({minMultipleChoiceResponses}) is less than \"max_multiple_choice_responses\" ({maxMultipleChoiceResponses})')

        return maxMultipleChoiceResponses

    async def getMaxQuestionLength(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_question_length', 200)

    async def getMaxPhraseAnswerLength(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_phrase_answer_length', 32)

    async def getMaxPhraseGuessLength(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_phrase_guess_length', 40)

    async def getMaxSuperTriviaQuestionSpoolSize(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_super_trivia_question_spool_size', 5)

    async def getMaxTriviaQuestionSpoolSize(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_trivia_question_spool_size', 5)

    async def getMaxRetryCount(self) -> int:
        jsonContents = await self.__readJson()
        maxRetryCount = utils.getIntFromDict(jsonContents, 'max_retry_count', 5)

        if maxRetryCount < 2:
            raise ValueError(f'max_retry_count is too small: \"{maxRetryCount}\"')

        return maxRetryCount

    async def getMaxSuperTriviaGameQueueSize(self) -> int:
        jsonContents = await self.__readJson()
        maxSuperGameQueueSize = utils.getIntFromDict(jsonContents, 'max_super_game_queue_size', 50)

        if maxSuperGameQueueSize < -1:
            raise ValueError(f'max_super_game_queue_size is too small: \"{maxSuperGameQueueSize}\"')

        return maxSuperGameQueueSize

    async def getMinDaysBeforeRepeatQuestion(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'min_days_before_repeat_question', 10)

    async def getMinMultipleChoiceResponses(self) -> int:
        jsonContents = await self.__readJson()
        maxMultipleChoiceResponses = utils.getIntFromDict(jsonContents, 'max_multiple_choice_responses', 6)
        minMultipleChoiceResponses = utils.getIntFromDict(jsonContents, 'min_multiple_choice_responses', 2)

        if minMultipleChoiceResponses < 2 or minMultipleChoiceResponses > utils.getIntMaxSafeSize():
            raise ValueError(f'\"min_multiple_choice_responses\" is out of bounds: {minMultipleChoiceResponses}')
        if maxMultipleChoiceResponses < minMultipleChoiceResponses:
            raise ValueError(f'\"min_multiple_choice_responses\" ({minMultipleChoiceResponses}) is less than \"max_multiple_choice_responses\" ({maxMultipleChoiceResponses})')

        return minMultipleChoiceResponses

    async def getShinyProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'shiny_probability', 0.03)

    async def getSuperTriviaCooldownSeconds(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'super_trivia_cooldown_seconds', 8)

    async def getSuperTriviaFirstQuestionDelaySeconds(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'super_trivia_first_question_delay_seconds', 4)

    async def getToxicProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'toxic_probability', 0.03)

    async def getTriviaSourceInstabilityThreshold(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'trivia_source_instability_threshold', 3)

    async def isBanListEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'is_ban_list_enabled', True)

    async def isDebugLoggingEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'debug_logging_enabled', True)

    async def __readJson(self) -> Dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: Optional[Dict[str, Any]] = None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from trivia settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents
