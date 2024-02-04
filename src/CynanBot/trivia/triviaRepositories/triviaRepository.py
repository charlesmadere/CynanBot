import asyncio
import queue
import random
import traceback
from queue import SimpleQueue
from typing import Dict, List, Optional, Set

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.content.triviaContentCode import TriviaContentCode
from CynanBot.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBot.trivia.questions.absTriviaQuestion import AbsTriviaQuestion
from CynanBot.trivia.questions.questionAnswerTriviaQuestion import \
    QuestionAnswerTriviaQuestion
from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource
from CynanBot.trivia.triviaExceptions import (
    GenericTriviaNetworkException, MalformedTriviaJsonException,
    NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException,
    NoTriviaQuestionException, TooManyTriviaFetchAttemptsException)
from CynanBot.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBot.trivia.triviaRepositories.bongoTriviaQuestionRepository import \
    BongoTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.funtoonTriviaQuestionRepository import \
    FuntoonTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.jServiceTriviaQuestionRepository import \
    JServiceTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.lotrTriviaQuestionsRepository import \
    LotrTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.millionaireTriviaQuestionRepository import \
    MillionaireTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.openTriviaQaTriviaQuestionRepository import \
    OpenTriviaQaTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.pkmnTriviaQuestionRepository import \
    PkmnTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.quizApiTriviaQuestionRepository import \
    QuizApiTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaDatabaseTriviaQuestionRepository import \
    TriviaDatabaseTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaQuestionCompanyTriviaQuestionRepository import \
    TriviaQuestionCompanyTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.triviaQuestionRepositoryInterface import \
    TriviaQuestionRepositoryInterface
from CynanBot.trivia.triviaRepositories.triviaRepositoryInterface import \
    TriviaRepositoryInterface
from CynanBot.trivia.triviaRepositories.willFryTriviaQuestionRepository import \
    WillFryTriviaQuestionRepository
from CynanBot.trivia.triviaRepositories.wwtbamTriviaQuestionRepository import \
    WwtbamTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.trivia.triviaSourceInstabilityHelper import \
    TriviaSourceInstabilityHelper
from CynanBot.trivia.triviaVerifierInterface import TriviaVerifierInterface
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface


class TriviaRepository(TriviaRepositoryInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        bongoTriviaQuestionRepository: BongoTriviaQuestionRepository,
        funtoonTriviaQuestionRepository: FuntoonTriviaQuestionRepository,
        jServiceTriviaQuestionRepository: Optional[JServiceTriviaQuestionRepository],
        lotrTriviaQuestionRepository: Optional[LotrTriviaQuestionRepository],
        millionaireTriviaQuestionRepository: MillionaireTriviaQuestionRepository,
        quizApiTriviaQuestionRepository: Optional[QuizApiTriviaQuestionRepository],
        openTriviaDatabaseTriviaQuestionRepository: OpenTriviaDatabaseTriviaQuestionRepository,
        openTriviaQaTriviaQuestionRepository: OpenTriviaQaTriviaQuestionRepository,
        pkmnTriviaQuestionRepository: PkmnTriviaQuestionRepository,
        timber: TimberInterface,
        triviaDatabaseTriviaQuestionRepository: TriviaDatabaseTriviaQuestionRepository,
        triviaQuestionCompanyTriviaQuestionRepository: TriviaQuestionCompanyTriviaQuestionRepository,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaSourceInstabilityHelper: TriviaSourceInstabilityHelper,
        triviaVerifier: TriviaVerifierInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        willFryTriviaQuestionRepository: WillFryTriviaQuestionRepository,
        wwtbamTriviaQuestionRepository: WwtbamTriviaQuestionRepository,
        spoolerLoopSleepTimeSeconds: float = 120,
        triviaRetrySleepTimeSeconds: float = 0.25
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(bongoTriviaQuestionRepository, BongoTriviaQuestionRepository):
            raise TypeError(f'bongoTriviaQuestionRepository argument is malformed: \"{bongoTriviaQuestionRepository}\"')
        elif not isinstance(funtoonTriviaQuestionRepository, FuntoonTriviaQuestionRepository):
            raise TypeError(f'funtoonTriviaQuestionRepository argument is malformed: \"{funtoonTriviaQuestionRepository}\"')
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
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(triviaSourceInstabilityHelper, TriviaSourceInstabilityHelper):
            raise TypeError(f'triviaSourceInstabilityHelper argument is malformed: \"{triviaSourceInstabilityHelper}\"')
        elif not isinstance(triviaVerifier, TriviaVerifierInterface):
            raise TypeError(f'triviaVerifier argument is malformed: \"{triviaVerifier}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
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

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__bongoTriviaQuestionRepository: TriviaQuestionRepositoryInterface = bongoTriviaQuestionRepository
        self.__funtoonTriviaQuestionRepository: TriviaQuestionRepositoryInterface = funtoonTriviaQuestionRepository
        self.__jServiceTriviaQuestionRepository: Optional[TriviaQuestionRepositoryInterface] = jServiceTriviaQuestionRepository
        self.__lotrTriviaQuestionRepository: Optional[TriviaQuestionRepositoryInterface] = lotrTriviaQuestionRepository
        self.__millionaireTriviaQuestionRepository: TriviaQuestionRepositoryInterface = millionaireTriviaQuestionRepository
        self.__openTriviaDatabaseTriviaQuestionRepository: TriviaQuestionRepositoryInterface = openTriviaDatabaseTriviaQuestionRepository
        self.__openTriviaQaTriviaQuestionRepository: TriviaQuestionRepositoryInterface = openTriviaQaTriviaQuestionRepository
        self.__pkmnTriviaQuestionRepository: TriviaQuestionRepositoryInterface = pkmnTriviaQuestionRepository
        self.__quizApiTriviaQuestionRepository: Optional[TriviaQuestionRepositoryInterface] = quizApiTriviaQuestionRepository
        self.__timber: TimberInterface = timber
        self.__triviaDatabaseTriviaQuestionRepository: TriviaQuestionRepositoryInterface = triviaDatabaseTriviaQuestionRepository
        self.__triviaQuestionCompanyTriviaQuestionRepository: TriviaQuestionRepositoryInterface = triviaQuestionCompanyTriviaQuestionRepository
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__triviaSourceInstabilityHelper: TriviaSourceInstabilityHelper = triviaSourceInstabilityHelper
        self.__triviaVerifier: TriviaVerifierInterface = triviaVerifier
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__willFryTriviaQuestionRepository: TriviaQuestionRepositoryInterface = willFryTriviaQuestionRepository
        self.__wwtbamTriviaQuestionRepository: TriviaQuestionRepositoryInterface = wwtbamTriviaQuestionRepository
        self.__spoolerLoopSleepTimeSeconds: float = spoolerLoopSleepTimeSeconds
        self.__triviaRetrySleepTimeSeconds: float = triviaRetrySleepTimeSeconds

        self.__isSpoolerStarted: bool = False
        self.__triviaSourceToRepositoryMap: Dict[TriviaSource, Optional[TriviaQuestionRepositoryInterface]] = self.__createTriviaSourceToRepositoryMap()
        self.__superTriviaQuestionSpool: SimpleQueue[QuestionAnswerTriviaQuestion] = SimpleQueue()
        self.__triviaQuestionSpool: SimpleQueue[AbsTriviaQuestion] = SimpleQueue()

    async def __chooseRandomTriviaSource(self, triviaFetchOptions: TriviaFetchOptions) -> TriviaQuestionRepositoryInterface:
        if not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise TypeError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        triviaSourcesAndWeights: Dict[TriviaSource, int] = await self.__triviaSettingsRepository.getAvailableTriviaSourcesAndWeights()
        triviaSourcesToRemove: Set[TriviaSource] = await self.__getCurrentlyInvalidTriviaSources(triviaFetchOptions)

        for triviaSourceToRemove in triviaSourcesToRemove:
            if triviaSourceToRemove in triviaSourcesAndWeights:
                del triviaSourcesAndWeights[triviaSourceToRemove]

        if not utils.hasItems(triviaSourcesAndWeights):
            raise RuntimeError(f'There are no trivia sources available to be fetched from! TriviaFetchOptions are: {triviaFetchOptions}')

        triviaSources: List[TriviaSource] = list()
        triviaWeights: List[int] = list()

        for triviaSource in triviaSourcesAndWeights:
            triviaSources.append(triviaSource)
            triviaWeights.append(triviaSourcesAndWeights[triviaSource])

        randomChoices = random.choices(
            population = triviaSources,
            weights = triviaWeights
        )

        if not utils.hasItems(randomChoices):
            raise RuntimeError(f'TriviaSource list returned by random.choices() is malformed: \"{randomChoices}\"')

        randomlyChosenTriviaSource = randomChoices[0]
        randomlyChosenTriviaRepository = self.__triviaSourceToRepositoryMap[randomlyChosenTriviaSource]

        if randomlyChosenTriviaRepository is None:
            # this scenario should definitely be impossible, but the Python type checking was
            # getting angry without this check
            raise RuntimeError(f'Couldn\'t retrieve corresponding TriviaQuestionRepository from given randomlyChosenTriviaSource ({randomlyChosenTriviaSource=}) ({randomlyChosenTriviaRepository=}) ({self.__triviaSourceToRepositoryMap=})')

        return randomlyChosenTriviaRepository

    def __createTriviaSourceToRepositoryMap(self) -> Dict[TriviaSource, Optional[TriviaQuestionRepositoryInterface]]:
        triviaSourceToRepositoryMap: Dict[TriviaSource, Optional[TriviaQuestionRepositoryInterface]] = {
            TriviaSource.BONGO: self.__bongoTriviaQuestionRepository,
            TriviaSource.FUNTOON: self.__funtoonTriviaQuestionRepository,
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
            raise RuntimeError(f'triviaSourceToRepositoryMap is missing some members of TriviaSource!')

        return triviaSourceToRepositoryMap

    async def fetchTrivia(
        self,
        emote: str,
        triviaFetchOptions: TriviaFetchOptions
    ) -> Optional[AbsTriviaQuestion]:
        if not utils.isValidStr(emote):
            raise ValueError(f'emote argument is malformed: \"{emote}\"')
        elif not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise ValueError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        question: Optional[AbsTriviaQuestion] = None
        retryCount: int = 0
        maxRetryCount = await self.__triviaSettingsRepository.getMaxRetryCount()
        attemptedTriviaSources: List[TriviaSource] = list()

        while retryCount < maxRetryCount:
            question = await self.__retrieveSpooledTriviaQuestion(triviaFetchOptions)

            if question is None:
                triviaQuestionRepository = await self.__chooseRandomTriviaSource(triviaFetchOptions)
                triviaSource = triviaQuestionRepository.getTriviaSource()
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
            ) and await self.__verifyTriviaQuestionIsNotDuplicate(
                question = question,
                emote = emote,
                triviaFetchOptions = triviaFetchOptions
            ):
                return question

            question = None
            retryCount = retryCount + 1
            await asyncio.sleep(self.__triviaRetrySleepTimeSeconds * float(retryCount))

        raise TooManyTriviaFetchAttemptsException(f'Unable to fetch trivia from {attemptedTriviaSources} after {retryCount} attempts (max attempts is {maxRetryCount})')

    async def __getCurrentlyInvalidTriviaSources(self, triviaFetchOptions: TriviaFetchOptions) -> Set[TriviaSource]:
        if not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise ValueError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

        availableTriviaSourcesMap: Dict[TriviaSource, TriviaQuestionRepositoryInterface] = dict()
        for triviaSource, triviaQuestionRepository in self.__triviaSourceToRepositoryMap.items():
            if triviaQuestionRepository is not None and await triviaQuestionRepository.hasQuestionSetAvailable():
                availableTriviaSourcesMap[triviaSource] = triviaQuestionRepository

        currentlyInvalidTriviaSources: Set[TriviaSource] = set()

        if not triviaFetchOptions.areQuestionAnswerTriviaQuestionsEnabled():
            for triviaSource, triviaQuestionRepository in availableTriviaSourcesMap.items():
                if TriviaQuestionType.QUESTION_ANSWER in triviaQuestionRepository.getSupportedTriviaTypes():
                    currentlyInvalidTriviaSources.add(triviaSource)

        if triviaFetchOptions.requireQuestionAnswerTriviaQuestion():
            for triviaSource, triviaQuestionRepository in availableTriviaSourcesMap.items():
                if TriviaQuestionType.QUESTION_ANSWER not in triviaQuestionRepository.getSupportedTriviaTypes():
                    currentlyInvalidTriviaSources.add(triviaSource)

        if not await self.__isJServiceTriviaQuestionRepositoryAvailable():
            currentlyInvalidTriviaSources.add(TriviaSource.J_SERVICE)

        if not await self.__isLotrTriviaQuestionRepositoryAvailable():
            currentlyInvalidTriviaSources.add(TriviaSource.LORD_OF_THE_RINGS)

        if not await self.__isQuizApiTriviaQuestionRepositoryAvailable():
            currentlyInvalidTriviaSources.add(TriviaSource.QUIZ_API)

        unstableTriviaSources = await self.__getCurrentlyUnstableTriviaSources()
        currentlyInvalidTriviaSources.update(unstableTriviaSources)

        return currentlyInvalidTriviaSources

    async def __getCurrentlyUnstableTriviaSources(self) -> Set[TriviaSource]:
        instabilityThreshold = await self.__triviaSettingsRepository.getTriviaSourceInstabilityThreshold()
        unstableTriviaSources: Set[TriviaSource] = set()

        for triviaSource in TriviaSource:
            if self.__triviaSourceInstabilityHelper[triviaSource] >= instabilityThreshold:
                unstableTriviaSources.add(triviaSource)

        return unstableTriviaSources

    async def __isJServiceTriviaQuestionRepositoryAvailable(self) -> bool:
        return self.__jServiceTriviaQuestionRepository is not None

    async def __isLotrTriviaQuestionRepositoryAvailable(self) -> bool:
        return self.__lotrTriviaQuestionRepository is not None

    async def __isQuizApiTriviaQuestionRepositoryAvailable(self) -> bool:
        return self.__quizApiTriviaQuestionRepository is not None

    async def __retrieveSpooledTriviaQuestion(
        self,
        triviaFetchOptions: TriviaFetchOptions
    ) -> Optional[AbsTriviaQuestion]:
        if not isinstance(triviaFetchOptions, TriviaFetchOptions):
            raise ValueError(f'triviaFetchOptions argument is malformed: \"{triviaFetchOptions}\"')

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

    async def __spoolNewSuperTriviaQuestion(self):
        if self.__superTriviaQuestionSpool.qsize() >= await self.__triviaSettingsRepository.getMaxSuperTriviaQuestionSpoolSize():
            return

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle(),
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )

        self.__timber.log('TriviaRepository', f'Spooling up a super trivia question (current qsize: {self.__superTriviaQuestionSpool.qsize()})')
        triviaQuestionRepository = await self.__chooseRandomTriviaSource(triviaFetchOptions)
        triviaSource = triviaQuestionRepository.getTriviaSource()
        question: Optional[AbsTriviaQuestion] = None

        try:
            question = await triviaQuestionRepository.fetchTriviaQuestion(triviaFetchOptions)
        except (NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException, NoTriviaQuestionException) as e:
            self.__timber.log('TriviaRepository', f'Failed to fetch trivia question for spool due to malformed data (trivia source was \"{triviaSource}\"): {e}', e, traceback.format_exc())
        except GenericTriviaNetworkException as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered network Exception when fetching super trivia question for spool (trivia source was \"{triviaSource}\"): {e}', e, traceback.format_exc())
        except MalformedTriviaJsonException as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered malformed JSON Exception when fetching super trivia question for spool (trivia source was \"{triviaSource}\"): {e}', e, traceback.format_exc())
        except Exception as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered unknown Exception when fetching super trivia question for spool (trivia source was \"{triviaSource}\"): {e}', e, traceback.format_exc())

        if question is None:
            return
        elif question.getTriviaType() is not TriviaQuestionType.QUESTION_ANSWER or not isinstance(question, QuestionAnswerTriviaQuestion):
            self.__timber.log('TriviaRepository', f'Encountered unexpected super trivia question type ({question}) when spooling a super trivia question')
            return

        if not await self.__verifyTriviaQuestionContent(
            question = question,
            triviaFetchOptions = triviaFetchOptions
        ):
            self.__timber.log('TriviaRepository', f'Encountered bad trivia question content when spooling a super trivia question')
            return

        self.__superTriviaQuestionSpool.put(question)
        self.__timber.log('TriviaRepository', f'Finished spooling up a super trivia question (new qsize: {self.__superTriviaQuestionSpool.qsize()})')

    async def __spoolNewTriviaQuestion(self):
        if self.__triviaQuestionSpool.qsize() >= await self.__triviaSettingsRepository.getMaxTriviaQuestionSpoolSize():
            return

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = await self.__twitchHandleProvider.getTwitchHandle(),
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.NOT_ALLOWED
        )

        self.__timber.log('TriviaRepository', f'Spooling up a trivia question (current qsize: {self.__triviaQuestionSpool.qsize()})')
        triviaQuestionRepository = await self.__chooseRandomTriviaSource(triviaFetchOptions)
        triviaSource = triviaQuestionRepository.getTriviaSource()
        question: Optional[AbsTriviaQuestion] = None

        try:
            question = await triviaQuestionRepository.fetchTriviaQuestion(triviaFetchOptions)
        except (NoTriviaCorrectAnswersException, NoTriviaMultipleChoiceResponsesException, NoTriviaQuestionException) as e:
            self.__timber.log('TriviaRepository', f'Failed to fetch trivia question for spool due to malformed data (trivia source was \"{triviaSource}\"): {e}', e, traceback.format_exc())
        except GenericTriviaNetworkException as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered network Exception when fetching trivia question for spool (trivia source was \"{triviaSource}\"): {e}', e, traceback.format_exc())
        except MalformedTriviaJsonException as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered malformed JSON Exception when fetching trivia question for spool (trivia source was \"{triviaSource}\"): {e}', e, traceback.format_exc())
        except Exception as e:
            self.__triviaSourceInstabilityHelper.incrementErrorCount(triviaSource)
            self.__timber.log('TriviaRepository', f'Encountered unknown Exception when fetching trivia question for spool (trivia source was \"{triviaSource}\"): {e}', e, traceback.format_exc())

        if question is None:
            return
        elif question.getTriviaType() is TriviaQuestionType.QUESTION_ANSWER or isinstance(question, QuestionAnswerTriviaQuestion):
            self.__timber.log('TriviaRepository', f'Encountered unexpected trivia question type ({question}) when spooling a trivia question')
            return

        if not await self.__verifyTriviaQuestionContent(
            question = question,
            triviaFetchOptions = triviaFetchOptions
        ):
            self.__timber.log('TriviaRepository', f'Encountered bad trivia question content when spooling a trivia question')
            return

        self.__triviaQuestionSpool.put(question)
        self.__timber.log('TriviaRepository', f'Finished spooling up a trivia question (new qsize: {self.__triviaQuestionSpool.qsize()})')

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
        question: Optional[AbsTriviaQuestion],
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
            self.__timber.log('TriviaRepository', f'Rejected a trivia question\'s content (code=\"{triviaContentCode}\")')
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
            return True
        else:
            self.__timber.log('TriviaRepository', f'Rejected a trivia question as it ended up being a duplicate (code=\"{triviaContentCode}\")')
            return False
