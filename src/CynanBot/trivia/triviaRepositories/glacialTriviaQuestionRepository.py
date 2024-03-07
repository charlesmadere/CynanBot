from typing import Optional, Set

import aiofiles
import aiofiles.ospath
import aiosqlite

import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.absTriviaQuestionRepository import \
    AbsTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.glacialTriviaQuestionRepositoryInterface import \
    GlacialTriviaQuestionRepositoryInterface
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface


class GlacialTriviaQuestionRepository(
    AbsTriviaQuestionRepository,
    GlacialTriviaQuestionRepositoryInterface
):

    def __init__(
        self,
        timber: TimberInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaDatabaseFile: str = 'glacialTriviaQuestionsDatabase.sqlite'
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(triviaDatabaseFile):
            raise TypeError(f'triviaDatabaseFile argument is malformed: \"{triviaDatabaseFile}\"')

        self.__timber: TimberInterface = timber
        self.__triviaDatabaseFile: str = triviaDatabaseFile

        self.__hasQuestionSetAvailable: Optional[bool] = None

    async def __fetchAnyTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions
    ) -> Optional[AbsTriviaQuestion]:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        # TODO
        raise RuntimeError('not implemented')

    async def __fetchMultipleChoiceOrTrueFalseTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions
    ) -> Optional[AbsTriviaQuestion]:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        # TODO
        raise RuntimeError('not implemented')

    async def __fetchQuestionAnswerTriviaQuestion(
        self,
        fetchOptions: TriviaFetchOptions
    ) -> Optional[QuestionAnswerTriviaQuestion]:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        connection = await aiosqlite.connect(self.__triviaDatabaseFile)
        cursor = await connection.execute(
            '''
                SELECT answerA, answerB, answerC, answerD, answerE, answerF, correctAnswer, question, triviaDifficulty, triviaId, triviaType FROM glacialQuestions
                ORDER BY RANDOM()
                LIMIT 1
            '''
        )

        # TODO

        await cursor.close()
        await connection.close()

        raise RuntimeError('not implemented')

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        if not await aiofiles.ospath.exists(self.__triviaDatabaseFile):
            raise FileNotFoundError(f'Glacial trivia database file not found: \"{self.__triviaDatabaseFile}\"')

        question: Optional[AbsTriviaQuestion] = None

        if fetchOptions.requireQuestionAnswerTriviaQuestion():
            question = await self.__fetchQuestionAnswerTriviaQuestion(fetchOptions)
        elif fetchOptions.areQuestionAnswerTriviaQuestionsEnabled():
            question = await self.__fetchAnyTriviaQuestion(fetchOptions)
        else:
            question = await self.__fetchMultipleChoiceOrTrueFalseTriviaQuestion(fetchOptions)

        if question is None:
            raise RuntimeError('not yet implemented')

        return question

    async def getSupportedTriviaTypes(self) -> Set[TriviaQuestionType]:
        return {
            TriviaQuestionType.MULTIPLE_CHOICE,
            TriviaQuestionType.QUESTION_ANSWER,
            TriviaQuestionType.TRUE_FALSE
        }

    async def getTriviaSource(self) -> TriviaSource:
        return TriviaSource.GLACIAL

    async def hasQuestionSetAvailable(self) -> bool:
        hasQuestionSetAvailable = self.__hasQuestionSetAvailable

        if hasQuestionSetAvailable is None:
            hasQuestionSetAvailable = await aiofiles.ospath.exists(self.__triviaDatabaseFile)
            self.__hasQuestionSetAvailable = hasQuestionSetAvailable

        return hasQuestionSetAvailable

    async def store(self, question: AbsTriviaQuestion) -> bool:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if not await self._triviaSettingsRepository.isScraperEnabled():
            return False

        # TODO
        return False
