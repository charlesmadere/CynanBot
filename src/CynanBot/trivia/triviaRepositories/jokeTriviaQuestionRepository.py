import random
from typing import Any, Dict, List, Optional, Set

import CynanBot.misc.utils as utils
from CynanBot.misc.clearable import Clearable
from CynanBot.storage.jsonReaderInterface import JsonReaderInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import UnsupportedTriviaTypeException
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.trivia.triviaSource import TriviaSource
from CynanBot.trivia.triviaType import TriviaType


class JokeTriviaQuestionRepository(AbsTriviaQuestionRepository, Clearable):

    def __init__(
        self,
        jokeTriviaJsonReader: JsonReaderInterface,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(jokeTriviaJsonReader, JsonReaderInterface):
            raise ValueError(f'jokeTriviaJsonReader argument is malformed: \"{jokeTriviaJsonReader}\"')
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__jokeTriviaJsonReader: JsonReaderInterface = jokeTriviaJsonReader
        self.__timber: TimberInterface = timber

        self.__cache: Optional[Dict[str, Any]] = None
        self.__hasQuestionSetAvailable: Optional[bool] = None

    async def clearCaches(self):
        self.__cache = None
        self.__timber.log('JokeTriviaQuestionRepository', 'Caches cleared')

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise ValueError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('JokeTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        triviaJson = await self.__fetchTriviaQuestionJson(fetchOptions.getTwitchChannel())

        if not utils.hasItems(triviaJson):
            return None

        category = utils.getStrFromDict(triviaJson, 'category', fallback = '', clean = True)
        question = utils.getStrFromDict(triviaJson, 'question', clean = True)
        triviaDifficulty = TriviaDifficulty.fromStr(triviaJson.get('difficulty'))
        triviaId = utils.getStrFromDict(triviaJson, 'id')
        triviaType = TriviaType.fromStr(utils.getStrFromDict(triviaJson, 'type'))

        if triviaType is TriviaType.MULTIPLE_CHOICE:
            correctAnswers: List[str] = triviaJson['correctAnswers']
            multipleChoiceResponses: List[str] = triviaJson['responses']
            random.shuffle(multipleChoiceResponses)

            return MultipleChoiceTriviaQuestion(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = multipleChoiceResponses,
                category = category,
                categoryId = None,
                triviaId = triviaId,
                question = question,
                triviaDifficulty = triviaDifficulty,
                triviaSource = TriviaSource.JOKE_TRIVIA_REPOSITORY
            )
        elif triviaType is TriviaType.TRUE_FALSE:
            correctAnswers: List[bool] = triviaJson['correctAnswers']

            return TrueFalseTriviaQuestion(
                correctAnswers = correctAnswers,
                category = category,
                categoryId = None,
                triviaId = triviaId,
                question = question,
                triviaDifficulty = triviaDifficulty,
                triviaSource = TriviaSource.JOKE_TRIVIA_REPOSITORY
            )
        else:
            raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for Joke Trivia Question Repository: {triviaJson}')

    async def __fetchTriviaQuestionJson(self, twitchChannel: str) -> Optional[Dict[str, Any]]:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannel = twitchChannel.lower()
        jsonContents = await self.__readAllJson()

        triviaQuestions: List[Dict[str, Any]] = jsonContents.get('triviaQuestions')
        if not utils.hasItems(triviaQuestions):
            return None

        acceptableTriviaQuestions: List[Dict[str, Any]] = list()

        for triviaQuestion in triviaQuestions:
            compatibleWith: Optional[List[str]] = triviaQuestion.get('compatibleWith')

            if utils.hasItems(compatibleWith):
                for tc in compatibleWith:
                    if tc.lower() == twitchChannel:
                        acceptableTriviaQuestions.append(triviaQuestion)
                        break
            else:
                acceptableTriviaQuestions.append(triviaQuestion)

        if utils.hasItems(acceptableTriviaQuestions):
            return random.choice(acceptableTriviaQuestions)
        else:
            return None

    def getSupportedTriviaTypes(self) -> Set[TriviaType]:
        return { TriviaType.MULTIPLE_CHOICE, TriviaType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.JOKE_TRIVIA_REPOSITORY

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await self.__jokeTriviaJsonReader.fileExistsAsync()
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable

    async def __readAllJson(self) -> Dict[str, Any]:
        if self.__cache is not None:
            return self.__cache

        jsonContents: Optional[Dict[str, Any]] = None

        if await self.__jokeTriviaJsonReader.fileExistsAsync():
            jsonContents = await self.__jokeTriviaJsonReader.readJsonAsync()
        else:
            jsonContents = dict()

        if jsonContents is None:
            raise IOError(f'Error reading from joke trivia file: \"{self.__jokeTriviaJsonReader}\"')

        self.__cache = jsonContents
        return jsonContents
