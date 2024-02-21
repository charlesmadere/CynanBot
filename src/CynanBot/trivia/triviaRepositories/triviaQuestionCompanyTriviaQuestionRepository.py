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
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaExceptions import UnsupportedTriviaTypeException
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class TriviaQuestionCompanyTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        timber: TimberInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaDatabaseFile: str = 'triviaQuestionCompanyTriviaQuestionRepository.sqlite'
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

        self.__timber.log('TriviaQuestionCompanyTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('TriviaQuestionCompanyTriviaQuestionRepository', f'{triviaDict}')

        difficulty = TriviaDifficulty.fromInt(utils.getIntFromDict(triviaDict, 'difficulty'))
        questionId = utils.getStrFromDict(triviaDict, 'questionId')
        questionType = TriviaQuestionType.fromStr(utils.getStrFromDict(triviaDict, 'questionType'))

        category = await self.__triviaQuestionCompiler.compileCategory(utils.getStrFromDict(triviaDict, 'category'))
        question = await self.__triviaQuestionCompiler.compileQuestion(utils.getStrFromDict(triviaDict, 'question'))

        if questionType is TriviaQuestionType.MULTIPLE_CHOICE:
            responses: List[str] = triviaDict['responses']
            correctAnswer: str = responses[utils.getIntFromDict(triviaDict, 'correctAnswerIndex')]
            correctAnswer = await self.__triviaQuestionCompiler.compileResponse(correctAnswer)
            correctAnswers: List[str] = list()
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
                triviaSource = self.getTriviaSource()
            )

        raise UnsupportedTriviaTypeException(f'triviaType \"{questionType}\" is not supported for {self.getTriviaSource()}: {triviaDict}')

    async def __fetchTriviaQuestionDict(self) -> Dict[str, Any]:
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

        questionDict: Dict[str, Any] = {
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

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.MULTIPLE_CHOICE }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.THE_QUESTION_CO

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable
