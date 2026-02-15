from typing import Any, Final

from frozendict import frozendict

from ..misc.triviaSourceParserInterface import TriviaSourceParserInterface
from ..questions.triviaSource import TriviaSource
from ..settings.triviaSettingsInterface import TriviaSettingsInterface
from ..settings.triviaSourceAndProperties import TriviaSourceAndProperties
from ...misc import utils as utils
from ...storage.jsonReaderInterface import JsonReaderInterface


class TriviaSettings(TriviaSettingsInterface):

    def __init__(
        self,
        settingsJsonReader: JsonReaderInterface,
        triviaSourceParser: TriviaSourceParserInterface,
    ):
        if not isinstance(settingsJsonReader, JsonReaderInterface):
            raise TypeError(f'settingsJsonReader argument is malformed: \"{settingsJsonReader}\"')
        elif not isinstance(triviaSourceParser, TriviaSourceParserInterface):
            raise TypeError(f'triviaSourceParser argument is malformed: \"{triviaSourceParser}\"')

        self.__settingsJsonReader: Final[JsonReaderInterface] = settingsJsonReader
        self.__triviaSourceParser: Final[TriviaSourceParserInterface] = triviaSourceParser

        self.__cache: dict[str, Any] | None = None
        self.__cachedTriviaSourcesAndProperties: frozendict[TriviaSource, TriviaSourceAndProperties] | None = None

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
        self.__cachedTriviaSourcesAndProperties = None

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
            raise ValueError(f'\"min_multiple_choice_responses\" is out of bounds: ({minMultipleChoiceResponses=})')
        elif maxMultipleChoiceResponses < minMultipleChoiceResponses:
            raise ValueError(f'\"min_multiple_choice_responses\" is less than \"max_multiple_choice_responses\" ({minMultipleChoiceResponses=}) ({maxMultipleChoiceResponses=})')

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
        return utils.getIntFromDict(jsonContents, 'max_super_trivia_question_spool_size', 8)

    async def getMaxTriviaQuestionSpoolSize(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_trivia_question_spool_size', 8)

    async def getMaxRetryCount(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'max_retry_count', 5)

    async def getMaxSuperTriviaGameQueueSize(self) -> int:
        jsonContents = await self.__readJson()

        return utils.getIntFromDict(
            d = jsonContents,
            key = 'max_super_game_queue_size',
            fallback = 32
        )

    async def getMinDaysBeforeRepeatQuestion(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'min_days_before_repeat_question', 10)

    async def getMinMultipleChoiceResponses(self) -> int:
        jsonContents = await self.__readJson()
        maxMultipleChoiceResponses = utils.getIntFromDict(jsonContents, 'max_multiple_choice_responses', 6)
        minMultipleChoiceResponses = utils.getIntFromDict(jsonContents, 'min_multiple_choice_responses', 2)

        if minMultipleChoiceResponses < 2 or minMultipleChoiceResponses > utils.getIntMaxSafeSize():
            raise ValueError(f'\"min_multiple_choice_responses\" is out of bounds: {minMultipleChoiceResponses}')
        elif maxMultipleChoiceResponses < minMultipleChoiceResponses:
            raise ValueError(f'\"min_multiple_choice_responses\" ({minMultipleChoiceResponses}) is less than \"max_multiple_choice_responses\" ({maxMultipleChoiceResponses})')

        return minMultipleChoiceResponses

    async def getShinyProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'shiny_probability', 0.05)

    async def getSuperTriviaCooldownSeconds(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'super_trivia_cooldown_seconds', 8)

    async def getSuperTriviaFirstQuestionDelaySeconds(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'super_trivia_first_question_delay_seconds', 4)

    async def getToxicProbability(self) -> float:
        jsonContents = await self.__readJson()
        return utils.getFloatFromDict(jsonContents, 'toxic_probability', 0.01)

    async def getTriviaSourcesAndProperties(self) -> frozendict[TriviaSource, TriviaSourceAndProperties]:
        cachedTriviaSourcesAndProperties = self.__cachedTriviaSourcesAndProperties

        if cachedTriviaSourcesAndProperties is not None:
            return cachedTriviaSourcesAndProperties

        jsonContents = await self.__readJson()
        triviaSourcesJson: dict[str, Any] | Any | None = jsonContents.get('trivia_sources', None)
        triviaSourcesAndProperties: dict[TriviaSource, TriviaSourceAndProperties] = dict()

        if not isinstance(triviaSourcesJson, dict) or len(triviaSourcesJson) == 0:
            frozenTriviaSourcesAndProperties = frozendict(triviaSourcesAndProperties)
            self.__cachedTriviaSourcesAndProperties = frozenTriviaSourcesAndProperties
            return frozenTriviaSourcesAndProperties

        for key, triviaSourceJson in triviaSourcesJson.items():
            triviaSource = await self.__triviaSourceParser.parse(key)
            isEnabled = utils.getBoolFromDict(triviaSourceJson, 'is_enabled', False)
            weight = utils.getIntFromDict(triviaSourceJson, 'weight', 1)

            if weight < 1 or weight > utils.getIntMaxSafeSize():
                raise ValueError(f'TriviaSource weight value is out of bounds ({triviaSourceJson=}) ({weight=})')

            triviaSourcesAndProperties[triviaSource] = TriviaSourceAndProperties(
                isEnabled = isEnabled,
                weight = weight,
                triviaSource = triviaSource,
            )

        frozenTriviaSourcesAndProperties = frozendict(triviaSourcesAndProperties)
        self.__cachedTriviaSourcesAndProperties = frozenTriviaSourcesAndProperties
        return frozenTriviaSourcesAndProperties

    async def getTriviaSourceInstabilityThreshold(self) -> int:
        jsonContents = await self.__readJson()
        return utils.getIntFromDict(jsonContents, 'trivia_source_instability_threshold', 3)

    async def isBanListEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'is_ban_list_enabled', True)

    async def isDebugLoggingEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'debug_logging_enabled', True)

    async def isEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'is_enabled', True)

    async def isScraperEnabled(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'scraper_enabled', True)

    async def __readJson(self) -> dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: dict[str, Any] | None

        if await self.__settingsJsonReader.fileExistsAsync():
            jsonContents = await self.__settingsJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if not isinstance(jsonContents, dict):
            raise IOError(f'Error reading from Trivia settings file: {self.__settingsJsonReader}')

        self.__cache = jsonContents
        return jsonContents

    async def useNewAnswerCheckingMethod(self) -> bool:
        jsonContents = await self.__readJson()
        return utils.getBoolFromDict(jsonContents, 'use_new_answer_checking_method', True)
