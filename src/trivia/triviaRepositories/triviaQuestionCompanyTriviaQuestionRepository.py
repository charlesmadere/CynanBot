from typing import Any

import aiofiles
import aiofiles.ospath
import aiosqlite
from ...timber.timberInterface import TimberInterface
from ..compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.multipleChoiceTriviaQuestion import \
    MultipleChoiceTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaExceptions import UnsupportedTriviaTypeException
from ..triviaFetchOptions import TriviaFetchOptions
from .absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from ..triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from ...misc import utils as utils


class TriviaQuestionCompanyTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaDatabaseFile: str = 'triviaQuestionCompanyTriviaQuestionRepository.sqlite'
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')
        elif not utils.isValidStr(triviaDatabaseFile):
            raise TypeError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__hasQuestionSetAvailable: bool | None = None

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise ValueError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('TriviaQuestionCompanyTriviaQuestionRepository', f'Fetching trivia question... ({fetchOptions=})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('TriviaQuestionCompanyTriviaQuestionRepository', f'{triviaDict}')

        difficulty = TriviaDifficulty.fromInt(utils.getIntFromDict(triviaDict, 'difficulty'))
        questionId = utils.getStrFromDict(triviaDict, 'questionId')
        questionType = TriviaQuestionType.fromStr(utils.getStrFromDict(triviaDict, 'questionType'))

        category = await self.__triviaQuestionCompiler.compileCategory(utils.getStrFromDict(triviaDict, 'category'))
        question = await self.__triviaQuestionCompiler.compileQuestion(utils.getStrFromDict(triviaDict, 'question'))

        if questionType is TriviaQuestionType.MULTIPLE_CHOICE:
            responses: list[str] = triviaDict['responses']
            correctAnswer: str = responses[utils.getIntFromDict(triviaDict, 'correctAnswerIndex')]
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(correctAnswer)
            correctAnswers: list[str] = list()
            correctAnswers.append(correctAnswer)

            responses = await self.__triviaQuestionCompiler.compileResponses(responses)

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
                triviaId = questionId,
                triviaDifficulty = difficulty,
                originalTriviaSource = None,
                triviaSource = self.getTriviaSource()
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{questionType}\" is not supported for {self.getTriviaSource()}: {triviaDict}')

    async def __fetchTriviaQuestionDict(self) -> dict[str, Any]:
        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'Trivia Question Company trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT category, correctAnswerIndex, difficulty, question, questionId, questionType, response0, response1, response2, response3 FROM tqcQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()
        if not utils.hasItems(row) or len(row) != 10:
            raise RuntimeError(f'Received malformed data from {self.getTriviaSource()} database: {row}')

        questionDict: dict[str, Any] = {
            'category': row[0],
            'correctAnswerIndex': row[1],
            'difficulty': row[2],
            'question': row[3],
            'questionId': row[4],
            'questionType': row[5],
            'responses': [ row[6], row[7], row[8], row[9] ]
        }

        await cursor.close()
        await connection.close()
        return questionDict

    def getSupportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.THE_QUESTION_CO

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable
