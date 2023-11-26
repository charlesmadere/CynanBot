from typing import Any, Dict, List, Optional, Set

import aiofiles
import aiofiles.ospath
import aiosqlite
import misc.utils as utils
from timber.timberInterface import TimberInterface
from trivia.absTriviaQuestion import AbsTriviaQuestion
from trivia.multipleChoiceTriviaQuestion import MultipleChoiceTriviaQuestion
from trivia.triviaDifficulty import TriviaDifficulty
from trivia.triviaExceptions import UnsupportedTriviaTypeException
from trivia.triviaFetchOptions import TriviaFetchOptions
from trivia.triviaQuestionCompiler import TriviaQuestionCompiler
from trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from trivia.triviaSource import TriviaSource
from trivia.triviaType import TriviaType
from trivia.trueFalseTriviaQuestion import TrueFalseTriviaQuestion


class OpenTriviaQaTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaQuestionCompiler: TriviaQuestionCompiler,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaDatabaseFile: str = 'CynanBotCommon/trivia/questionSources/openTriviaQaTriviaQuestionDatabase.sqlite'
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompiler):
            raise ValueError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')
        elif not utils.isValidStr(triviaDatabaseFile):
            raise ValueError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__triviaQuestionCompiler: TriviaQuestionCompiler = triviaQuestionCompiler
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__hasQuestionSetAvailable: Optional[bool] = None

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise ValueError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('OpenTriviaQaTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('OpenTriviaQaTriviaQuestionRepository', f'{triviaDict}')

        triviaId = utils.getStrFromDict(triviaDict, 'questionId')
        triviaType = TriviaType.fromStr(utils.getStrFromDict(triviaDict, 'questionType'))

        category = utils.getStrFromDict(triviaDict, 'category')
        category = await self.__triviaQuestionCompiler.compileCategory(category)

        question = utils.getStrFromDict(triviaDict, 'question')
        question = await self.__triviaQuestionCompiler.compileQuestion(question)

        if triviaType is TriviaType.MULTIPLE_CHOICE:
            correctAnswer = utils.getStrFromDict(triviaDict, 'correctAnswer')
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(correctAnswer)

            correctAnswers: List[str] = list()
            correctAnswers.append(correctAnswer)

            responses = await self.__triviaQuestionCompiler.compileResponses(triviaDict['responses'])

            multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = responses
            )

            return MultipleChoiceTriviaQuestion(
                correctAnswers = correctAnswers,
                multipleChoiceResponses = multipleChoiceResponses,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = TriviaDifficulty.UNKNOWN,
                triviaSource = TriviaSource.OPEN_TRIVIA_QA
            )
        elif triviaType is TriviaType.TRUE_FALSE:
            correctAnswer = utils.getBoolFromDict(triviaDict, 'correctAnswer')
            correctAnswers: List[bool] = list()
            correctAnswers.append(correctAnswer)

            return TrueFalseTriviaQuestion(
                correctAnswers = correctAnswers,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = TriviaDifficulty.UNKNOWN,
                triviaSource = TriviaSource.OPEN_TRIVIA_QA
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{triviaType}\" is not supported for OpenTriviaQaTriviaQuestionRepository: {triviaDict}')

    async def __fetchTriviaQuestionDict(self) -> Dict[str, Any]:
        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'Open Trivia QA trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT correctAnswer, newCategory, question, questionId, questionType, response1, response2, response3, response4 FROM triviaQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()
        if not utils.hasItems(row) or len(row) != 9:
            raise RuntimeError(f'Received malformed data from OpenTriviaQaTriviaQuestion database: {row}')

        triviaQuestionDict: Dict[str, Any] = {
            'category': row[1],
            'correctAnswer': row[0],
            'question': row[2],
            'questionId': row[3],
            'questionType': row[4],
            'responses': [ row[5], row[6], row[7], row[8] ]
        }

        await cursor.close()
        await connection.close()
        return triviaQuestionDict

    def getSupportedTriviaTypes(self) -> Set[TriviaType]:
        return { TriviaType.MULTIPLE_CHOICE, TriviaType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.OPEN_TRIVIA_QA

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable
