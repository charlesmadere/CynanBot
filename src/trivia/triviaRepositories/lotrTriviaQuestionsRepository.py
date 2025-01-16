from .absTriviaQuestionRepository import AbsTriviaQuestionRepository
from .lordOfTheRings.lotrDatabaseQuestionStorageInterface import LotrDatabaseQuestionStorageInterface
from ..additionalAnswers.additionalTriviaAnswersRepositoryInterface import AdditionalTriviaAnswersRepositoryInterface
from ..compilers.triviaAnswerCompilerInterface import TriviaAnswerCompilerInterface
from ..compilers.triviaQuestionCompilerInterface import TriviaQuestionCompilerInterface
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..triviaDifficulty import TriviaDifficulty
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ...timber.timberInterface import TimberInterface


class LotrTriviaQuestionRepository(AbsTriviaQuestionRepository):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        lotrDatabaseQuestionStorage: LotrDatabaseQuestionStorageInterface,
        timber: TimberInterface,
        triviaAnswerCompiler: TriviaAnswerCompilerInterface,
        triviaQuestionCompiler: TriviaQuestionCompilerInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
    ):
        super().__init__(triviaSettingsRepository)

        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(lotrDatabaseQuestionStorage, LotrDatabaseQuestionStorageInterface):
            raise TypeError(f'lotrDatabaseQuestionStorage argument is malformed: \"{lotrDatabaseQuestionStorage}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaAnswerCompiler, TriviaAnswerCompilerInterface):
            raise TypeError(f'triviaAnswerCompiler argument is malformed: \"{triviaAnswerCompiler}\"')
        elif not isinstance(triviaQuestionCompiler, TriviaQuestionCompilerInterface):
            raise TypeError(f'triviaQuestionCompiler argument is malformed: \"{triviaQuestionCompiler}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__lotrDatabaseQuestionStorage: LotrDatabaseQuestionStorageInterface = lotrDatabaseQuestionStorage
        self.__timber: TimberInterface = timber
        self.__triviaAnswerCompiler: TriviaAnswerCompilerInterface = triviaAnswerCompiler
        self.__triviaQuestionCompiler: TriviaQuestionCompilerInterface = triviaQuestionCompiler

    async def fetchTriviaQuestion(self, fetchOptions: TriviaFetchOptions) -> AbsTriviaQuestion:
        if not isinstance(fetchOptions, TriviaFetchOptions):
            raise TypeError(f'fetchOptions argument is malformed: \"{fetchOptions}\"')

        self.__timber.log('LotrTriviaQuestionRepository', f'Fetching trivia question... ({fetchOptions=})')

        lotrTriviaQuestion = await self.__lotrDatabaseQuestionStorage.fetchTriviaQuestion()

        category = 'Lord of the Rings'
        question = await self.__triviaQuestionCompiler.compileQuestion(lotrTriviaQuestion.question)

        originalCorrectAnswers: list[str] = list()
        originalCorrectAnswers.extend(lotrTriviaQuestion.answers)

        correctAnswers: list[str] = list()
        correctAnswers.extend(originalCorrectAnswers)

        if await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswers(
            currentAnswers = correctAnswers,
            triviaId = lotrTriviaQuestion.triviaId,
            triviaQuestionType = TriviaQuestionType.QUESTION_ANSWER,
            triviaSource = self.triviaSource
        ):
            self.__timber.log('LotrTriviaQuestionRepository', f'Added additional answers to question ({lotrTriviaQuestion.triviaId=})')

        correctAnswers = await self.__triviaQuestionCompiler.compileResponses(correctAnswers)
        compiledCorrectAnswers = await self.__triviaAnswerCompiler.compileTextAnswersList(correctAnswers)

        expandedCompiledCorrectAnswers: set[str] = set()
        for answer in compiledCorrectAnswers:
            expandedCompiledCorrectAnswers.update(await self.__triviaAnswerCompiler.expandNumerals(answer))

        allWords = await self.__triviaQuestionCompiler.findAllWordsInQuestion(
            category = category,
            question = question
        )

        self.__timber.log('LotrTriviaQuestionsRepository', f'All words found in question ({question=}) and category ({category=}) ({lotrTriviaQuestion.triviaId=}): ({allWords=})')

        return QuestionAnswerTriviaQuestion(
            allWords = allWords,
            compiledCorrectAnswers = list(expandedCompiledCorrectAnswers),
            correctAnswers = correctAnswers,
            originalCorrectAnswers = originalCorrectAnswers,
            category = category,
            categoryId = None,
            question = question,
            triviaId = lotrTriviaQuestion.triviaId,
            triviaDifficulty = TriviaDifficulty.UNKNOWN,
            originalTriviaSource = None,
            triviaSource = self.triviaSource
        )

    async def hasQuestionSetAvailable(self) -> bool:
        return await self.__lotrDatabaseQuestionStorage.hasQuestionSetAvailable()

    @property
    def supportedTriviaTypes(self) -> set[TriviaQuestionType]:
        return { TriviaQuestionType.QUESTION_ANSWER }

    @property
    def triviaSource(self) -> TriviaSource:
        return TriviaSource.LORD_OF_THE_RINGS
