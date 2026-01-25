import asyncio
import queue
import random
import traceback
from queue import SimpleQueue

from frozendict import frozendict

from .bongoTriviaQuestionRepository import BongoTriviaQuestionRepository
from .funtoonTriviaQuestionRepository import FuntoonTriviaQuestionRepository
from .glacialTriviaQuestionRepositoryInterface import GlacialTriviaQuestionRepositoryInterface
from .jServiceTriviaQuestionRepository import JServiceTriviaQuestionRepository
from .lotrTriviaQuestionsRepository import LotrTriviaQuestionRepository
from .millionaireTriviaQuestionRepository import MillionaireTriviaQuestionRepository
from .openTriviaDatabaseTriviaQuestionRepository import OpenTriviaDatabaseTriviaQuestionRepository
from .openTriviaQaTriviaQuestionRepository import OpenTriviaQaTriviaQuestionRepository
from .pkmnTriviaQuestionRepository import PkmnTriviaQuestionRepository
from .quizApiTriviaQuestionRepository import QuizApiTriviaQuestionRepository
from .triviaDatabaseTriviaQuestionRepository import TriviaDatabaseTriviaQuestionRepository
from .triviaQuestionCompanyTriviaQuestionRepository import TriviaQuestionCompanyTriviaQuestionRepository
from .triviaQuestionRepositoryInterface import TriviaQuestionRepositoryInterface
from .triviaRepositoryInterface import TriviaRepositoryInterface
from .willFryTriviaQuestionRepository import WillFryTriviaQuestionRepository
from .wwtbamTriviaQuestionRepository import WwtbamTriviaQuestionRepository
from ..content.triviaContentCode import TriviaContentCode
from ..history.triviaQuestionOccurrencesRepositoryInterface import TriviaQuestionOccurrencesRepositoryInterface
from ..questionAnswerTriviaConditions import QuestionAnswerTriviaConditions
from ..questions.absTriviaQuestion import AbsTriviaQuestion
from ..questions.questionAnswerTriviaQuestion import QuestionAnswerTriviaQuestion
from ..questions.triviaQuestionType import TriviaQuestionType
from ..questions.triviaSource import TriviaSource
from ..scraper.triviaScraperInterface import TriviaScraperInterface
from ..settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..triviaExceptions import (GenericTriviaNetworkException,
                                MalformedTriviaJsonException,
                                NoTriviaCorrectAnswersException,
                                NoTriviaMultipleChoiceResponsesException,
                                NoTriviaQuestionException,
                                TooManyTriviaFetchAttemptsException,
                                UnavailableTriviaSourceException)
from ..triviaFetchOptions import TriviaFetchOptions
from ..triviaSourceInstabilityHelper import TriviaSourceInstabilityHelper
from ..triviaVerifierInterface import TriviaVerifierInterface
from ...misc import utils as utils
from ...misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from ...timber.timberInterface import TimberInterface
from ...twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ...users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class TriviaRepository(TriviaRepositoryInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        bongoTriviaQuestionRepository: BongoTriviaQuestionRepository,
        funtoonTriviaQuestionRepository: FuntoonTriviaQuestionRepository,
        glacialTriviaQuestionRepository: GlacialTriviaQuestionRepositoryInterface | None,
        jServiceTriviaQuestionRepository: JServiceTriviaQuestionRepository | None,
        lotrTriviaQuestionRepository: LotrTriviaQuestionRepository | None,
        millionaireTriviaQuestionRepository: MillionaireTriviaQuestionRepository,
        quizApiTriviaQuestionRepository: QuizApiTriviaQuestionRepository | None,
        openTriviaDatabaseTriviaQuestionRepository: OpenTriviaDatabaseTriviaQuestionRepository,
        openTriviaQaTriviaQuestionRepository: OpenTriviaQaTriviaQuestionRepository,
        pkmnTriviaQuestionRepository: PkmnTriviaQuestionRepository,
        timber: TimberInterface,
        triviaDatabaseTriviaQuestionRepository: TriviaDatabaseTriviaQuestionRepository,
        triviaQuestionCompanyTriviaQuestionRepository: TriviaQuestionCompanyTriviaQuestionRepository,
        triviaQuestionOccurrencesRepository: TriviaQuestionOccurrencesRepositoryInterface,
        triviaScraper: TriviaScraperInterface | None,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaSourceInstabilityHelper: TriviaSourceInstabilityHelper,
        triviaVerifier: TriviaVerifierInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        willFryTriviaQuestionRepository: WillFryTriviaQuestionRepository,
        wwtbamTriviaQuestionRepository: WwtbamTriviaQuestionRepository,
        spoolerLoopSleepTimeSeconds: float = 120,
        triviaRetrySleepTimeSeconds: float = 0.25
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(bongoTriviaQuestionRepository, BongoTriviaQuestionRepository):
            raise TypeError(f'bongoTriviaQuestionRepository argument is malformed: \"{bongoTriviaQuestionRepository}\"')
        elif not isinstance(funtoonTriviaQuestionRepository, FuntoonTriviaQuestionRepository):
            raise TypeError(f'funtoonTriviaQuestionRepository argument is malformed: \"{funtoonTriviaQuestionRepository}\"')
        elif glacialTriviaQuestionRepository is not None and not isinstance(glacialTriviaQuestionRepository, GlacialTriviaQuestionRepositoryInterface):
            raise TypeError(f'glacialTriviaQuestionRepository argument is malformed: \"{glacialTriviaQuestionRepository}\"')
        elif jServiceTriviaQuestionRepository is not None and not isinstance(jServiceTriviaQuestionRepository, JServiceTriviaQuestionRepository):
            raise TypeError(f'jServiceTriviaQuestionRepository argument is malformed \"{jServiceTriviaQuestionRepository}\"')
        elif lotrTriviaQuestionRepository is not None and not isinstance(lotrTriviaQuestionRepository, LotrTriviaQuestionRepository):
            raise TypeError(f'lotrTriviaQuestionRepository argument is malformed: \"{lotrTriviaQuestionRepository}\"')
        elif not isinstance(millionaireTriviaQuestionRepository, MillionaireTriviaQuestionRepository):
            raise TypeError(f'millionaireTriviaQuestionRepository argument is malformed: \"{millionaireTriviaQuestionRepository}\"')
        elif not isinstance(openTriviaDatabaseTriviaQuestionRepository, OpenTriviaDatabaseTriviaQuestionRepository):
            raise TypeError(f'openTriviaDatabaseTriviaQuestionRepository argument is malformed: \"{openTriviaDatabaseTriviaQuestionRepository}\"')
        elif not isinstance(openTriviaQaTriviaQuestionRepository, OpenTriviaQaTriviaQuestionRepository):
            raise TypeError(f'openTriviaQaTriviaQuestionRepository argument is malformed: \"{openTriviaQaTriviaQuestionRepository}\"')
        elif not isinstance(pkmnTriviaQuestionRepository, PkmnTriviaQuestionRepository):
            raise TypeError(f'pkmnTriviaQuestionRepository argument is malformed: \"{pkmnTriviaQuestionRepository}\"')
        elif quizApiTriviaQuestionRepository is not None and not isinstance(quizApiTriviaQuestionRepository, QuizApiTriviaQuestionRepository):
            raise TypeError(f'quizApiTriviaQuestionRepository argument is malformed: \"{quizApiTriviaQuestionRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaDatabaseTriviaQuestionRepository, TriviaDatabaseTriviaQuestionRepository):
            raise TypeError(f'triviaDatabaseTriviaQuestionRepository argument is malformed: \"{triviaDatabaseTriviaQuestionRepository}\"')
        elif not isinstance(triviaQuestionCompanyTriviaQuestionRepository, TriviaQuestionCompanyTriviaQuestionRepository):
            raise TypeError(f'triviaQuestionCompanyTriviaQuestionRepository argument is malformed: \"{triviaQuestionCompanyTriviaQuestionRepository}\"')
        elif not isinstance(triviaQuestionOccurrencesRepository, TriviaQuestionOccurrencesRepositoryInterface):
            raise TypeError(f'triviaQuestionOccurrencesRepository argument is malformed: \"{triviaQuestionOccurrencesRepository}\"')
        elif triviaScraper is not None and not isinstance(triviaScraper, TriviaScraperInterface):
            raise TypeError(f'triviaScraper argument is malformed: \"{triviaScraper}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(triviaSourceInstabilityHelper, TriviaSourceInstabilityHelper):
            raise TypeError(f'triviaSourceInstabilityHelper argument is malformed: \"{triviaSourceInstabilityHelper}\"')
        elif not isinstance(triviaVerifier, TriviaVerifierInterface):
            raise TypeError(f'triviaVerifier argument is malformed: \"{triviaVerifier}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(willFryTriviaQuestionRepository, WillFryTriviaQuestionRepository):
            raise TypeError(f'willFryTriviaQuestionRepository argument is malformed: \"{willFryTriviaQuestionRepository}\"')
        elif not isinstance(wwtbamTriviaQuestionRepository, WwtbamTriviaQuestionRepository):
            raise TypeError(f'wwtbamTriviaQuestionRepository argument is malformed: \"{wwtbamTriviaQuestionRepository}\"')
        elif not utils.isValidNum(spoolerLoopSleepTimeSeconds):
            raise TypeError(f'spoolerLoopSleepTimeSeconds argument is malformed: \"{spoolerLoopSleepTimeSeconds}\"')
        elif spoolerLoopSleepTimeSeconds < 15 or spoolerLoopSleepTimeSeconds > 300:
            raise ValueError(f'spoolerLoopSleepTimeSeconds argument is out of bounds: {spoolerLoopSleepTimeSeconds}')
        elif not utils.isValidNum(triviaRetrySleepTimeSeconds):
            raise TypeError(f'triviaRetrySleepTimeSeconds argument is malformed: \"{triviaRetrySleepTimeSeconds}\"')
        elif triviaRetrySleepTimeSeconds < 0.25 or triviaRetrySleepTimeSeconds > 3:
            raise ValueError(f'triviaRetrySleepTimeSeconds argument is out of bounds: {triviaRetrySleepTimeSeconds}')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__bongoTriviaQuestionRepository: TriviaQuestionRepositoryInterface = bongoTriviaQuestionRepository
        self.__funtoonTriviaQuestionRepository: TriviaQuestionRepositoryInterface = funtoonTriviaQuestionRepository
        self.__glacialTriviaQuestionRepository: TriviaQuestionRepositoryInterface | None = glacialTriviaQuestionRepository
        self.__jServiceTriviaQuestionRepository: TriviaQuestionRepositoryInterface | None = jServiceTriviaQuestionRepository
        self.__lotrTriviaQuestionRepository: TriviaQuestionRepositoryInterface | None = lotrTriviaQuestionRepository
        self.__millionaireTriviaQuestionRepository: TriviaQuestionRepositoryInterface = millionaireTriviaQuestionRepository
        self.__openTriviaDatabaseTriviaQuestionRepository: TriviaQuestionRepositoryInterface = openTriviaDatabaseTriviaQuestionRepository
        self.__openTriviaQaTriviaQuestionRepository: TriviaQuestionRepositoryInterface = openTriviaQaTriviaQuestionRepository
        self.__pkmnTriviaQuestionRepository: TriviaQuestionRepositoryInterface = pkmnTriviaQuestionRepository
        self.__quizApiTriviaQuestionRepository: TriviaQuestionRepositoryInterface | None = quizApiTriviaQuestionRepository
        self.__timber: TimberInterface = timber
        self.__triviaDatabaseTriviaQuestionRepository: TriviaQuestionRepositoryInterface = triviaDatabaseTriviaQuestionRepository
        self.__triviaQuestionCompanyTriviaQuestionRepository: TriviaQuestionRepositoryInterface = triviaQuestionCompanyTriviaQuestionRepository
        self.__triviaQuestionOccurrencesRepository: TriviaQuestionOccurrencesRepositoryInterface = triviaQuestionOccurrencesRepository
        self.__triviaScraper: TriviaScraperInterface | None = triviaScraper
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__triviaSourceInstabilityHelper: TriviaSourceInstabilityHelper = triviaSourceInstabilityHelper
        self.__triviaVerifier: TriviaVerifierInterface = triviaVerifier
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__willFryTriviaQuestionRepository: TriviaQuestionRepositoryInterface = willFryTriviaQuestionRepository
        self.__wwtbamTriviaQuestionRepository: TriviaQuestionRepositoryInterface = wwtbamTriviaQuestionRepository
        self.__spoolerLoopSleepTimeSeconds: float = spoolerLoopSleepTimeSeconds
        self.__triviaRetrySleepTimeSeconds: float = triviaRetrySleepTimeSeconds

        self.__isSpoolerStarted: bool = False
        self.__triviaSourceToRepositoryMap: frozendict[TriviaSource, TriviaQuestionRepositoryInterface | None] = self.__createTriviaSourceToRepositoryMap()
        self.__superTriviaQuestionSpool: SimpleQueue[QuestionAnswerTriviaQuestion] = SimpleQueue()
        self.__triviaQuestionSpool: SimpleQueue[AbsTriviaQuestion] = SimpleQueue()
        self.__twitchChannelId: str | None = None

    async def __chooseRandomTriviaSource(
        self,
        triviaFetchOptions: TriviaFetchOptions
    ) -> TriviaQuestionRepositoryInterface:
        if not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        allTriviaSourcesAndProperties = await self.__triviaSettingsRepository.getTriviaSourcesAndProperties()

        currentlyInvalidTriviaSources = await self.__getCurrentlyInvalidTriviaSources(
            triviaFetchOptions = triviaFetchOptions
        )

        triviaSources: list[TriviaSource] = list()
        triviaWeights: list[int] = list()

        for triviaSource, triviaSourceAndProperties in allTriviaSourcesAndProperties.items():
            if triviaSource in currentlyInvalidTriviaSources or not triviaSourceAndProperties.isEnabled:
                continue

            triviaSources.append(triviaSourceAndProperties.triviaSource)
            triviaWeights.append(triviaSourceAndProperties.weight)

        if len(triviaSources) == 0 or len(triviaWeights) == 0:
            raise RuntimeError(f'There are no trivia sources available to be fetched from! ({triviaFetchOptions=}) ({allTriviaSourcesAndProperties=}) ({currentlyInvalidTriviaSources=})')

        randomlyChosenTriviaSource = random.choices(population = triviaSources, weights = triviaWeights)[0]
        randomlyChosenTriviaRepository = self.__triviaSourceToRepositoryMap[randomlyChosenTriviaSource]

        if not isinstance(randomlyChosenTriviaRepository, TriviaQuestionRepositoryInterface):
            # this scenario should definitely be impossible, but the Python type checking was
            # getting angry without this check
            raise RuntimeError(f'Couldn\'t retrieve corresponding TriviaQuestionRepository from given randomlyChosenTriviaSource ({triviaFetchOptions=}) ({allTriviaSourcesAndProperties=}) ({currentlyInvalidTriviaSources=}) ({randomlyChosenTriviaSource=}) ({randomlyChosenTriviaRepository=}) ({self.__triviaSourceToRepositoryMap=})')

        return randomlyChosenTriviaRepository

    def __createTriviaSourceToRepositoryMap(self) -> frozendict[TriviaSource, TriviaQuestionRepositoryInterface | None]:
        triviaSourceToRepositoryMap: dict[TriviaSource, TriviaQuestionRepositoryInterface | None] = {
            TriviaSource.BONGO: self.__bongoTriviaQuestionRepository,
            TriviaSource.FUNTOON: self.__funtoonTriviaQuestionRepository,
            TriviaSource.GLACIAL: self.__glacialTriviaQuestionRepository,
            TriviaSource.J_SERVICE: self.__jServiceTriviaQuestionRepository,
            TriviaSource.LORD_OF_THE_RINGS: self.__lotrTriviaQuestionRepository,
            TriviaSource.MILLIONAIRE: self.__millionaireTriviaQuestionRepository,
            TriviaSource.OPEN_TRIVIA_DATABASE: self.__openTriviaDatabaseTriviaQuestionRepository,
            TriviaSource.OPEN_TRIVIA_QA: self.__openTriviaQaTriviaQuestionRepository,
            TriviaSource.POKE_API: self.__pkmnTriviaQuestionRepository,
            TriviaSource.QUIZ_API: self.__quizApiTriviaQuestionRepository,
            TriviaSource.THE_QUESTION_CO: self.__triviaQuestionCompanyTriviaQuestionRepository,
            TriviaSource.TRIVIA_DATABASE: self.__triviaDatabaseTriviaQuestionRepository,
            TriviaSource.WILL_FRY_TRIVIA: self.__willFryTriviaQuestionRepository,
            TriviaSource.WWTBAM: self.__wwtbamTriviaQuestionRepository
        }

        if len(triviaSourceToRepositoryMap.keys()) != len(TriviaSource):
            raise RuntimeError(f'triviaSourceToRepositoryMap is missing some members of TriviaSource! ({triviaSourceToRepositoryMap=})')

        return frozendict(triviaSourceToRepositoryMap)

    async def __getTriviaSource(
        self,
        triviaFetchOptions: TriviaFetchOptions
    ) -> TriviaQuestionRepositoryInterface:
        if not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        if triviaFetchOptions.requiredTriviaSource is not None:
            invalidTriviaSources = await self.__getCurrentlyInvalidTriviaSources(
                triviaFetchOptions = triviaFetchOptions
            )

            if triviaFetchOptions.requiredTriviaSource in invalidTriviaSources:
                raise UnavailableTriviaSourceException("Trivia source is currently invalid")

            triviaSource = self.__triviaSourceToRepositoryMap[triviaFetchOptions.requiredTriviaSource]

            if triviaSource is None:
                raise UnavailableTriviaSourceException("Unable to fetch trivia source from trivia source repository map")
            else:
                return triviaSource

        return await self.__chooseRandomTriviaSource(
            triviaFetchOptions = triviaFetchOptions
        )

    async def fetchTrivia(
        self,
        emote: str,
        triviaFetchOptions: TriviaFetchOptions
    ) -> AbsTriviaQuestion | None:
        if not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        question: AbsTriviaQuestion | None = None
        retryCount = 0
        maxRetryCount = await self.__triviaSettingsRepository.getMaxRetryCount()
        attemptedTriviaSources: list[TriviaSource] = list()

        while retryCount < maxRetryCount:
            if triviaFetchOptions.requiredTriviaSource is not None:
                question = None
            else:
                question = await self.__retrieveSpooledTriviaQuestion(triviaFetchOptions)

            if question is None:
                try:
                    triviaQuestionRepository = await self.__getTriviaSource(
                        triviaFetchOptions = triviaFetchOptions
                    )
                except UnavailableTriviaSourceException as e:
                    self.__timber.log('TriviaRepository', f'Failed to get trivia source ({triviaFetchOptions=}): {e}', e, traceback.format_exc())
                    return None

                triviaSource = triviaQuestionRepository.triviaSource
                attemptedTriviaSources.append(triviaSource)

                try:
                    question = await triviaQuestionRepository.fetchTriviaQuestion(triviaFetchOptions)
                except (NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException, NoTriviaQuestionException) as e:
                    self.__timber.log('TriviaRepository', f'Failed to fetch trivia question due to malformed data (trivia source was \"{triviaSource}\"): {e}', e, traceback.format_exc())
                except GenericTriviaNetworkException as e:
                    errorCount = self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
                    self.__timber.log('TriviaRepository', f'Encountered network Exception when fetching trivia question (trivia source was \"{triviaSource}\") (new error count is {errorCount}): {e}', e, traceback.format_exc())
                except MalformedTriviaJsonException as e:
                    errorCount = self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
                    self.__timber.log('TriviaRepository', f'Encountered malformed JSON Exception when fetching trivia question (trivia source was \"{triviaSource}\") (new error count is {errorCount}): {e}', e, traceback.format_exc())
                except Exception as e:
                    errorCount = self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
                    self.__timber.log('TriviaRepository', f'Encountered unknown Exception when fetching trivia question (trivia source was \"{triviaSource}\") (new error count is {errorCount}): {e}', e, traceback.format_exc())

            if question is not None and await self.__verifyTriviaQuestionContent(
                question = question,
                triviaFetchOptions = triviaFetchOptions
            ):
                await self.__scrapeAndStore(question)

                if await self.__verifyTriviaQuestionIsNotDuplicate(
                    question = question,
                    emote = emote,
                    triviaFetchOptions = triviaFetchOptions
                ):
                    return question

            question = None
            retryCount = retryCount + 1
            await asyncio.sleep(self.__triviaRetrySleepTimeSeconds * float(retryCount))

        raise TooManyTriviaFetchAttemptsException(f'Unable to fetch trivia after {retryCount} attempts ({maxRetryCount=}) ({attemptedTriviaSources=}) ({triviaFetchOptions=})')

    async def __getCurrentlyInvalidTriviaSources(
        self,
        triviaFetchOptions: TriviaFetchOptions
    ) -> frozenset[TriviaSource]:
        if not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        availableTriviaSourcesMap: dict[TriviaSource, TriviaQuestionRepositoryInterface] = dict()
        for triviaSource, triviaQuestionRepository in self.__triviaSourceToRepositoryMap.items():
            if triviaQuestionRepository is not None and await triviaQuestionRepository.hasQuestionSetAvailable():
                availableTriviaSourcesMap[triviaSource] = triviaQuestionRepository

        currentlyInvalidTriviaSources: set[TriviaSource] = set()

        if not triviaFetchOptions.areQuestionAnswerTriviaQuestionsEnabled():
            for triviaSource, triviaQuestionRepository in availableTriviaSourcesMap.items():
                if TriviaQuestionType.QUESTION_ANSWER in triviaQuestionRepository.supportedTriviaTypes:
                    currentlyInvalidTriviaSources.add(triviaSource)

        if triviaFetchOptions.requireQuestionAnswerTriviaQuestion():
            for triviaSource, triviaQuestionRepository in availableTriviaSourcesMap.items():
                if TriviaQuestionType.QUESTION_ANSWER not in triviaQuestionRepository.supportedTriviaTypes:
                    currentlyInvalidTriviaSources.add(triviaSource)

        if not await self.__isGlacialTriviaQuestionRepositoryAvailable():
            currentlyInvalidTriviaSources.add(TriviaSource.GLACIAL)

        if not await self.__isJServiceTriviaQuestionRepositoryAvailable():
            currentlyInvalidTriviaSources.add(TriviaSource.J_SERVICE)

        if not await self.__isLotrTriviaQuestionRepositoryAvailable():
            currentlyInvalidTriviaSources.add(TriviaSource.LORD_OF_THE_RINGS)

        if not await self.__isQuizApiTriviaQuestionRepositoryAvailable():
            currentlyInvalidTriviaSources.add(TriviaSource.QUIZ_API)

        currentlyUnstableTriviaSources = await self.__getCurrentlyUnstableTriviaSources()
        currentlyInvalidTriviaSources.update(currentlyUnstableTriviaSources)

        return frozenset(currentlyInvalidTriviaSources)

    async def __getCurrentlyUnstableTriviaSources(self) -> set[TriviaSource]:
        instabilityThreshold = await self.__triviaSettingsRepository.getTriviaSourceInstabilityThreshold()
        unstableTriviaSources: set[TriviaSource] = set()

        for triviaSource in TriviaSource:
            if self.__triviaSourceInstabilityHelper[triviaSource] >= instabilityThreshold:
                unstableTriviaSources.add(triviaSource)

        return unstableTriviaSources

    async def __getTwitchChannelId(self) -> str:
        twitchChannelId = self.__twitchChannelId

        if twitchChannelId is not None:
            return twitchChannelId

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchChannelId = await self.__userIdsRepository.requireUserId(twitchHandle)
        self.__twitchChannelId = twitchChannelId

        return twitchChannelId

    async def __isGlacialTriviaQuestionRepositoryAvailable(self) -> bool:
        glacialTriviaQuestionRepository = self.__glacialTriviaQuestionRepository

        if glacialTriviaQuestionRepository is None:
            return False

        return await glacialTriviaQuestionRepository.hasQuestionSetAvailable()

    async def __isJServiceTriviaQuestionRepositoryAvailable(self) -> bool:
        jServiceTriviaQuestionRepository = self.__jServiceTriviaQuestionRepository

        if jServiceTriviaQuestionRepository is None:
            return False

        return await jServiceTriviaQuestionRepository.hasQuestionSetAvailable()

    async def __isLotrTriviaQuestionRepositoryAvailable(self) -> bool:
        lotrTriviaQuestionRepository = self.__lotrTriviaQuestionRepository

        if lotrTriviaQuestionRepository is None:
            return False

        return await lotrTriviaQuestionRepository.hasQuestionSetAvailable()

    async def __isQuizApiTriviaQuestionRepositoryAvailable(self) -> bool:
        quizApiTriviaQuestionRepository = self.__quizApiTriviaQuestionRepository

        if quizApiTriviaQuestionRepository is None:
            return False

        return await quizApiTriviaQuestionRepository.hasQuestionSetAvailable()

    async def __retrieveSpooledTriviaQuestion(
        self,
        triviaFetchOptions: TriviaFetchOptions
    ) -> AbsTriviaQuestion | None:
        if not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        if triviaFetchOptions.requireQuestionAnswerTriviaQuestion():
            if not self.__superTriviaQuestionSpool.empty():
                try:
                    self.__timber.log('TriviaRepository', f'Retrieving spooled super trivia question (current qsize: {self.__superTriviaQuestionSpool.qsize()})')
                    return self.__superTriviaQuestionSpool.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('TriviaRepository', f'Encountered queue.Empty when trying to retrieve a spooled super trivia question', e, traceback.format_exc())
        else:
            if not self.__triviaQuestionSpool.empty():
                try:
                    self.__timber.log('TriviaRepository', f'Retrieving spooled trivia question (current qsize: {self.__triviaQuestionSpool.qsize()})')
                    return self.__triviaQuestionSpool.get_nowait()
                except queue.Empty as e:
                    self.__timber.log('TriviaRepository', f'Encountered queue.Empty when trying to retrieve a spooled trivia question', e, traceback.format_exc())

        return None

    async def __scrapeAndStore(self, question: AbsTriviaQuestion | None):
        if question is None:
            return
        elif not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')

        if not await self.__triviaSettingsRepository.isScraperEnabled():
            return

        triviaScraper = self.__triviaScraper

        if triviaScraper is not None:
            await triviaScraper.store(question)

    async def __spoolNewSuperTriviaQuestion(self):
        if self.__superTriviaQuestionSpool.qsize() >= await self.__triviaSettingsRepository.getMaxSuperTriviaQuestionSpoolSize():
            return

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchChannelId = await self.__getTwitchChannelId(),
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )

        self.__timber.log('TriviaRepository', f'Spooling up a super trivia question (current qsize: {self.__superTriviaQuestionSpool.qsize()})')
        triviaQuestionRepository = await self.__chooseRandomTriviaSource(triviaFetchOptions)
        triviaSource = triviaQuestionRepository.triviaSource
        question: AbsTriviaQuestion | None = None

        try:
            question = await triviaQuestionRepository.fetchTriviaQuestion(triviaFetchOptions)
        except (NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException, NoTriviaQuestionException) as e:
            self.__timber.log('TriviaRepository', f'Failed to fetch trivia question for spool due to malformed data ({triviaSource=}): {e}', e, traceback.format_exc())
        except GenericTriviaNetworkException as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered network Exception when fetching super trivia question for spool ({triviaSource=}): {e}', e, traceback.format_exc())
        except MalformedTriviaJsonException as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered malformed JSON Exception when fetching super trivia question for spool ({triviaSource=}): {e}', e, traceback.format_exc())
        except Exception as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered unknown Exception when fetching super trivia question for spool ({triviaSource=}): {e}', e, traceback.format_exc())

        if question is None:
            return
        elif not isinstance(question, QuestionAnswerTriviaQuestion) or question.triviaType is not TriviaQuestionType.QUESTION_ANSWER:
            self.__timber.log('TriviaRepository', f'Encountered unexpected super trivia question type when spooling a super trivia question ({question=})')
            return

        if not await self.__verifyTriviaQuestionContent(
            question = question,
            triviaFetchOptions = triviaFetchOptions
        ):
            self.__timber.log('TriviaRepository', f'Encountered bad trivia question content when spooling a super trivia question ({question=})')
            return

        self.__superTriviaQuestionSpool.put(question)
        self.__timber.log('TriviaRepository', f'Finished spooling up a super trivia question (new qsize: {self.__superTriviaQuestionSpool.qsize()})')
        await self.__scrapeAndStore(question)

    async def __spoolNewTriviaQuestion(self):
        if self.__triviaQuestionSpool.qsize() >= await self.__triviaSettingsRepository.getMaxTriviaQuestionSpoolSize():
            return

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle(),
            twitchChannelId = await self.__getTwitchChannelId(),
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
        )

        self.__timber.log('TriviaRepository', f'Spooling up a trivia question (current qsize: {self.__triviaQuestionSpool.qsize()})')
        triviaQuestionRepository = await self.__chooseRandomTriviaSource(triviaFetchOptions)
        triviaSource = triviaQuestionRepository.triviaSource
        question: AbsTriviaQuestion | None = None

        try:
            question = await triviaQuestionRepository.fetchTriviaQuestion(triviaFetchOptions)
        except (NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException, NoTriviaQuestionException) as e:
            self.__timber.log('TriviaRepository', f'Failed to fetch trivia question for spool due to malformed data ({triviaSource=}): {e}', e, traceback.format_exc())
        except GenericTriviaNetworkException as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered network Exception when fetching trivia question for spool ({triviaSource=}): {e}', e, traceback.format_exc())
        except MalformedTriviaJsonException as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered malformed JSON Exception when fetching trivia question for spool ({triviaSource=}): {e}', e, traceback.format_exc())
        except Exception as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered unknown Exception when fetching trivia question for spool ({triviaSource=}): {e}', e, traceback.format_exc())

        if question is None:
            return
        elif isinstance(question, QuestionAnswerTriviaQuestion) or question.triviaType is TriviaQuestionType.QUESTION_ANSWER:
            self.__timber.log('TriviaRepository', f'Encountered unexpected trivia question type when spooling a trivia question ({question=})')
            return

        if not await self.__verifyTriviaQuestionContent(
            question = question,
            triviaFetchOptions = triviaFetchOptions
        ):
            self.__timber.log('TriviaRepository', f'Encountered bad trivia question content when spooling a trivia question ({question=})')
            return

        self.__triviaQuestionSpool.put(question)
        self.__timber.log('TriviaRepository', f'Finished spooling up a trivia question (new qsize: {self.__triviaQuestionSpool.qsize()})')
        await self.__scrapeAndStore(question)

    def startSpooler(self):
        if self.__isSpoolerStarted:
            self.__timber.log('TriviaRepository', 'Not starting spooler as it has already been started')
            return

        self.__isSpoolerStarted = True
        self.__timber.log('TriviaRepository', 'Starting spooler...')
        self.__backgroundTaskHelper.createTask(self.__startTriviaQuestionSpooler())

    async def __startTriviaQuestionSpooler(self):
        while True:
            try:
                await self.__spoolNewTriviaQuestion()
            except Exception as e:
                self.__timber.log('TriviaRepository', f'Encountered unknown Exception when refreshing trivia question spool', e, traceback.format_exc())

            try:
                await self.__spoolNewSuperTriviaQuestion()
            except Exception as e:
                self.__timber.log('TriviaRepository', f'Encountered unknown Exception when refreshing super trivia question spool', e, traceback.format_exc())

            await asyncio.sleep(self.__spoolerLoopSleepTimeSeconds)

    async def __verifyTriviaQuestionContent(
        self,
        question: AbsTriviaQuestion | None,
        triviaFetchOptions: TriviaFetchOptions
    ) -> bool:
        if question is not None and not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        triviaContentCode = await self.__triviaVerifier.checkContent(
            question = question,
            triviaFetchOptions = triviaFetchOptions
        )

        if triviaContentCode is TriviaContentCode.OK:
            return True
        else:
            self.__timber.log('TriviaRepository', f'A trivia question failed content verification ({question=}) ({triviaFetchOptions=}) ({triviaContentCode=})')
            return False

    async def __verifyTriviaQuestionIsNotDuplicate(
        self,
        question: AbsTriviaQuestion,
        emote: str,
        triviaFetchOptions: TriviaFetchOptions
    ) -> bool:
        if not isinstance(question, AbsTriviaQuestion):
            raise TypeError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(emote):
            raise TypeError(f'emote argument is malformed: \"{emote}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        triviaContentCode = await self.__triviaVerifier.checkHistory(
            question = question,
            emote = emote,
            triviaFetchOptions = triviaFetchOptions
        )

        if triviaContentCode is TriviaContentCode.OK:
            await self.__triviaQuestionOccurrencesRepository.incrementOccurrencesFromQuestion(
                triviaQuestion = question
            )

            return True
        else:
            self.__timber.log('TriviaRepository', f'Rejected a trivia question as it ended up being a duplicate ({triviaContentCode=})')
            return False
