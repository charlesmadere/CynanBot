from typing import Any, Dict, List, Optional, Set

import aiofiles
import aiofiles.ospath
import aiosqlite

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBot.trivia.compilers.triviaAnswerCompilerInterface import \
    TriviaAnswerCompilerInterface
from CynanBot.trivia.compilers.triviaQuestionCompilerInterface import \
    TriviaQuestionCompilerInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaDifficulty import TriviaDifficulty
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class LotrTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaDatabaseFile: str = 'lotrTriviaQuestionsDatabase.sqlite'
    ):
        super().__init__(triviaSettingsRepository)

        assert isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface), f"malformed {additionalTriviaAnswersRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface), f"malformed {triviaAnswerCompiler=}"
        assert isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface), f"malformed {triviaQuestionCompiler=}"
        if not utils.isValidStr(triviaDatabaseFile):
            raise ValueError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__timber: TimberInterface = timber
        self.__triviaAnswerCompiler: TriviaAnswerCompilerInterface = triviaAnswerCompiler
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__hasQuestionSetAvailable: Optional[bool] = None

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        assert isinstance(fetchOptions, TriviaFetchOptions), f"malformed {fetchOptions=}"

        self.__timber.log('LotrTriviaQuestionRepository', f'Fetching trivia question... (fetchOptions={fetchOptions})')

        triviaDict = await self.__fetchTriviaQuestionDict()

        if await self._triviaSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('LotrTriviaQuestionRepository', f'{triviaDict}')

        question = utils.getStrFromDict(triviaDict, 'question')
        question = await self.__triviaQuestionCompiler.compileQuestion(question)

        triviaId = utils.getStrFromDict(triviaDict, 'triviaId')

        correctAnswers: List[str] = list()
        correctAnswers.extend(triviaDict['correctAnswers'])

        if await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = correctAnswers,
            triviaId = triviaId,
            triviaSource = self.getTriviaSource(),
            triviaType = TriviaQuestionType.QUESTION_ANSWER
        ):
            self.__timber.log('LotrTriviaQuestionRepository', f'Added additional answers to question (triviaId=\"{triviaId}\")')

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(correctAnswers)

        cleanedCorrectAnswers: List[str] = list()
        cleanedCorrectAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(correctAnswers)

        expandedCorrectAnswers: Set[str] = set()
        for answer in cleanedCorrectAnswers:
            expandedCorrectAnswers.update(await self.__triviaAnswerCompiler.expandNumerals(answer))

        return QuestionAnswerTriviaQuestion(
            correctAnswers = correctAnswers,
            cleanedCorrectAnswers = list(expandedCorrectAnswers),
            category = 'Lord of the Rings',
            categoryId = None,
            question = question,
            triviaId = triviaId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            triviaSource = TriviaSource.LORD_OF_THE_RINGS
        )

    async def __fetchTriviaQuestionDict(self) -> Dict[str, Any]:
        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'LOTR trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT answerA, answerB, answerC, answerD, question, triviaId FROM lotrQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        row = await cursor.fetchone()
        if not utils.hasItems(row) or len(row) != 6:
            raise RuntimeError(f'Received malformed data from LOTR database: {row}')

        correctAnswers: List[str] = list()
        self.__selectiveAppend(correctAnswers, row[0])
        self.__selectiveAppend(correctAnswers, row[1])
        self.__selectiveAppend(correctAnswers, row[2])
        self.__selectiveAppend(correctAnswers, row[3])

        if not utils.hasItems(correctAnswers):
            raise RuntimeError(f'Received malformed correct answer data from LOTR database: {row}')

        triviaQuestionDict: Dict[str, Any] = {
            'correctAnswers': correctAnswers,
            'question': row[4],
            'triviaId': row[5]
        }

        await cursor.close()
        await connection.close()
        return triviaQuestionDict

    def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return { TriviaQuestionType.QUESTION_ANSWER }

    def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.LORD_OF_THE_RINGS

    async def hasQuestionSetAvailable(self) -> bool:
        if self.__hasQuestionSetAvailable is not None:
            return self.__hasQuestionSetAvailable

        hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
        self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable

    def __selectiveAppend(self, correctAnswers: List[str], correctAnswer: Optional[str]):
        if correctAnswers is None:
            raise ValueError(f'correctAnswers argument is malformed: \"{correctAnswers}\"')

        if utils.isValidStr(correctAnswer):
            correctAnswers.append(correctAnswer)
