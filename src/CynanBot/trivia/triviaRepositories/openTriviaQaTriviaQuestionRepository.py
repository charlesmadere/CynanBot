from typing import Any, Dict, List, Optional, Set

import aiofiles
import aiofiles.ospath
import aiosqlite

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.questions.trueFalseTriviaQuestion import \
    TrueFalseTriviaQuestion
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import UnsupportedTriviaTypeException
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class OpenTriviaQaTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaDatabaseFile: str = 'openTriviaQaTriviaQuestionDatabase.sqlite'
    ):
        super().__init__(triviaSettingsRepository)

        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface), f"malformed {triviaQuestionCompiler=}"
        if not utils.isValidStr(triviaDatabaseFile):
            raise ValueError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__hasQuestionSetAvailable: Optional[bool] = None

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        assert isinstance(fetchOptions, TriviaFetchOptions), f"malformed {fetchOptions=}"

        self.__timber.log('OpenTriviaQaTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('OpenTriviaQaTriviaQuestionRepository', f'{triviaDict}')

        triviaId = utils.getStrFromDict(triviaDict, 'questionId')
        triviaType = TriviaQuestionType.fromStr(utils.getStrFromDict(triviaDict, 'questionType'))

        category = utils.getStrFromDict(triviaDict, 'category')
        category = await self.__triviaQuestionCompiler.compileCategory(category)

        question = utils.getStrFromDict(triviaDict, 'question')
        question = await self.__triviaQuestionCompiler.compileQuestion(question)

        if triviaType is TriviaQuestionType.MULTIPLE_CHOICE:
            correctAnswer = utils.getStrFromDict(triviaDict, 'correctAnswer')
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(correctAnswer)

            correctAnswerStrings: List[str] = list()
            correctAnswerStrings.append(correctAnswer)

            responses = await self.__triviaQuestionCompiler.compileResponses(triviaDict['responses'])

            multipleChoiceResponses = await self._buildMultipleChoiceResponsesList(
                correctAnswers = correctAnswerStrings,
                multipleChoiceResponses = responses
            )

            return MultipleChoiceTriviaQuestion(
                correctAnswers = correctAnswerStrings,
                multipleChoiceResponses = multipleChoiceResponses,
                category = category,
                categoryId = None,
                question = question,
                triviaId = triviaId,
                triviaDifficulty = TriviaDifficulty.UNKNOWN,
                triviaSource = TriviaSource.OPEN_TRIVIA_QA
            )
        elif triviaType is TriviaQuestionType.TRUE_FALSE:
            correctAnswer = utils.getBoolFromDict(triviaDict, 'correctAnswer')
            correctAnswerBools: List[bool] = list()
            correctAnswerBools.append(correctAnswer)

            return TrueFalseTriviaQuestion(
                correctAnswers = correctAnswerBools,
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

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE, TriviaQuestionType.TRUE_FALSE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.OPEN_TRIVIA_QA

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable
