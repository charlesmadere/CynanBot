import traceback
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional

import CynanBotCommon.utils as utils
from authRepository import AuthRepository
from cutenessUtils import CutenessUtils
from CynanBotCommon.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBotCommon.cuteness.cutenessLeaderboardResult import \
    CutenessLeaderboardResult
from CynanBotCommon.cuteness.cutenessRepository import CutenessRepository
from CynanBotCommon.cuteness.cutenessResult import CutenessResult
from CynanBotCommon.funtoon.funtoonRepository import FuntoonRepository
from CynanBotCommon.language.jishoHelper import JishoHelper
from CynanBotCommon.language.languageEntry import LanguageEntry
from CynanBotCommon.language.languagesRepository import LanguagesRepository
from CynanBotCommon.language.translationHelper import TranslationHelper
from CynanBotCommon.language.wordOfTheDayRepository import \
    WordOfTheDayRepository
from CynanBotCommon.location.locationsRepository import LocationsRepository
from CynanBotCommon.network.exceptions import GenericNetworkException
from CynanBotCommon.pkmn.pokepediaRepository import PokepediaRepository
from CynanBotCommon.starWars.starWarsQuotesRepository import \
    StarWarsQuotesRepository
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.timedDict import TimedDict
from CynanBotCommon.trivia.additionalTriviaAnswersRepository import \
    AdditionalTriviaAnswersRepository
from CynanBotCommon.trivia.addTriviaGameControllerResult import \
    AddTriviaGameControllerResult
from CynanBotCommon.trivia.bannedWordsRepository import BannedWordsRepository
from CynanBotCommon.trivia.checkAnswerTriviaAction import \
    CheckAnswerTriviaAction
from CynanBotCommon.trivia.checkSuperAnswerTriviaAction import \
    CheckSuperAnswerTriviaAction
from CynanBotCommon.trivia.clearSuperTriviaQueueTriviaAction import \
    ClearSuperTriviaQueueTriviaAction
from CynanBotCommon.trivia.questionAnswerTriviaConditions import \
    QuestionAnswerTriviaConditions
from CynanBotCommon.trivia.removeTriviaGameControllerResult import \
    RemoveTriviaGameControllerResult
from CynanBotCommon.trivia.shinyTriviaOccurencesRepository import \
    ShinyTriviaOccurencesRepository
from CynanBotCommon.trivia.startNewSuperTriviaGameAction import \
    StartNewSuperTriviaGameAction
from CynanBotCommon.trivia.toxicTriviaOccurencesRepository import \
    ToxicTriviaOccurencesRepository
from CynanBotCommon.trivia.triviaBanHelper import TriviaBanHelper
from CynanBotCommon.trivia.triviaEmoteGenerator import TriviaEmoteGenerator
from CynanBotCommon.trivia.triviaExceptions import (
    AdditionalTriviaAnswerAlreadyExistsException,
    AdditionalTriviaAnswerIsMalformedException,
    AdditionalTriviaAnswerIsUnsupportedTriviaTypeException,
    TooManyAdditionalTriviaAnswersException)
from CynanBotCommon.trivia.triviaFetchOptions import TriviaFetchOptions
from CynanBotCommon.trivia.triviaGameControllersRepository import \
    TriviaGameControllersRepository
from CynanBotCommon.trivia.triviaGameGlobalControllersRepository import \
    TriviaGameGlobalControllersRepository
from CynanBotCommon.trivia.triviaGameMachine import TriviaGameMachine
from CynanBotCommon.trivia.triviaHistoryRepository import \
    TriviaHistoryRepository
from CynanBotCommon.trivia.triviaScoreRepository import TriviaScoreRepository
from CynanBotCommon.trivia.triviaSettingsRepository import \
    TriviaSettingsRepository
from CynanBotCommon.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBotCommon.users.userIdsRepository import UserIdsRepository
from CynanBotCommon.weather.weatherRepository import WeatherRepository
from generalSettingsRepository import GeneralSettingsRepository
from generalSettingsRepositorySnapshot import GeneralSettingsRepositorySnapshot
from triviaUtils import TriviaUtils
from twitch.twitchContext import TwitchContext
from twitch.twitchUtils import TwitchUtils
from users.modifyUserActionType import ModifyUserActionType
from users.modifyUserDataHelper import ModifyUserDataHelper
from users.user import User
from users.usersRepository import UsersRepository


class AbsCommand(ABC):

    @abstractmethod
    async def handleCommand(self, ctx: TwitchContext):
        pass


class AddGlobalTriviaControllerCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        timber: Timber,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepository,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepository):
            raise ValueError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__timber: Timber = timber
        self.__triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepository = triviaGameGlobalControllersRepository
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        if ctx.getAuthorId() != administrator:
            self.__timber.log('AddGlobalTriviaControllerCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddGlobalTriviaControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add global trivia controller as no username argument was given. Example: !addglobaltriviacontroller {administrator}')
            return

        userName: Optional[str] = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('AddGlobalTriviaControllerCommand', f'Attempted to handle command for {userName}:{ctx.getAuthorId()} in {user.getHandle()}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add global trivia controller as username argument is malformed. Example: !addglobaltriviacontroller {user.getHandle()}')
            return

        result = await self.__triviaGameGlobalControllersRepository.addController(
            userName = userName
        )

        if result is AddTriviaGameControllerResult.ADDED:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Added {userName} as a global trivia game controller.')
        elif result is AddTriviaGameControllerResult.ALREADY_EXISTS:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Tried adding {userName} as a global trivia game controller, but they already were one.')
        elif result is AddTriviaGameControllerResult.ERROR:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An error occurred when trying to add {userName} as a global trivia game controller!')
        else:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An unknown error occurred when trying to add {userName} as a global trivia game controller!')
            self.__timber.log('AddGlobalTriviaControllerCommand', f'Encountered unknown AddTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a global trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            raise ValueError(f'Encountered unknown AddTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a global trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

        self.__timber.log('AddGlobalTriviaControllerCommand', f'Handled !addglobaltriviacontroller command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}')


class AddTriviaAnswerCommand(AbsCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaEmoteGenerator: TriviaEmoteGenerator,
        triviaHistoryRepository: TriviaHistoryRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        answerDelimiter: str = ', '
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepository):
            raise ValueError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGenerator):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepository):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(answerDelimiter, str):
            raise ValueError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepository = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaEmoteGenerator: TriviaEmoteGenerator = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepository = triviaHistoryRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__answerDelimiter: str = answerDelimiter

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 3:
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but not enough arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add additional trivia answer as not enough arguments were given. Example: !addtriviaanswer {self.__triviaEmoteGenerator.getRandomEmote()} Theodore Roosevelt')
            return

        emote: Optional[str] = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add additional trivia answer as an invalid emote argument was given. Example: !addtriviaanswer {self.__triviaEmoteGenerator.getRandomEmote()} Theodore Roosevelt')
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.getHandle()
        )

        if reference is None:
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")')
            return

        additionalAnswer: Optional[str] = ' '.join(splits[2:])
        if not utils.isValidStr(additionalAnswer):
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid additional answer was given: \"{additionalAnswer}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add additional trivia answer as an invalid answer argument was given. Example: !addtriviaanswer {self.__triviaEmoteGenerator.getRandomEmote()} Theodore Roosevelt')
            return

        try:
            result = await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswer(
                additionalAnswer = additionalAnswer,
                triviaId = reference.getTriviaId(),
                triviaSource = reference.getTriviaSource(),
                triviaType = reference.getTriviaType()
            )

            additionalAnswers = self.__answerDelimiter.join(result.getAdditionalAnswers())
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} Added additional trivia answer for {result.getTriviaSource().toStr()}:{result.getTriviaId()} — {additionalAnswers}')
            self.__timber.log('AddTriviaAnswerCommand', f'Added additional trivia answer for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}: \"{additionalAnswer}\"')
        except AdditionalTriviaAnswerAlreadyExistsException as e:
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} Unable to add additional trivia answer for {reference.getTriviaSource().toStr()}:{reference.getTriviaId()} as it already exists')
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but the additional answer already exists: \"{additionalAnswer}\"', e, traceback.format_exc())
        except AdditionalTriviaAnswerIsMalformedException as e:
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} Unable to add additional trivia answer for {reference.getTriviaSource().toStr()}:{reference.getTriviaId()} as it is malformed')
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but the additional answer is malformed: \"{additionalAnswer}\"', e, traceback.format_exc())
        except AdditionalTriviaAnswerIsUnsupportedTriviaTypeException as e:
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} Unable to add additional trivia answer for {reference.getTriviaSource().toStr()}:{reference.getTriviaId()} as the question is an unsupported type ({reference.getTriviaType().toStr()})')
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but the question is an unsupported type: \"{reference.getTriviaType().toStr()}\"', e, traceback.format_exc())
        except TooManyAdditionalTriviaAnswersException as e:
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} Unable to add additional trivia answer for {reference.getTriviaSource().toStr()}:{reference.getTriviaId()} as the question has too many additional answers ({reference.getTriviaType().toStr()})')
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but the question has too many additional answers', e, traceback.format_exc())

        self.__timber.log('AddTriviaAnswerCommand', f'Handled !addtriviaanswer command with for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class AddTriviaControllerCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameControllersRepository: TriviaGameControllersRepository,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepository):
            raise ValueError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameControllersRepository: TriviaGameControllersRepository = triviaGameControllersRepository
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return

        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        if user.getHandle().lower() != ctx.getAuthorName() and administrator != ctx.getAuthorId():
            self.__timber.log('AddTriviaGameControllerCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddTriviaGameControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add trivia controller as no username argument was given. Example: !addtriviacontroller {user.getHandle()}')
            return

        userName: Optional[str] = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('AddTriviaGameControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add trivia controller as username argument is malformed. Example: !addtriviacontroller {user.getHandle()}')
            return

        result = await self.__triviaGameControllersRepository.addController(
            twitchChannel = user.getHandle(),
            userName = userName
        )

        if result is AddTriviaGameControllerResult.ADDED:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Added {userName} as a trivia game controller.')
        elif result is AddTriviaGameControllerResult.ALREADY_EXISTS:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Tried adding {userName} as a trivia game controller, but they already were one.')
        elif result is AddTriviaGameControllerResult.ERROR:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An error occurred when trying to add {userName} as a trivia game controller!')
        else:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An unknown error occurred when trying to add {userName} as a trivia game controller!')
            self.__timber.log('AddTriviaControllerCommand', f'Encountered unknown AddTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            raise ValueError(f'Encountered unknown AddTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

        self.__timber.log('AddTriviaControllerCommand', f'Handled !addtriviacontroller command with {result} result for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class AddUserCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: Timber,
        twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepositoryInterface, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepositoryInterface}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__timber: Timber = timber
        self.__twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface = twitchTokensRepositoryInterface
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        if ctx.getAuthorId() != administrator:
            self.__timber.log('AddUserCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddUserCommand', f'Not enough arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !adduser command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username argument is necessary for the !adduser command. Example: !adduser {user.getHandle()}')
            return

        userName: Optional[str] = utils.removePreceedingAt(splits[1])

        if not utils.isValidStr(userName):
            self.__timber.log('AddUserCommand', f'Invalid username argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !adduser command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username argument is necessary for the !adduser command. Example: !adduser {user.getHandle()}')
            return

        if await self.__usersRepository.containsUserAsync(userName):
            self.__timber.log('AddUserCommand', f'Username argument (\"{userName}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} already exists as a user')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add \"{userName}\" as this user already exists!')
            return

        userId: Optional[str] = None

        try:
            userId = await self.__userIdsRepository.fetchUserId(
                userName = userName,
                twitchAccessToken = await self.__twitchTokensRepositoryInterface.getAccessToken(user.getHandle())
            )
        except GenericNetworkException as e:
            self.__timber.log('AddUserCommand', f'Unable to fetch userId for \"{userName}\" due to a generic network exception: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to fetch user ID for \"{userName}\" due to a generic network error!')
            return
        except RuntimeError as e:
            self.__timber.log('AddUserCommand', f'Unable to fetch userId for \"{userName}\" due to an internal error: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to fetch user ID for \"{userName}\" due to an internal error!')
            return

        if not utils.isValidStr(userId):
            self.__timber.log('AddUserCommand', f'Failed to fetch userId for \"{userName}\" due to an unknown internal error')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Failed to fetch user ID for \"{userName}\" due to an unknown internal error')
            return

        await self.__modifyUserDataHelper.setUserData(
            actionType = ModifyUserActionType.ADD,
            userId = userId,
            userName = userName
        )

        await self.__twitchUtils.safeSend(ctx, f'ⓘ To add user \"{userName}\" ({userId}), please respond with `!confirm`')
        self.__timber.log('AddUserCommand', f'Handled !adduser command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class AnswerCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameMachine: TriviaGameMachine,
        usersRepository: UsersRepository
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachine):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled():
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            return

        answer = ' '.join(splits[1:])

        self.__triviaGameMachine.submitAction(CheckAnswerTriviaAction(
            answer = answer,
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId(),
            userName = ctx.getAuthorName()
        ))

        self.__timber.log('AnswerCommand', f'Handled !answer command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class BanTriviaQuestionCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaBanHelper: TriviaBanHelper,
        triviaEmoteGenerator: TriviaEmoteGenerator,
        triviaHistoryRepository: TriviaHistoryRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaBanHelper, TriviaBanHelper):
            raise ValueError(f'triviaBanHelper argument is malformed: \"{triviaBanHelper}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGenerator):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepository):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaBanHelper: TriviaBanHelper = triviaBanHelper
        self.__triviaEmoteGenerator: TriviaEmoteGenerator = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepository = triviaHistoryRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('BanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to ban trivia question as no emote argument was given. Example: !bantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        emote: Optional[str] = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('BanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to ban trivia question as an invalid emote argument was given. Example: !bantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.getHandle()
        )

        if reference is None:
            self.__timber.log('BanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")')
            return

        await self.__triviaBanHelper.ban(
            triviaId = reference.getTriviaId(),
            triviaSource = reference.getTriviaSource()
        )

        await self.__twitchUtils.safeSend(ctx, f'{normalizedEmote} Banned trivia question {reference.getTriviaSource().toStr()} — {reference.getTriviaId()}')
        self.__timber.log('BanTriviaQuestionCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} ({normalizedEmote}) ({reference.getTriviaSource().toStr()}:{reference.getTriviaId()} was banned)')


class ClearCachesCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        authRepository: AuthRepository,
        bannedWordsRepository: Optional[BannedWordsRepository],
        funtoonRepository: Optional[FuntoonRepository],
        generalSettingsRepository: GeneralSettingsRepository,
        locationsRepository: Optional[LocationsRepository],
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: Timber,
        triviaSettingsRepository: Optional[TriviaSettingsRepository],
        twitchTokensRepositoryInterface: Optional[TwitchTokensRepositoryInterface],
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        weatherRepository: Optional[WeatherRepository],
        wordOfTheDayRepository: Optional[WordOfTheDayRepository]
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__authRepository: AuthRepository = authRepository
        self.__bannedWordsRepository: Optional[BannedWordsRepository] = bannedWordsRepository
        self.__funtoonRepository: Optional[FuntoonRepository] = funtoonRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__locationsRepository: Optional[LocationsRepository] = locationsRepository
        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__timber: Timber = timber
        self.__triviaSettingsRepository: Optional[TriviaSettingsRepository] = triviaSettingsRepository
        self.__twitchTokensRepositoryInterface: Optional[TwitchTokensRepositoryInterface] = twitchTokensRepositoryInterface
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__weatherRepository: Optional[WeatherRepository] = weatherRepository
        self.__wordOfTheDayRepository: Optional[WordOfTheDayRepository] = wordOfTheDayRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        if administrator != ctx.getAuthorId():
            self.__timber.log('ClearCachesCommand', f'Attempted use of !clearcaches command by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            return

        await self.__authRepository.clearCaches()

        if self.__bannedWordsRepository is not None:
            await self.__bannedWordsRepository.clearCaches()

        if self.__funtoonRepository is not None:
            await self.__funtoonRepository.clearCaches()

        await self.__generalSettingsRepository.clearCaches()

        if self.__locationsRepository is not None:
            await self.__locationsRepository.clearCaches()

        await self.__modifyUserDataHelper.clearCaches()

        if self.__triviaSettingsRepository is not None:
            await self.__triviaSettingsRepository.clearCaches()

        if self.__twitchTokensRepositoryInterface is not None:
            await self.__twitchTokensRepositoryInterface.clearCaches()

        await self.__usersRepository.clearCaches()

        if self.__weatherRepository is not None:
            await self.__weatherRepository.clearCaches()

        if self.__wordOfTheDayRepository is not None:
            await self.__wordOfTheDayRepository.clearCaches()

        await self.__twitchUtils.safeSend(ctx, 'ⓘ All caches cleared')
        self.__timber.log('ClearCachesCommand', f'Handled !clearcaches command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class ClearSuperTriviaQueueCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameMachine: TriviaGameMachine,
        triviaUtils: TriviaUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachine):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId()
        ):
            return

        self.__triviaGameMachine.submitAction(ClearSuperTriviaQueueTriviaAction(
            twitchChannel = user.getHandle()
        ))

        self.__timber.log('ClearSuperTriviaQueueCommand', f'Handled !clearsupertriviaqueue command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class CommandsCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaUtils: Optional[TriviaUtils],
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaUtils is not None and not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaUtils: Optional[TriviaUtils] = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def __buildLanguageCommandsList(
        self,
        generalSettings: GeneralSettingsRepositorySnapshot,
        user: User
    ) -> List[str]:
        if not isinstance(generalSettings, GeneralSettingsRepositorySnapshot):
            raise ValueError(f'generalSettings argument is malformed: \"{generalSettings}\"')
        elif not isinstance(user, User):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        commands: List[str] = list()

        if generalSettings.isJishoEnabled() and user.isJishoEnabled():
            commands.append('!jisho')

        if generalSettings.isTranslateEnabled() and user.isTranslateEnabled():
            commands.append('!translate')

        if generalSettings.isWordOfTheDayEnabled() and user.isWordOfTheDayEnabled():
            commands.append('!word')

        return commands

    async def __buildPkmnCommandsList(
        self,
        generalSettings: GeneralSettingsRepositorySnapshot,
        user: User
    ) -> List[str]:
        if not isinstance(generalSettings, GeneralSettingsRepositorySnapshot):
            raise ValueError(f'generalSettings argument is malformed: \"{generalSettings}\"')
        elif not isinstance(user, User):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        commands: List[str] = list()

        if generalSettings.isPokepediaEnabled() and user.isPokepediaEnabled():
            commands.append('!pkmon')
            commands.append('!pkmove')

        return commands

    async def __buildTriviaCommandsList(
        self,
        isMod: bool,
        generalSettings: GeneralSettingsRepositorySnapshot,
        userId: str,
        userName: str,
        user: User
    ) -> List[str]:
        if not utils.isValidBool(isMod):
            raise ValueError(f'isMod argument is malformed: \"{isMod}\"')
        elif not isinstance(generalSettings, GeneralSettingsRepositorySnapshot):
            raise ValueError(f'generalSettings argument is malformed: \"{generalSettings}\"')
        elif not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(user, User):
            raise ValueError(f'user argument is malformed: \"{user}\"')

        isPrivilegedTriviaUser = self.__triviaUtils is not None and await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = userId
        )

        userName = userName.lower()
        commands: List[str] = list()

        if userName == user.getHandle().lower():
            commands.append('!addtriviacontroller')
            commands.append('!gettriviacontrollers')
            commands.append('!removetriviacontroller')

        if isPrivilegedTriviaUser:
            commands.append('!bantriviaquestion')

            if user.isSuperTriviaGameEnabled():
                commands.append('!clearsupertriviaqueue')
                commands.append('!supertrivia')

            if user.isTriviaGameEnabled() or user.isSuperTriviaGameEnabled():
                commands.append('!triviainfo')

        if user.isCutenessEnabled():
            commands.append('!cuteness')
            commands.append('!cutenesschampions')
            commands.append('!cutenesshistory')
            commands.append('!mycutenesshistory')

            if isMod and user.isGiveCutenessEnabled():
                commands.append('!givecuteness')

        if (generalSettings.isTriviaGameEnabled() and user.isTriviaGameEnabled()) or (generalSettings.isSuperTriviaGameEnabled() and user.isSuperTriviaGameEnabled()):
            commands.append('!triviascore')

        return commands

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not ctx.isAuthorMod() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        commands: List[str] = list()

        if user.hasDiscord():
            commands.append('!discord')

        if user.hasSpeedrunProfile():
            commands.append('!pbs')

        if user.hasTimeZones():
            commands.append('!time')

        if user.hasTwitter():
            commands.append('!twitter')

        if generalSettings.isWeatherEnabled() and user.isWeatherEnabled():
            commands.append('!weather')

        commands.extend(await self.__buildTriviaCommandsList(
            isMod = ctx.isAuthorMod(),
            generalSettings = generalSettings,
            userId = ctx.getAuthorId(),
            userName = ctx.getAuthorName(),
            user = user
        ))

        commands.extend(await self.__buildPkmnCommandsList(
            generalSettings = generalSettings,
            user = user
        ))

        commands.extend(await self.__buildLanguageCommandsList(
            generalSettings = generalSettings,
            user = user
        ))

        if user.isCynanSourceEnabled():
            commands.append('!cynansource')

        if not utils.hasItems(commands):
            return

        commandsString = self.__delimiter.join(commands)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Available commands: {commandsString}')
        self.__timber.log('CommandsCommand', f'Handled !commands command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class ConfirmCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        if ctx.getAuthorId() != administrator:
            self.__timber.log('ConfirmCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        userData = await self.__modifyUserDataHelper.getUserData()

        if userData is None:
            self.__timber.log('ConfirmCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried confirming the modification of a user, but there is no persisted user data')
            return

        if userData.getActionType() is ModifyUserActionType.ADD:
            await self.__usersRepository.addUser(userData.getUserName())
        elif userData.getActionType() is ModifyUserActionType.REMOVE:
            await self.__usersRepository.removeUser(userData.getUserName())
        else:
            raise RuntimeError(f'unknown ModifyUserActionType: \"{userData.getActionType()}\"')

        await self.__modifyUserDataHelper.notifyModifyUserListenerAndClearData()
        self.__timber.log('CommandsCommand', f'Handled !confirm command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class CutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        cutenessUtils: CutenessUtils,
        timber: Timber,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(cutenessRepository, CutenessRepository):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtils):
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__cutenessUtils: CutenessUtils = cutenessUtils
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    def __cutenessLeaderboardResultToStr(self, result: CutenessLeaderboardResult) -> str:
        if not isinstance(result, CutenessLeaderboardResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')

        if not result.hasEntries():
            return f'{result.getCutenessDate().toStr()} Leaderboard is empty 😿'

        specificLookupText: Optional[str] = None
        if result.hasSpecificLookupCutenessResult():
            userName = result.getSpecificLookupCutenessResult().getUserName()
            cutenessStr = result.getSpecificLookupCutenessResult().getCutenessStr()
            specificLookupText = f'@{userName} your cuteness is {cutenessStr}'

        leaderboard = self.__cutenessUtils.getLeaderboard(
            entries = result.getEntries(),
            delimiter = self.__delimiter
        )

        if utils.isValidStr(specificLookupText):
            return f'{specificLookupText}, and the {result.getCutenessDate().toStr()} Leaderboard is: {leaderboard} ✨'
        else:
            return f'{result.getCutenessDate().toStr()} Leaderboard {leaderboard} ✨'

    def __cutenessResultToStr(self, result: CutenessResult) -> str:
        if not isinstance(result, CutenessResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')

        if result.hasCuteness() and result.getCuteness() >= 1:
            return f'{result.getUserName()}\'s {result.getCutenessDate().toStr()} cuteness is {result.getCutenessStr()} ✨'
        else:
            return f'{result.getUserName()} has no cuteness in {result.getCutenessDate().toStr()}'

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())

        userId: str = None
        userName: str = None

        if len(splits) >= 2:
            userName = utils.removePreceedingAt(splits[1])
        else:
            userName = ctx.getAuthorName()

        # this means that a user is querying for another user's cuteness
        if userName.lower() != ctx.getAuthorName().lower():
            try:
                userId = await self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError) as e:
                self.__timber.log('CutenessCommand', f'Unable to find user ID for \"{userName}\" in the database: {e}', e, traceback.format_exc())
                await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return

            result = await self.__cutenessRepository.fetchCuteness(
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = userName
            )

            await self.__twitchUtils.safeSend(ctx, self.__cutenessResultToStr(result))
        else:
            userId = ctx.getAuthorId()

            result = await self.__cutenessRepository.fetchCutenessLeaderboard(
                twitchChannel = user.getHandle(),
                specificLookupUserId = userId,
                specificLookupUserName = userName
            )

            await self.__twitchUtils.safeSend(ctx, self.__cutenessLeaderboardResultToStr(result))

        self.__timber.log('CutenessCommand', f'Handled !cuteness command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class CutenessChampionsCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        cutenessUtils: CutenessUtils,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if not isinstance(cutenessRepository, CutenessRepository):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtils):
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__cutenessUtils: CutenessUtils = cutenessUtils
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        result = await self.__cutenessRepository.fetchCutenessChampions(
            twitchChannel = user.getHandle()
        )

        await self.__twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessChampions(result, self.__delimiter))
        self.__timber.log('CutenessChampionsCommand', f'Handled !cutenesschampions command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class CutenessHistoryCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        cutenessUtils: CutenessUtils,
        timber: Timber,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        entryDelimiter: str = ', ',
        leaderboardDelimiter: str = ' — ',
        cooldown: timedelta = timedelta(seconds = 5)
    ):
        if not isinstance(cutenessRepository, CutenessRepository):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtils):
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(entryDelimiter, str):
            raise ValueError(f'entryDelimiter argument is malformed: \"{entryDelimiter}\"')
        elif not isinstance(leaderboardDelimiter, str):
            raise ValueError(f'leaderboardDelimiter argument is malformed: \"{leaderboardDelimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__cutenessUtils: CutenessUtils = cutenessUtils
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__entryDelimiter: str = entryDelimiter
        self.__leaderboardDelimiter: str = leaderboardDelimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())

        userName: str = None
        if len(splits) >= 2:
            userName = utils.removePreceedingAt(splits[1])
        else:
            userName = ctx.getAuthorName()

        userId: Optional[str] = None

        # this means that a user is querying for another user's cuteness history
        if userName.lower() != ctx.getAuthorName().lower():
            try:
                userId = await self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError):
                # this exception can be safely ignored
                pass

            if not utils.isValidStr(userId):
                self.__timber.log('CutenessHistoryCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return

            result = await self.__cutenessRepository.fetchCutenessHistory(
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = userName
            )

            await self.__twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessHistory(result, self.__entryDelimiter))
        else:
            result = await self.__cutenessRepository.fetchCutenessLeaderboardHistory(
                twitchChannel = user.getHandle()
            )

            await self.__twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessLeaderboardHistory(
                result = result,
                entryDelimiter = self.__entryDelimiter,
                leaderboardDelimiter = self.__leaderboardDelimiter
            ))

        self.__timber.log('CutenessHistoryCommand', f'Handled !cutenesshistory command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class CynanSourceCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCynanSourceEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(ctx.getTwitchChannelName()):
            return

        await self.__twitchUtils.safeSend(ctx, 'My source code is available here: https://github.com/charlesmadere/cynanbot')
        self.__timber.log('CynanSourceCommand', f'Handled !cynansource command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class DeleteTriviaAnswersCommand(AbsCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaEmoteGenerator: TriviaEmoteGenerator,
        triviaHistoryRepository: TriviaHistoryRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        answerDelimiter: str = ', '
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepository):
            raise ValueError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGenerator):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepository):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(answerDelimiter, str):
            raise ValueError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepository = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaEmoteGenerator: TriviaEmoteGenerator = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepository = triviaHistoryRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__answerDelimiter: str = answerDelimiter

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('DeleteTriviaAnswersCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but not enough arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to delete additional trivia answers as not enough arguments were given. Example: !deletetriviaanswers {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        emote: Optional[str] = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('DeleteTriviaAnswersCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to delete additional trivia answers as an invalid emote argument was given. Example: !deletetriviaanswers {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.getHandle()
        )

        if reference is None:
            self.__timber.log('DeleteTriviaAnswersCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")')
            return

        result = await self.__additionalTriviaAnswersRepository.deleteAdditionalTriviaAnswers(
            triviaId = reference.getTriviaId(),
            triviaSource = reference.getTriviaSource(),
            triviaType = reference.getTriviaType()
        )

        if result is None:
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} There are no additional trivia answers for {reference.getTriviaSource().toStr()}:{reference.getTriviaId()}')
        else:
            additionalAnswers = self.__answerDelimiter.join(result.getAdditionalAnswers())
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} Deleted additional trivia answers for {result.getTriviaSource().toStr()}:{result.getTriviaId()} — {additionalAnswers}')

        self.__timber.log('DeleteTriviaAnswersCommand', f'Handled !deletetriviaanswers command with {result} for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class DiscordCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.hasDiscord():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await self.__twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s discord: {user.getDiscordUrl()}')
        self.__timber.log('DiscordCommand', f'Handled !discord command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class GetGlobalTriviaControllersCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        timber: Timber,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepository):
            raise ValueError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__timber: Timber = timber
        self.__triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepository = triviaGameGlobalControllersRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        userName = ctx.getAuthorName().lower()

        if user.getHandle().lower() != userName and ctx.getAuthorId() != administrator:
            self.__timber.log('GetGlobalTriviaControllersCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        controllers = await self.__triviaGameGlobalControllersRepository.getControllers()
        await self.__twitchUtils.safeSend(ctx, await self.__triviaUtils.getTriviaGameGlobalControllers(controllers))
        self.__timber.log('GetGlobalTriviaControllersCommand', f'Handled !getglobaltriviacontrollers command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class GetTriviaAnswersCommand(AbsCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaEmoteGenerator: TriviaEmoteGenerator,
        triviaHistoryRepository: TriviaHistoryRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        answerDelimiter: str = ', '
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepository):
            raise ValueError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGenerator):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepository):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(answerDelimiter, str):
            raise ValueError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepository = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaEmoteGenerator: TriviaEmoteGenerator = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepository = triviaHistoryRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__answerDelimiter: str = answerDelimiter

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('GetTriviaAnswersCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but not enough arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to get additional trivia answers as not enough arguments were given. Example: !gettriviaanswers {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        emote: Optional[str] = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('GetTriviaAnswersCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to get additional trivia answers as an invalid emote argument was given. Example: !gettriviaanswers {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.getHandle()
        )

        if reference is None:
            self.__timber.log('GetTriviaAnswersCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")')
            return

        result = await self.__additionalTriviaAnswersRepository.getAdditionalTriviaAnswers(
            triviaId = reference.getTriviaId(),
            triviaSource = reference.getTriviaSource(),
            triviaType = reference.getTriviaType()
        )

        if result is None:
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} There are no additional trivia answers for {reference.getTriviaSource().toStr()}:{reference.getTriviaId()}')
        else:
            additionalAnswers = self.__answerDelimiter.join(result.getAdditionalAnswers())
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} Additional trivia answers for {result.getTriviaSource().toStr()}:{result.getTriviaId()} — {additionalAnswers}')

        self.__timber.log('GetTriviaAnswersCommand', f'Handled !gettriviaanswers command with {result} for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class GetTriviaControllersCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameControllersRepository: TriviaGameControllersRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepository):
            raise ValueError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameControllersRepository: TriviaGameControllersRepository = triviaGameControllersRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return

        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        if user.getHandle().lower() != ctx.getAuthorName().lower() and administrator != ctx.getAuthorId():
            self.__timber.log('GetTriviaControllersCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        controllers = await self.__triviaGameControllersRepository.getControllers(user.getHandle())
        await self.__twitchUtils.safeSend(ctx, await self.__triviaUtils.getTriviaGameControllers(controllers))
        self.__timber.log('GetTriviaControllersCommand', f'Handled !gettriviacontrollers command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class GiveCutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        timber: Timber,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository
    ):
        if not isinstance(cutenessRepository, CutenessRepository):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__timber: Timber = timber
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled() or not user.isGiveCutenessEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 3:
            self.__timber.log('GiveCutenessCommand', f'Less than 3 arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username and amount is necessary for the !givecuteness command. Example: !givecuteness {user.getHandle()} 5')
            return

        userName: str = splits[1]
        if not utils.isValidStr(userName):
            self.__timber.log('GiveCutenessCommand', f'Username given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        incrementAmountStr: str = splits[2]
        if not utils.isValidStr(incrementAmountStr):
            self.__timber.log('GiveCutenessCommand', f'Increment amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is malformed: \"{incrementAmountStr}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        try:
            incrementAmount = int(incrementAmountStr)
        except (SyntaxError, TypeError, ValueError) as e:
            self.__timber.log('GiveCutenessCommand', f'Unable to convert increment amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} into an int: \"{incrementAmountStr}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Increment amount argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        userName = utils.removePreceedingAt(userName)

        try:
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)
        except ValueError:
            self.__timber.log('GiveCutenessCommand', f'Unable to give {incrementAmount} cuteness from {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} to \"{userName}\", they don\'t current exist in the database')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to give cuteness to \"{userName}\", they don\'t currently exist in the database')
            return

        try:
            result = await self.__cutenessRepository.fetchCutenessIncrementedBy(
                incrementAmount = incrementAmount,
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = userName
            )

            await self.__twitchUtils.safeSend(ctx, f'✨ Cuteness for {userName} is now {result.getCutenessStr()} ✨')
        except (OverflowError, ValueError) as e:
            self.__timber.log('GiveCutenessCommand', f'Error giving {incrementAmount} cuteness from {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} to {userName}:{userId} in {user.getHandle()}: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error giving cuteness to \"{userName}\"')

        self.__timber.log('GiveCutenessCommand', f'Handled !givecuteness command of {incrementAmount} for {userName}:{userId} from {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class JishoCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        jishoHelper: JishoHelper,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(jishoHelper, JishoHelper):
            raise ValueError(f'jishoHelper argument is malformed: \"{jishoHelper}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__jishoHelper: JishoHelper = jishoHelper
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isJishoEnabled():
            return
        elif not user.isJishoEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReady(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, '⚠ A search term is necessary for the !jisho command. Example: !jisho 食べる')
            return

        query: Optional[str] = splits[1]
        self.__lastMessageTimes.update(user.getHandle())

        try:
            result = await self.__jishoHelper.search(query)

            for string in result.toStrList():
                await self.__twitchUtils.safeSend(ctx, string)
        except (RuntimeError, ValueError) as e:
            self.__timber.log('JishoCommand', f'Error searching Jisho for \"{query}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error searching Jisho for \"{query}\"')

        self.__timber.log('JishoCommand', f'Handled !jisho command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class LoremIpsumCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isLoremIpsumEnabled():
            return
        elif not ctx.isAuthorMod() or ctx.getAuthorName().lower() != user.getHandle().lower():
            return

        loremIpsumText = ''
        if utils.randomBool():
            loremIpsumText = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eu scelerisque felis imperdiet proin. Id donec ultrices tincidunt arcu non sodales neque sodales. Amet consectetur adipiscing elit ut aliquam. Mattis pellentesque id nibh tortor id. Suspendisse interdum consectetur libero id faucibus nisl tincidunt. Amet cursus sit amet dictum sit amet justo. Sem integer vitae justo eget magna fermentum iaculis eu non. Augue ut lectus arcu bibendum at varius vel. Risus nullam eget felis eget nunc. Enim eu turpis egestas pretium aenean pharetra magna.'
        else:
            loremIpsumText = 'Bacon ipsum dolor amet t-bone sirloin tenderloin pork belly, shoulder landjaeger boudin. Leberkas short loin jowl short ribs, strip steak beef ribs flank pork belly ham corned beef. Spare ribs turkey sausage, tenderloin boudin brisket chislic shankle. Beef ribs ball tip ham hock beef t-bone porchetta bacon bresaola chislic swine. Pork meatball pancetta, jerky chuck burgdoggen tongue jowl fatback cupim doner rump flank landjaeger. Doner salami venison buffalo rump pork chop landjaeger jowl leberkas tail bresaola brisket spare ribs tri-tip sausage.'

        await self.__twitchUtils.safeSend(ctx, loremIpsumText)
        self.__timber.log('LoremIpsumCommand', f'Handled !lorem command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class MyCutenessHistoryCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepository,
        cutenessUtils: CutenessUtils,
        timber: Timber,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(cutenessRepository, CutenessRepository):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtils):
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepository = cutenessRepository
        self.__cutenessUtils: CutenessUtils = cutenessUtils
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())

        userName: str = None
        if len(splits) >= 2:
            userName = utils.removePreceedingAt(splits[1])
        else:
            userName = ctx.getAuthorName()

        userId: str = None

        # this means that a user is querying for another user's cuteness history
        if userName.lower() != ctx.getAuthorName().lower():
            try:
                userId = await self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError):
                self.__timber.log('MyCutenessHistoryCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return
        else:
            userId = ctx.getAuthorId()

        result = await self.__cutenessRepository.fetchCutenessHistory(
            twitchChannel = user.getHandle(),
            userId = userId,
            userName = userName
        )

        await self.__twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessHistory(result, self.__delimiter))
        self.__timber.log('MyCutenessHistoryCommand', f'Handled !mycutenesshistory command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class PbsCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.hasSpeedrunProfile():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await self.__twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s speedrun profile: {user.getSpeedrunProfile()}')
        self.__timber.log('PbsCommand', f'Handled !pbs command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class PkMonCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        pokepediaRepository: PokepediaRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 10)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(pokepediaRepository, PokepediaRepository):
            raise ValueError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__pokepediaRepository: PokepediaRepository = pokepediaRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isPokepediaEnabled():
            return
        elif not user.isPokepediaEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, '⚠ A Pokémon name is necessary for the !pkmon command. Example: !pkmon charizard')
            return

        name: str = splits[1]

        try:
            mon = await self.__pokepediaRepository.searchPokemon(name)

            for string in mon.toStrList():
                await self.__twitchUtils.safeSend(ctx, string)
        except (RuntimeError, ValueError) as e:
            self.__timber.log('PkMonCommand', f'Error retrieving Pokemon \"{name}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error retrieving Pokémon \"{name}\"')

        self.__timber.log('PkMonCommand', f'Handled !pkmon command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class PkMoveCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        pokepediaRepository: PokepediaRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 10)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(pokepediaRepository, PokepediaRepository):
            raise ValueError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__pokepediaRepository: PokepediaRepository = pokepediaRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isPokepediaEnabled():
            return
        elif not user.isPokepediaEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, '⚠ A move name is necessary for the !pkmove command. Example: !pkmove fire spin')
            return

        name = ' '.join(splits[1:])

        try:
            move = await self.__pokepediaRepository.searchMoves(name)

            for string in move.toStrList():
                await self.__twitchUtils.safeSend(ctx, string)
        except (RuntimeError, ValueError) as e:
            self.__timber.log('PkMoveCommand', f'Error retrieving Pokemon move: \"{name}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error retrieving Pokémon move: \"{name}\"')

        self.__timber.log('PkMoveCommand', f'Handled !pkmove command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class RaceCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastRaceMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        if not ctx.isAuthorMod():
            return

        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isRaceEnabled():
            return
        elif not self.__lastRaceMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await self.__twitchUtils.safeSend(ctx, '!race')
        self.__timber.log('RaceCommand', f'Handled !race command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class RemoveGlobalTriviaControllerCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepository,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepository):
            raise ValueError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepository = triviaGameGlobalControllersRepository
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return

        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        if user.getHandle().lower() != ctx.getAuthorName().lower() and administrator != ctx.getAuthorId():
            self.__timber.log('RemoveGlobalTriviaControllerCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('RemoveGlobalTriviaControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to remove global trivia controller as no username argument was given. Example: !removeglobaltriviacontroller {user.getHandle()}')
            return

        userName: Optional[str] = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('RemoveGlobalTriviaControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to remove global trivia controller as username argument is malformed. Example: !removeglobaltriviacontroller {user.getHandle()}')
            return

        result = await self.__triviaGameGlobalControllersRepository.removeController(
            userName = userName
        )

        if result is RemoveTriviaGameControllerResult.REMOVED:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Removed {userName} as a global trivia game controller.')
        elif result is RemoveTriviaGameControllerResult.ERROR:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An error occurred when trying to remove {userName} as a global trivia game controller!')
        else:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An unknown error occurred when trying to remove {userName} as a global trivia game controller!')
            self.__timber.log('RemoveGlobalTriviaControllerCommand', f'Encountered unknown RemoveTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a global trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            raise ValueError(f'Encountered unknown RemoveTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a global trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

        self.__timber.log('RemoveGlobalTriviaControllerCommand', f'Handled !removeglobaltriviacontroller command with {result} result for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class RemoveTriviaControllerCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameControllersRepository: TriviaGameControllersRepository,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepository):
            raise ValueError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameControllersRepository: TriviaGameControllersRepository = triviaGameControllersRepository
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return

        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        if user.getHandle().lower() != ctx.getAuthorName().lower() and administrator != ctx.getAuthorId():
            self.__timber.log('RemoveTriviaControllerCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('RemoveTriviaControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to remove trivia controller as no username argument was given. Example: !removetriviacontroller {user.getHandle()}')
            return

        userName: Optional[str] = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('RemoveTriviaControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to remove trivia controller as username argument is malformed. Example: !removetriviacontroller {user.getHandle()}')
            return

        result = await self.__triviaGameControllersRepository.removeController(
            twitchChannel = user.getHandle(),
            userName = userName
        )

        if result is RemoveTriviaGameControllerResult.REMOVED:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Removed {userName} as a trivia game controller.')
        elif result is RemoveTriviaGameControllerResult.ERROR:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An error occurred when trying to remove {userName} as a trivia game controller!')
        else:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An unknown error occurred when trying to remove {userName} as a trivia game controller!')
            self.__timber.log('RemoveTriviaControllerCommand', f'Encountered unknown RemoveTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            raise ValueError(f'Encountered unknown RemoveTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

        self.__timber.log('RemoveTriviaControllerCommand', f'Handled !removetriviacontroller command with {result} result for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class RemoveUserCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: Timber,
        twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepositoryInterface, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepositoryInterface}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__timber: Timber = timber
        self.__twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface = twitchTokensRepositoryInterface
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProviderInterface.getAdministratorUserName()

        if ctx.getAuthorName().lower() != administrator.lower():
            self.__timber.log('RemoveUserCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('RemoveUserCommand', f'Not enough arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !adduser command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username argument is necessary for the !removeuser command. Example: !removeuser {user.getHandle()}')
            return

        userName: Optional[str] = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('RemoveUserCommand', f'Invalid username argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !removeuser command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username argument is necessary for the !removeuser command. Example: !removeuser {user.getHandle()}')
            return

        if not await self.__usersRepository.containsUserAsync(userName):
            self.__timber.log('RemoveUserCommand', f'Username argument (\"{userName}\") given by {ctx.getAuthorName()}:{ctx.getAuthorId()} does not already exist as a user')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to remove \"{userName}\" as this user does not already exist!')
            return

        await self.__twitchTokensRepositoryInterface.removeUser(userName)
        userId = await self.__userIdsRepository.fetchUserId(userName = userName)

        await self.__modifyUserDataHelper.setUserData(
            actionType = ModifyUserActionType.REMOVE,
            userId = userId,
            userName = userName
        )

        await self.__twitchUtils.safeSend(ctx, f'ⓘ To remove user \"{userName}\" ({userId}), please respond with `!confirm`')
        self.__timber.log('RemoveUserCommand', f'Handled !removeuser command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class SetTwitchCodeCommand(AbsCommand):

    def __init__(
        self,
        administratorProviderInterface: AdministratorProviderInterface,
        timber: Timber,
        twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(administratorProviderInterface, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProviderInterface}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepositoryInterface, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepositoryInterface}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProviderInterface: AdministratorProviderInterface = administratorProviderInterface
        self.__timber: Timber = timber
        self.__twitchTokensRepositoryInterface: TwitchTokensRepositoryInterface = twitchTokensRepositoryInterface
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProviderInterface.getAdministratorUserId()

        if ctx.getAuthorName().lower() != user.getHandle().lower() and ctx.getAuthorId() != administrator:
            self.__timber.log('SetTwitchCodeCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('SetTwitchCodeCommand', f'Not enough arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !settwitchcode command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Code argument is necessary for the !settwitchcode command. Example: !settwitchcode {self.__getRandomCodeStr()}')
            return

        code: Optional[str] = splits[1]
        if not utils.isValidStr(code):
            self.__timber.log('SetTwitchCodeCommand', f'Invalid code argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !settwitchcode command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Code argument is necessary for the !settwitchcode command. Example: !settwitchcode {self.__getRandomCodeStr()}')
            return

        await self.__twitchTokensRepositoryInterface.addUser(
            twitchHandle = user.getHandle(),
            code = code
        )

        self.__timber.log('SetTwitchCodeCommand', f'Handled !settwitchcode command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

    def __getRandomCodeStr(self) -> str:
        randomUuid = str(uuid.uuid4())
        randomUuid = randomUuid.replace('-', '')

        if len(randomUuid) > 16:
            randomUuid = randomUuid[0:16]

        return randomUuid


class StubCommand(AbsCommand):

    def __init__(self):
        pass

    async def handleCommand(self, ctx: TwitchContext):
        pass


class SuperAnswerCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameMachine: TriviaGameMachine,
        usersRepository: UsersRepository
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachine):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled() or not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() or not user.isSuperTriviaGameEnabled():
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            return

        answer = ' '.join(splits[1:])

        self.__triviaGameMachine.submitAction(CheckSuperAnswerTriviaAction(
            answer = answer,
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId(),
            userName = ctx.getAuthorName()
        ))

        self.__timber.log('SuperAnswerCommand', f'Handled !superanswer command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class SuperTriviaCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaGameMachine: TriviaGameMachine,
        triviaSettingsRepository: TriviaSettingsRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachine):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepository):
            raise ValueError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaGameMachine: TriviaGameMachine = triviaGameMachine
        self.__triviaSettingsRepository: TriviaSettingsRepository = triviaSettingsRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled() or not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() or not user.isSuperTriviaGameEnabled():
            return

        # For the time being, this command is intentionally not checking for mod status, as it has
        # been determined that super trivia game controllers shouldn't necessarily have to be mod.

        if not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId()
        ):
            return

        numberOfGames: int = 1
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2:
            numberOfGamesStr: Optional[str] = splits[1]

            try:
                numberOfGames = int(numberOfGamesStr)
            except (SyntaxError, TypeError, ValueError) as e:
                self.__timber.log('SuperTriviaCommand', f'Unable to convert the numberOfGamesStr ({numberOfGamesStr}) argument into an int (given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}): {e}', e, traceback.format_exc())
                await self.__twitchUtils.safeSend(ctx, f'⚠ Error converting the given count into an int. Example: !supertrivia 2')
                return

            maxNumberOfGames = await self.__triviaSettingsRepository.getMaxSuperGameQueueSize()

            if numberOfGames < 1 or numberOfGames > maxNumberOfGames:
                self.__timber.log('SuperTriviaCommand', f'The numberOfGames argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is out of bounds ({numberOfGames}) (converted from \"{numberOfGamesStr}\")')
                await self.__twitchUtils.safeSend(ctx, f'⚠ The given count is an unexpected number, please try again. Example: !supertrivia 2')
                return

        perUserAttempts = generalSettings.getSuperTriviaGamePerUserAttempts()
        if user.hasSuperTriviaPerUserAttempts():
            perUserAttempts = user.getSuperTriviaPerUserAttempts()

        points = generalSettings.getSuperTriviaGamePoints()
        if user.hasSuperTriviaGamePoints():
            points = user.getSuperTriviaGamePoints()

        regularTriviaPointsForWinning = generalSettings.getTriviaGamePoints()
        if user.hasTriviaGamePoints():
            regularTriviaPointsForWinning = user.getTriviaGamePoints()

        secondsToLive = generalSettings.getWaitForSuperTriviaAnswerDelay()
        if user.hasWaitForSuperTriviaAnswerDelay():
            secondsToLive = user.getWaitForSuperTriviaAnswerDelay()

        shinyMultiplier = generalSettings.getSuperTriviaGameShinyMultiplier()
        if user.hasSuperTriviaGameShinyMultiplier():
            shinyMultiplier = user.getSuperTriviaGameShinyMultiplier()

        toxicMultiplier = generalSettings.getSuperTriviaGameToxicMultiplier()
        if user.hasSuperTriviaGameToxicMultiplier():
            toxicMultiplier = user.getSuperTriviaGameToxicMultiplier()

        toxicTriviaPunishmentMultiplier = generalSettings.getSuperTriviaGameToxicPunishmentMultiplier()
        if user.hasSuperTriviaGameToxicPunishmentMultiplier():
            toxicTriviaPunishmentMultiplier = user.getSuperTriviaGameToxicPunishmentMultiplier()

        triviaFetchOptions = TriviaFetchOptions(
            twitchChannel = user.getHandle(),
            isJokeTriviaRepositoryEnabled = False,
            questionAnswerTriviaConditions = QuestionAnswerTriviaConditions.REQUIRED
        )

        self.__triviaGameMachine.submitAction(StartNewSuperTriviaGameAction(
            isQueueActionConsumed = False,
            isShinyTriviaEnabled = user.isShinyTriviaEnabled(),
            isToxicTriviaEnabled = user.isToxicTriviaEnabled(),
            numberOfGames = numberOfGames,
            perUserAttempts = perUserAttempts,
            pointsForWinning = points,
            regularTriviaPointsForWinning = regularTriviaPointsForWinning,
            secondsToLive = secondsToLive,
            shinyMultiplier = shinyMultiplier,
            toxicMultiplier = toxicMultiplier,
            toxicTriviaPunishmentMultiplier = toxicTriviaPunishmentMultiplier,
            twitchChannel = user.getHandle(),
            triviaFetchOptions = triviaFetchOptions
        ))

        self.__timber.log('SuperTriviaCommand', f'Handled !supertrivia command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class SwQuoteCommand(AbsCommand):

    def __init__(
        self,
        starWarsQuotesRepository: StarWarsQuotesRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if not isinstance(starWarsQuotesRepository, StarWarsQuotesRepository):
            raise ValueError(f'starWarsQuotesRepository argument is malformed: \"{starWarsQuotesRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__starWarsQuotesRepository: StarWarsQuotesRepository = starWarsQuotesRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isStarWarsQuotesEnabled():
            return
        elif not ctx.isAuthorMod() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        randomSpaceEmoji = utils.getRandomSpaceEmoji()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) < 2:
            swQuote = await self.__starWarsQuotesRepository.fetchRandomQuote()
            await self.__twitchUtils.safeSend(ctx, f'{swQuote} {randomSpaceEmoji}')
            return

        query = ' '.join(splits[1:])

        try:
            swQuote = await self.__starWarsQuotesRepository.searchQuote(query)

            if utils.isValidStr(swQuote):
                await self.__twitchUtils.safeSend(ctx, f'{swQuote} {randomSpaceEmoji}')
            else:
                await self.__twitchUtils.safeSend(ctx, f'⚠ No Star Wars quote found for the given query: \"{query}\"')
        except ValueError:
            self.__timber.log('SwQuoteCommand', f'Error retrieving Star Wars quote with query: \"{query}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error retrieving Star Wars quote with query: \"{query}\"')


class TimeCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.hasTimeZones():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        timeZones = user.getTimeZones()
        first = True
        text = ''

        for timeZone in timeZones:
            localTime = datetime.now(timeZone)

            if first:
                first = False
                formattedTime = utils.formatTime(localTime)
                text = f'🕰️ The local time for {user.getHandle()} is {formattedTime}.'
            else:
                formattedTime = utils.formatTimeShort(localTime)
                timeZoneName = timeZone.tzname(datetime.utcnow())
                text = f'{text} {timeZoneName} time is {formattedTime}.'

        await self.__twitchUtils.safeSend(ctx, text)
        self.__timber.log('TimeCommand', f'Handled !time command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class TranslateCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        languagesRepository: LanguagesRepository,
        timber: Timber,
        translationHelper: TranslationHelper,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 15)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(languagesRepository, LanguagesRepository):
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(translationHelper, TranslationHelper):
            raise ValueError(f'translationHelper argument is malformed: \"{translationHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__languagesRepository: LanguagesRepository = languagesRepository
        self.__timber: Timber = timber
        self.__translationHelper: TranslationHelper = translationHelper
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    def __determineOptionalLanguageEntry(self, splits: List[str]) -> Optional[LanguageEntry]:
        if not utils.hasItems(splits):
            raise ValueError(f'splits argument is malformed: \"{splits}\"')

        if len(splits[1]) >= 3 and splits[1][0:2] == '--':
            return self.__languagesRepository.getLanguageForCommand(
                command = splits[1][2:],
                hasIso6391Code = True
            )

        return None

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTranslateEnabled():
            return
        elif not user.isTranslateEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, f'⚠ Please specify the text you want to translate. Example: !translate I like tamales')
            return

        targetLanguageEntry = self.__determineOptionalLanguageEntry(splits)

        startSplitIndex: int = 1
        if targetLanguageEntry is not None:
            startSplitIndex = 2

        text = ' '.join(splits[startSplitIndex:])

        try:
            response = await self.__translationHelper.translate(text, targetLanguageEntry)
            await self.__twitchUtils.safeSend(ctx, response.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('TranslateCommand', f'Error translating text: \"{text}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, '⚠ Error translating')

        self.__timber.log('TranslateCommand', f'Handled !translate command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class TriviaInfoCommand(AbsCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaEmoteGenerator: TriviaEmoteGenerator,
        triviaHistoryRepository: TriviaHistoryRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepository):
            raise ValueError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGenerator):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepository):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepository = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaEmoteGenerator: TriviaEmoteGenerator = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepository = triviaHistoryRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('TriviaInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to get trivia question info as an invalid emote argument was given. Example: !triviainfo {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        emote: Optional[str] = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('TriviaInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to get trivia question info as an invalid emote argument was given. Example: !triviainfo {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.getHandle()
        )

        if reference is None:
            self.__timber.log('TriviaInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")')
            return

        additionalAnswers = await self.__additionalTriviaAnswersRepository.getAdditionalTriviaAnswers(
            triviaId = reference.getTriviaId(),
            triviaSource = reference.getTriviaSource(),
            triviaType = reference.getTriviaType()
        )

        additionalAnswersLen = 0
        if additionalAnswers is not None:
            additionalAnswersLen = additionalAnswers.getAdditionalAnswersLen()

        await self.__twitchUtils.safeSend(ctx, f'{normalizedEmote} {reference.getTriviaSource().toStr()}:{reference.getTriviaId()} triviaType:{reference.getTriviaType().toStr()} additionalAnswers:{additionalAnswersLen} isLocal:{str(reference.getTriviaSource().isLocal()).lower()}')
        self.__timber.log('TriviaInfoCommand', f'Handled !triviainfo command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class TriviaScoreCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepository,
        timber: Timber,
        toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepository,
        triviaScoreRepository: TriviaScoreRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepository,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(shinyTriviaOccurencesRepository, ShinyTriviaOccurencesRepository):
            raise ValueError(f'shinyTriviaOccurencesRepository argument is malformed: \"{shinyTriviaOccurencesRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepository):
            raise ValueError(f'toxicTriviaOccurencesRepository argument is malformed: \"{toxicTriviaOccurencesRepository}\"')
        elif not isinstance(triviaScoreRepository, TriviaScoreRepository):
            raise ValueError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepository):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepository = shinyTriviaOccurencesRepository
        self.__timber: Timber = timber
        self.__toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepository = toxicTriviaOccurencesRepository
        self.__triviaScoreRepository: TriviaScoreRepository = triviaScoreRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepository = userIdsRepository
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())

        userName: str = None
        if len(splits) >= 2:
            userName = utils.removePreceedingAt(splits[1])
        else:
            userName = ctx.getAuthorName()

        userId: str = None

        # this means that a user is querying for another user's trivia score
        if userName.lower() != ctx.getAuthorName().lower():
            try:
                userId = await self.__userIdsRepository.fetchUserId(userName = userName)
            except (RuntimeError, ValueError) as e:
                self.__timber.log('TriviaScoreCommand', f'Unable to find user ID for \"{userName}\" in the database: {e}', e, traceback.format_exc())
                await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database')
                return
        else:
            userId = ctx.getAuthorId()

        shinyResult = await self.__shinyTriviaOccurencesRepository.fetchDetails(
            twitchChannel = user.getHandle(),
            userId = userId
        )

        toxicResult = await self.__toxicTriviaOccurencesRepository.fetchDetails(
            twitchChannel = user.getHandle(),
            userId = userId
        )

        triviaResult = await self.__triviaScoreRepository.fetchTriviaScore(
            twitchChannel = user.getHandle(),
            userId = userId
        )

        await self.__twitchUtils.safeSend(ctx, await self.__triviaUtils.getTriviaScoreMessage(
            shinyResult = shinyResult,
            userName = userName,
            toxicResult = toxicResult,
            triviaResult = triviaResult
        ))

        self.__timber.log('TriviaScoreCommand', f'Handled !triviascore command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class TwitterCommand(AbsCommand):

    def __init__(
        self,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        cooldown: timedelta = timedelta(minutes = 5)
    ):
        if not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.hasTwitter():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await self.__twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s twitter: {user.getTwitterUrl()}')
        self.__timber.log('TwitterCommand', f'Handled !twitter command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class UnbanTriviaQuestionCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        triviaBanHelper: TriviaBanHelper,
        triviaEmoteGenerator: TriviaEmoteGenerator,
        triviaHistoryRepository: TriviaHistoryRepository,
        triviaUtils: TriviaUtils,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaBanHelper, TriviaBanHelper):
            raise ValueError(f'triviaBanHelper argument is malformed: \"{triviaBanHelper}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGenerator):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepository):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtils):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__triviaBanHelper: TriviaBanHelper = triviaBanHelper
        self.__triviaEmoteGenerator: TriviaEmoteGenerator = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepository = triviaHistoryRepository
        self.__triviaUtils: TriviaUtils = triviaUtils
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('UnbanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to unban trivia question as no emote argument was given. Example: !unbantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        emote: Optional[str] = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('UnbanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to unban trivia question as an invalid emote argument was given. Example: !unbantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.getHandle()
        )

        if reference is None:
            self.__timber.log('UnbanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")')
            return

        await self.__triviaBanHelper.unban(
            triviaId = reference.getTriviaId(),
            triviaSource = reference.getTriviaSource()
        )

        await self.__twitchUtils.safeSend(ctx, f'ⓘ Unbanned trivia question {normalizedEmote} — {reference.getTriviaSource().toStr()}:{reference.getTriviaId()}')
        self.__timber.log('UnbanTriviaQuestionCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} ({normalizedEmote}) ({reference.getTriviaSource().toStr()}:{reference.getTriviaId()} was unbanned)')


class WeatherCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        locationsRepository: LocationsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        weatherRepository: WeatherRepository,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(locationsRepository, LocationsRepository):
            raise ValueError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(weatherRepository, WeatherRepository):
            raise ValueError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__locationsRepository: LocationsRepository = locationsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__weatherRepository: WeatherRepository = weatherRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isWeatherEnabled():
            return
        elif not user.isWeatherEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        if not user.hasLocationId():
            await self.__twitchUtils.safeSend(ctx, f'⚠ Weather for {user.getHandle()} is enabled, but no location ID is available')
            return

        location = await self.__locationsRepository.getLocation(user.getLocationId())

        try:
            weatherReport = await self.__weatherRepository.fetchWeather(location)
            await self.__twitchUtils.safeSend(ctx, weatherReport.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WeatherCommand', f'Error fetching weather for \"{user.getLocationId()}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, '⚠ Error fetching weather')

        self.__timber.log('WeatherCommand', f'Handled !weather command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class WordCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        languagesRepository: LanguagesRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        usersRepository: UsersRepository,
        wordOfTheDayRepository: WordOfTheDayRepository,
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(languagesRepository, LanguagesRepository):
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(wordOfTheDayRepository, WordOfTheDayRepository):
            raise ValueError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__languagesRepository: LanguagesRepository = languagesRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__usersRepository: UsersRepository = usersRepository
        self.__wordOfTheDayRepository: WordOfTheDayRepository = wordOfTheDayRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isWordOfTheDayEnabled():
            return
        elif not user.isWordOfTheDayEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            exampleEntry = self.__languagesRepository.getExampleLanguageEntry(hasWotdApiCode = True)
            allWotdApiCodes = self.__languagesRepository.getAllWotdApiCodes()
            await self.__twitchUtils.safeSend(ctx, f'⚠ A language code is necessary for the !word command. Example: !word {exampleEntry.getWotdApiCode()}. Available languages: {allWotdApiCodes}')
            return

        language: str = splits[1]
        languageEntry: LanguageEntry = None

        try:
            languageEntry = self.__languagesRepository.requireLanguageForCommand(
                command = language,
                hasWotdApiCode = True
            )
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error retrieving language entry: \"{language}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ The given language code is not supported by the !word command. Available languages: {self.__languagesRepository.getAllWotdApiCodes()}')
            return

        try:
            wotd = await self.__wordOfTheDayRepository.fetchWotd(languageEntry)
            await self.__twitchUtils.safeSend(ctx, wotd.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error fetching Word Of The Day for \"{languageEntry.getWotdApiCode()}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error fetching Word Of The Day for \"{languageEntry.getWotdApiCode()}\"')

        self.__timber.log('WordCommand', f'Handled !word command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
