import json
import random
from typing import Any, Dict, List, Optional, Set

import aiofiles
import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import UnsupportedTriviaTypeException
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.trivia.triviaSource import TriviaSource
from CynanBot.trivia.triviaType import TriviaType
from CynanBot.trivia.trueFalseTriviaQuestion import TrueFalseTriviaQuestion


class JokeTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        jokeTriviaQuestionFile: str = 'CynanBotCommon/trivia/questionSources/jokeTriviaQuestionRepository.json'
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(jokeTriviaQuestionFile):
            raise ValueError(f'jokeTriviaQuestionFile argument is malformed: \"{jokeTriviaQuestionFile}\"')

        self.__timber: TimberInterface = timber
        self.__triviaDatabaseFile: str = jokeTriviaQuestionFile

        self.__hasQuestionSetAvailable: Optional[bool] = None

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

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable

    async def __readAllJson(self) -> Dict[str, Any]:
        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'Joke trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        async with aiofiles.open(self.__triviaDatabaseFile, mode = 'r', encoding = 'utf-8') as file:
            data = await file.read()
            jsonContents = json.loads(data)

        if jsonContents is None:
            raise IOError(f'Error reading from joke trivia file: \"{self.__triviaDatabaseFile}\"')

        return jsonContents
