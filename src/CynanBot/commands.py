import random
import traceback
import uuid
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.authRepository import AuthRepository
from CynanBot.cheerActions.cheerAction import CheerAction
from CynanBot.cheerActions.cheerActionIdGeneratorInterface import \
    CheerActionIdGeneratorInterface
from CynanBot.cheerActions.cheerActionsRepositoryInterface import \
    CheerActionsRepositoryInterface
from CynanBot.contentScanner.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBot.cuteness.cutenessLeaderboardResult import \
    CutenessLeaderboardResult
from CynanBot.cuteness.cutenessRepositoryInterface import \
    CutenessRepositoryInterface
from CynanBot.cuteness.cutenessResult import CutenessResult
from CynanBot.cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from CynanBot.funtoon.funtoonTokensRepositoryInterface import \
    FuntoonTokensRepositoryInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.language.jishoHelperInterface import JishoHelperInterface
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.language.translationHelper import TranslationHelper
from CynanBot.language.wordOfTheDayRepositoryInterface import \
    WordOfTheDayRepositoryInterface
from CynanBot.location.locationsRepositoryInterface import \
    LocationsRepositoryInterface
from CynanBot.misc.clearable import Clearable
from CynanBot.misc.timedDict import TimedDict
from CynanBot.mostRecentChat.mostRecentChatsRepositoryInterface import \
    MostRecentChatsRepositoryInterface
from CynanBot.pkmn.pokepediaRepository import PokepediaRepository
from CynanBot.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from CynanBot.recurringActions.weatherRecurringAction import \
    WeatherRecurringAction
from CynanBot.recurringActions.wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction
from CynanBot.soundPlayerManager.soundAlert import SoundAlert
from CynanBot.soundPlayerManager.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.starWars.starWarsQuotesRepositoryInterface import \
    StarWarsQuotesRepositoryInterface
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.actions.checkAnswerTriviaAction import \
    CheckAnswerTriviaAction
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBot.trivia.banned.bannedTriviaGameControllersRepositoryInterface import \
    BannedTriviaGameControllersRepositoryInterface
from CynanBot.trivia.banned.triviaBanHelperInterface import \
    TriviaBanHelperInterface
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.gameController.addTriviaGameControllerResult import \
    AddTriviaGameControllerResult
from CynanBot.trivia.gameController.removeBannedTriviaGameControllerResult import \
    RemoveBannedTriviaGameControllerResult
from CynanBot.trivia.gameController.removeTriviaGameControllerResult import \
    RemoveTriviaGameControllerResult
from CynanBot.trivia.gameController.triviaGameControllersRepositoryInterface import \
    TriviaGameControllersRepositoryInterface
from CynanBot.trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from CynanBot.trivia.triviaEmoteGeneratorInterface import \
    TriviaEmoteGeneratorInterface
from CynanBot.trivia.triviaExceptions import (
    AdditionalTriviaAnswerAlreadyExistsException,
    AdditionalTriviaAnswerIsMalformedException,
    AdditionalTriviaAnswerIsUnsupportedTriviaTypeException,
    TooManyAdditionalTriviaAnswersException)
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.trivia.triviaHistoryRepositoryInterface import \
    TriviaHistoryRepositoryInterface
from CynanBot.trivia.triviaIdGeneratorInterface import \
    TriviaIdGeneratorInterface
from CynanBot.trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from CynanBot.trivia.triviaSettingsRepositoryInterface import \
    TriviaSettingsRepositoryInterface
from CynanBot.trivia.triviaUtilsInterface import TriviaUtilsInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchUserDetails import TwitchUserDetails
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBot.twitch.twitchFollowerRepositoryInterface import \
    TwitchFollowerRepositoryInterface
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.modifyUserActionType import ModifyUserActionType
from CynanBot.users.modifyUserDataHelper import ModifyUserDataHelper
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface
from CynanBot.weather.exceptions import OneWeatherApiKeyUnavailableException
from CynanBot.weather.weatherRepositoryInterface import \
    WeatherRepositoryInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class AbsCommand(ABC):

    @abstractmethod
    async def handleCommand(self, ctx: TwitchContext):
        pass


class AddTriviaAnswerCommand(AbsCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        answerDelimiter: str = ', '
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise ValueError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(answerDelimiter, str):
            raise ValueError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
            twitchChannelId = await ctx.getTwitchChannelId(),
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
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
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
                userId = ctx.getAuthorId(),
                triviaSource = reference.getTriviaSource(),
                triviaType = reference.getTriviaType()
            )

            additionalAnswers = self.__answerDelimiter.join(result.getAdditionalAnswersStrs())
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
        administratorProvider: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise ValueError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameControllersRepository: TriviaGameControllersRepositoryInterface = triviaGameControllersRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return

        twitchChannelId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if twitchChannelId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
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
            twitchChannelId = twitchChannelId,
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
        administratorProvider: AdministratorProviderInterface,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

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

        userId = await self.__userIdsRepository.fetchUserId(
            userName = userName,
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(ctx.getTwitchChannelName())
        )

        if not utils.isValidStr(userId):
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to fetch user ID for \"{userName}\"!')
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
        timber: TimberInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise ValueError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameMachine: TriviaGameMachineInterface = triviaGameMachine
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__usersRepository: UsersRepositoryInterface = usersRepository

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
            actionId = await self.__triviaIdGenerator.generateActionId(),
            answer = answer,
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId(),
            userName = ctx.getAuthorName()
        ))

        self.__timber.log('AnswerCommand', f'Handled !answer command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class BanTriviaQuestionCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaBanHelper: TriviaBanHelperInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaBanHelper, TriviaBanHelperInterface):
            raise ValueError(f'triviaBanHelper argument is malformed: \"{triviaBanHelper}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaBanHelper: TriviaBanHelperInterface = triviaBanHelper
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('BanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to ban trivia question as no emote argument was given. Example: !bantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        emote = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('BanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to ban trivia question as an invalid emote argument was given. Example: !bantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if reference is None:
            self.__timber.log('BanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")')
            return

        await self.__triviaBanHelper.ban(
            triviaId = reference.getTriviaId(),
            userId = ctx.getAuthorId(),
            originalTriviaSource = reference.getOriginalTriviaSource(),
            triviaSource = reference.getTriviaSource()
        )

        await self.__twitchUtils.safeSend(ctx, f'{normalizedEmote} Banned trivia question {reference.getTriviaSource().toStr()} — {reference.getTriviaId()}')
        self.__timber.log('BanTriviaQuestionCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} ({normalizedEmote}) ({reference.getTriviaSource().toStr()}:{reference.getTriviaId()} was banned)')


class ClearCachesCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        authRepository: AuthRepository,
        bannedWordsRepository: Optional[BannedWordsRepositoryInterface],
        cheerActionsRepository: Optional[CheerActionsRepositoryInterface],
        funtoonTokensRepository: Optional[FuntoonTokensRepositoryInterface],
        generalSettingsRepository: GeneralSettingsRepository,
        isLiveOnTwitchRepository: Optional[IsLiveOnTwitchRepositoryInterface],
        locationsRepository: Optional[LocationsRepositoryInterface],
        modifyUserDataHelper: ModifyUserDataHelper,
        mostRecentChatsRepository: Optional[MostRecentChatsRepositoryInterface],
        openTriviaDatabaseTriviaQuestionRepository: Optional[OpenTriviaDatabaseTriviaQuestionRepository],
        soundPlayerSettingsRepository: Optional[SoundPlayerSettingsRepositoryInterface],
        timber: TimberInterface,
        triviaSettingsRepository: Optional[TriviaSettingsRepositoryInterface],
        ttsSettingsRepository: Optional[TtsSettingsRepositoryInterface],
        twitchFollowerRepository: Optional[TwitchFollowerRepositoryInterface],
        twitchTokensRepository: Optional[TwitchTokensRepositoryInterface],
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        weatherRepository: Optional[WeatherRepositoryInterface],
        websocketConnectionServer: Optional[WebsocketConnectionServerInterface],
        wordOfTheDayRepository: Optional[WordOfTheDayRepositoryInterface]
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif bannedWordsRepository is not None and not isinstance(bannedWordsRepository, BannedWordsRepositoryInterface):
            raise ValueError(f'bannedWordsRepository argument is malformed: \"{bannedWordsRepository}\"')
        elif cheerActionsRepository is not None and not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise ValueError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif funtoonTokensRepository is not None and not isinstance(funtoonTokensRepository, FuntoonTokensRepositoryInterface):
            raise ValueError(f'funtoonTokensRepository argument is malformed: \"{funtoonTokensRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif isLiveOnTwitchRepository is not None and not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise ValueError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif locationsRepository is not None and not isinstance(locationsRepository, LocationsRepositoryInterface):
            raise ValueError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif mostRecentChatsRepository is not None and not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise ValueError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif openTriviaDatabaseTriviaQuestionRepository is not None and not isinstance(openTriviaDatabaseTriviaQuestionRepository, OpenTriviaDatabaseTriviaQuestionRepository):
            raise ValueError(f'openTriviaDatabaseTriviaQuestionRepository argument is malformed: \"{openTriviaDatabaseTriviaQuestionRepository}\"')
        elif soundPlayerSettingsRepository is not None and not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise ValueError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif triviaSettingsRepository is not None and not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise ValueError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif ttsSettingsRepository is not None and not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise ValueError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif twitchFollowerRepository is not None and not isinstance(twitchFollowerRepository, TwitchFollowerRepositoryInterface):
            raise TypeError(f'twitchFollowerRepository argument is malformed: \"{twitchFollowerRepository}\"')
        elif twitchTokensRepository is not None and not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif weatherRepository is not None and not isinstance(weatherRepository, WeatherRepositoryInterface):
            raise ValueError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise ValueError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')
        elif wordOfTheDayRepository is not None and not isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface):
            raise ValueError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

        self.__clearables: List[Optional[Clearable]] = list()
        self.__clearables.append(administratorProvider)
        self.__clearables.append(authRepository)
        self.__clearables.append(bannedWordsRepository)
        self.__clearables.append(cheerActionsRepository)
        self.__clearables.append(funtoonTokensRepository)
        self.__clearables.append(generalSettingsRepository)
        self.__clearables.append(isLiveOnTwitchRepository)
        self.__clearables.append(locationsRepository)
        self.__clearables.append(modifyUserDataHelper)
        self.__clearables.append(mostRecentChatsRepository)
        self.__clearables.append(openTriviaDatabaseTriviaQuestionRepository)
        self.__clearables.append(soundPlayerSettingsRepository)
        self.__clearables.append(triviaSettingsRepository)
        self.__clearables.append(ttsSettingsRepository)
        self.__clearables.append(twitchFollowerRepository)
        self.__clearables.append(twitchTokensRepository)
        self.__clearables.append(userIdsRepository)
        self.__clearables.append(usersRepository)
        self.__clearables.append(weatherRepository)
        self.__clearables.append(websocketConnectionServer)
        self.__clearables.append(wordOfTheDayRepository)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if administrator != ctx.getAuthorId():
            self.__timber.log('ClearCachesCommand', f'Attempted use of !clearcaches command by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            return

        for clearable in self.__clearables:
            if clearable is not None:
                await clearable.clearCaches()

        await self.__twitchUtils.safeSend(ctx, 'ⓘ All caches cleared')
        self.__timber.log('ClearCachesCommand', f'Handled !clearcaches command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class ConfirmCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

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
        cutenessRepository: CutenessRepositoryInterface,
        cutenessUtils: CutenessUtilsInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 2)
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__cutenessUtils: CutenessUtilsInterface = cutenessUtils
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    def __cutenessLeaderboardResultToStr(self, result: CutenessLeaderboardResult) -> str:
        if not isinstance(result, CutenessLeaderboardResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')

        entries = result.getEntries()

        if not utils.hasItems(entries):
            return f'{result.getCutenessDate().getHumanString()} Leaderboard is empty 😿'

        specificLookupText: Optional[str] = None
        specificLookupCutenessResult = result.getSpecificLookupCutenessResult()

        if specificLookupCutenessResult is not None:
            userName = specificLookupCutenessResult.getUserName()
            cutenessStr = specificLookupCutenessResult.getCutenessStr()
            specificLookupText = f'@{userName} your cuteness is {cutenessStr}'

        leaderboard = self.__cutenessUtils.getLeaderboard(
            entries = entries,
            delimiter = self.__delimiter
        )

        if utils.isValidStr(specificLookupText):
            return f'{specificLookupText}, and the {result.getCutenessDate().getHumanString()} Leaderboard is: {leaderboard} ✨'
        else:
            return f'{result.getCutenessDate().getHumanString()} Leaderboard {leaderboard} ✨'

    def __cutenessResultToStr(self, result: CutenessResult) -> str:
        if not isinstance(result, CutenessResult):
            raise ValueError(f'result argument is malformed: \"{result}\"')

        cuteness = result.getCuteness()

        if utils.isValidInt(cuteness) and cuteness >= 1:
            return f'{result.getUserName()}\'s {result.getCutenessDate().getHumanString()} cuteness is {result.getCutenessStr()} ✨'
        else:
            return f'{result.getUserName()} has no cuteness in {result.getCutenessDate().getHumanString()}'

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        # this means that a user is querying for another user's cuteness
        if userName.lower() != ctx.getAuthorName().lower():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return

            result = await self.__cutenessRepository.fetchCuteness(
                twitchChannel = user.getHandle(),
                twitchChannelId = await ctx.getTwitchChannelId(),
                userId = userId,
                userName = userName
            )

            await self.__twitchUtils.safeSend(ctx, self.__cutenessResultToStr(result))
        else:
            userId = ctx.getAuthorId()

            result = await self.__cutenessRepository.fetchCutenessLeaderboard(
                twitchChannel = user.getHandle(),
                twitchChannelId = await ctx.getTwitchChannelId(),
                specificLookupUserId = userId,
                specificLookupUserName = userName
            )

            await self.__twitchUtils.safeSend(ctx, self.__cutenessLeaderboardResultToStr(result))

        self.__timber.log('CutenessCommand', f'Handled !cuteness command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class CutenessChampionsCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        cutenessUtils: CutenessUtilsInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 15)
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__cutenessUtils: CutenessUtilsInterface = cutenessUtils
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        result = await self.__cutenessRepository.fetchCutenessChampions(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        await self.__twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessChampions(result, self.__delimiter))
        self.__timber.log('CutenessChampionsCommand', f'Handled !cutenesschampions command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class CutenessHistoryCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        cutenessUtils: CutenessUtilsInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        entryDelimiter: str = ', ',
        leaderboardDelimiter: str = ' — ',
        cooldown: timedelta = timedelta(seconds = 2)
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(entryDelimiter, str):
            raise ValueError(f'entryDelimiter argument is malformed: \"{entryDelimiter}\"')
        elif not isinstance(leaderboardDelimiter, str):
            raise ValueError(f'leaderboardDelimiter argument is malformed: \"{leaderboardDelimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__cutenessUtils: CutenessUtilsInterface = cutenessUtils
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__entryDelimiter: str = entryDelimiter
        self.__leaderboardDelimiter: str = leaderboardDelimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        # this means that a user is querying for another user's cuteness history
        if userName.lower() != ctx.getAuthorName().lower():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                self.__timber.log('CutenessHistoryCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return

            result = await self.__cutenessRepository.fetchCutenessHistory(
                twitchChannel = user.getHandle(),
                twitchChannelId = await ctx.getTwitchChannelId(),
                userId = userId,
                userName = userName
            )

            await self.__twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessHistory(result, self.__entryDelimiter))
        else:
            result = await self.__cutenessRepository.fetchCutenessLeaderboardHistory(
                twitchChannel = user.getHandle(),
                twitchChannelId = await ctx.getTwitchChannelId()
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
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCynanSourceEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(ctx.getTwitchChannelName()):
            return

        await self.__twitchUtils.safeSend(ctx, 'My source code is available here: https://github.com/charlesmadere/cynanbot')
        self.__timber.log('CynanSourceCommand', f'Handled !cynansource command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class DeleteCheerActionCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionIdGenerator: CheerActionIdGeneratorInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionIdGenerator, CheerActionIdGeneratorInterface):
            raise ValueError(f'cheerActionIdGenerator argument is malformed: \"{cheerActionIdGenerator}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise ValueError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__cheerActionIdGenerator: CheerActionIdGeneratorInterface = cheerActionIdGenerator
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __actionToStr(self, action: CheerAction) -> str:
        if not isinstance(action, CheerAction):
            raise ValueError(f'action argument is malformed: \"{action}\"')

        return f'id={action.getActionId()}, amount={action.getAmount()}, duration={action.getDurationSeconds()}'

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await self.__userIdsRepository.requireUserId(user.getHandle())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('DeleteCheerActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return
        elif not user.areCheerActionsEnabled():
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2 or not utils.strContainsAlphanumericCharacters(splits[1]):
            self.__timber.log('DeleteCheerActionCommand', f'Incorrect arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            actionId = await self.__cheerActionIdGenerator.generateActionId()
            await self.__twitchUtils.safeSend(ctx, f'⚠ Action ID is necessary for the !deletecheeraction command. Example: !deletecheeraction {actionId}')
            return

        actionId = splits[1]

        action = await self.__cheerActionsRepository.deleteAction(
            actionId = splits[1],
            userId = userId
        )

        if action is None:
            self.__timber.log('DeleteCheerActionCommand', f'Cheer action ID {actionId} was attempted to be deleted by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no corresponding cheer action was found')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Could not find any corresponding cheer action with ID \"{actionId}\"')
            return

        actionString = await self.__actionToStr(action)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Deleted cheer action — {actionString}')
        self.__timber.log('DeleteCheerActionCommand', f'Handled !deletecheeraction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class DeleteTriviaAnswersCommand(AbsCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        answerDelimiter: str = ', '
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise ValueError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(answerDelimiter, str):
            raise ValueError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
            twitchChannelId = await ctx.getTwitchChannelId(),
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
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
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
            additionalAnswers = self.__answerDelimiter.join(result.getAdditionalAnswersStrs())
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} Deleted additional trivia answers for {result.getTriviaSource().toStr()}:{result.getTriviaId()} — {additionalAnswers}')

        self.__timber.log('DeleteTriviaAnswersCommand', f'Handled !deletetriviaanswers command with {result} for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class DiscordCommand(AbsCommand):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.hasDiscord():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await self.__twitchUtils.safeSend(ctx, f'{user.getHandle()}\'s discord: {user.getDiscordUrl()}')
        self.__timber.log('DiscordCommand', f'Handled !discord command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class GetBannedTriviaControllersCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise ValueError(f'bannedTriviaGameControllersRepository argument is malformed: \"{bannedTriviaGameControllersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface = bannedTriviaGameControllersRepository
        self.__timber: TimberInterface = timber
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        userName = ctx.getAuthorName().lower()

        if user.getHandle().lower() != userName and ctx.getAuthorId() != administrator:
            self.__timber.log('GetBannedTriviaControllersCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        controllers = await self.__bannedTriviaGameControllersRepository.getBannedControllers()
        await self.__twitchUtils.safeSend(ctx, await self.__triviaUtils.getTriviaGameBannedControllers(controllers))
        self.__timber.log('GetBannedTriviaControllersCommand', f'Handled !getbannedtriviacontrollers command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class GetCheerActionsCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = '; '
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise ValueError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter

    async def __actionsToStr(self, actions: List[CheerAction]) -> str:
        if not isinstance(actions, List):
            raise ValueError(f'actions argument is malformed: \"{actions}\"')

        if len(actions) == 0:
            return f'ⓘ You have no cheer actions'

        cheerActionStrings: List[str] = list()

        for action in actions:
            cheerActionStrings.append(f'id={action.getActionId()}, amount={action.getAmount()}, duration={action.getDurationSeconds()}')

        cheerActionsString = self.__delimiter.join(cheerActionStrings)
        return f'ⓘ Your cheer actions — {cheerActionsString}'

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await self.__userIdsRepository.requireUserId(user.getHandle())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('GetCheerActionsCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return
        elif not user.areCheerActionsEnabled():
            return

        actions = await self.__cheerActionsRepository.getActions(userId)
        await self.__twitchUtils.safeSend(ctx, await self.__actionsToStr(actions))
        self.__timber.log('GetCheerActionsCommand', f'Handled !getcheeractions command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class GetGlobalTriviaControllersCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface):
            raise ValueError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface = triviaGameGlobalControllersRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

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
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        answerDelimiter: str = ', '
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise ValueError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(answerDelimiter, str):
            raise ValueError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
            twitchChannelId = await ctx.getTwitchChannelId(),
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
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
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
            additionalAnswers = self.__answerDelimiter.join(result.getAdditionalAnswersStrs())
            await self.__twitchUtils.safeSend(ctx, f'{reference.getEmote()} Additional trivia answers for {result.getTriviaSource().toStr()}:{result.getTriviaId()} — {additionalAnswers}')

        self.__timber.log('GetTriviaAnswersCommand', f'Handled !gettriviaanswers command with {result} for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class GetTriviaControllersCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise ValueError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameControllersRepository: TriviaGameControllersRepositoryInterface = triviaGameControllersRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return

        twitchChannelId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if twitchChannelId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('GetTriviaControllersCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        controllers = await self.__triviaGameControllersRepository.getControllers(
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId
        )

        await self.__twitchUtils.safeSend(ctx, await self.__triviaUtils.getTriviaGameControllers(controllers))
        self.__timber.log('GetTriviaControllersCommand', f'Handled !gettriviacontrollers command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class JishoCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        jishoHelper: JishoHelperInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(jishoHelper, JishoHelperInterface):
            raise ValueError(f'jishoHelper argument is malformed: \"{jishoHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__jishoHelper: JishoHelperInterface = jishoHelper
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

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
        cutenessRepository: CutenessRepositoryInterface,
        cutenessUtils: CutenessUtilsInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise ValueError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise ValueError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__cutenessUtils: CutenessUtilsInterface = cutenessUtils
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isCutenessEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        userId = ctx.getAuthorId()

        # this means that a user is querying for another user's cuteness history
        if userName.lower() != ctx.getAuthorName().lower():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                self.__timber.log('MyCutenessHistoryCommand', f'Unable to find user ID for \"{userName}\" in the database')
                await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to find user info for \"{userName}\" in the database!')
                return

        result = await self.__cutenessRepository.fetchCutenessHistory(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = userId,
            userName = userName
        )

        await self.__twitchUtils.safeSend(ctx, self.__cutenessUtils.getCutenessHistory(result, self.__delimiter))
        self.__timber.log('MyCutenessHistoryCommand', f'Handled !mycutenesshistory command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class PbsCommand(AbsCommand):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 10)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(pokepediaRepository, PokepediaRepository):
            raise ValueError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__pokepediaRepository: PokepediaRepository = pokepediaRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 10)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(pokepediaRepository, PokepediaRepository):
            raise ValueError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__pokepediaRepository: PokepediaRepository = pokepediaRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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


class RecurringActionCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        languagesRepository: LanguagesRepositoryInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __enableSuperTriviaRecurringAction(
        self,
        ctx: TwitchContext,
        user: UserInterface,
        splits: List[str]
    ):
        if not isinstance(ctx, TwitchContext):
            raise TypeError(f'ctx argument is malformed: \"{ctx}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not utils.hasItems(splits):
            raise TypeError(f'splits argument is malformed: \"{splits}\"')

        minutesBetween = await self.__parseMinutesBetween(
            actionType = RecurringActionType.SUPER_TRIVIA,
            splits = splits
        )

        recurringAction = SuperTriviaRecurringAction(
            enabled = True,
            twitchChannel = user.getHandle(),
            minutesBetween = minutesBetween
        )

        await self.__recurringActionsRepository.setRecurringAction(recurringAction)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Enabled recurring Super Trivia action every {minutesBetween} minutes')

    async def __enableWeatherRecurringAction(
        self,
        ctx: TwitchContext,
        user: UserInterface,
        splits: List[str]
    ):
        if not isinstance(ctx, TwitchContext):
            raise TypeError(f'ctx argument is malformed: \"{ctx}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not utils.hasItems(splits):
            raise TypeError(f'splits argument is malformed: \"{splits}\"')

        minutesBetween = await self.__parseMinutesBetween(
            actionType = RecurringActionType.WEATHER,
            splits = splits
        )

        recurringAction = WeatherRecurringAction(
            enabled = True,
            twitchChannel = user.getHandle(),
            minutesBetween = minutesBetween
        )

        await self.__recurringActionsRepository.setRecurringAction(recurringAction)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Enabled recurring Weather action every {minutesBetween} minutes')

    async def __enableWordOfTheDayRecurringAction(
        self,
        ctx: TwitchContext,
        user: UserInterface,
        splits: List[str]
    ):
        if not isinstance(ctx, TwitchContext):
            raise TypeError(f'ctx argument is malformed: \"{ctx}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not utils.hasItems(splits):
            raise TypeError(f'splits argument is malformed: \"{splits}\"')

        minutesBetween = await self.__parseMinutesBetween(
            actionType = RecurringActionType.WORD_OF_THE_DAY,
            splits = splits
        )

        languageEntry: Optional[LanguageEntry] = None

        if len(splits) >= 4:
            try:
                languageEntry = await self.__languagesRepository.getLanguageForWotdApiCode(splits[3])
            except:
                pass

        if languageEntry is None:
            allWotdApiCodes = await self.__languagesRepository.getAllWotdApiCodes()
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to configure recurring Word Of The Day action as an invalid language was specified (available languages: {allWotdApiCodes})')
            return

        recurringAction = WordOfTheDayRecurringAction(
            enabled = True,
            twitchChannel = user.getHandle(),
            minutesBetween = minutesBetween,
            languageEntry = languageEntry
        )

        await self.__recurringActionsRepository.setRecurringAction(recurringAction)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Enabled recurring Word Of The Day action every {minutesBetween} minutes for {languageEntry.getName()}')

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if user.getHandle().lower() != ctx.getAuthorName().lower() and administrator != ctx.getAuthorId():
            self.__timber.log('RecurringActionCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('RecurringActionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to configure recurring action as no arguments were given. Example: !recurringaction {self.__randomRecurringActionType().toStr()}')
            return

        actionTypeStr: Optional[str] = splits[1]
        actionType: Optional[RecurringActionType] = None

        try:
            actionType = RecurringActionType.fromStr(actionTypeStr)
        except:
            pass

        if actionType is None:
            self.__timber.log('RecurringActionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid RecurringActionType argument was given: \"{actionTypeStr}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to configure recurring action as an invalid recurring action type was given. Example: !recurringaction {self.__randomRecurringActionType().toStr()}')
            return

        if actionType is RecurringActionType.SUPER_TRIVIA:
            await self.__enableSuperTriviaRecurringAction(
                ctx = ctx,
                user = user,
                splits = splits
            )
        elif actionType is RecurringActionType.WEATHER:
            await self.__enableWeatherRecurringAction(
                ctx = ctx,
                user = user,
                splits = splits
            )
        elif actionType is RecurringActionType.WORD_OF_THE_DAY:
            await self.__enableWordOfTheDayRecurringAction(
                ctx = ctx,
                user = user,
                splits = splits
            )
        else:
            raise RuntimeError(f'actionType is unknown: \"{actionType}\"')

        self.__timber.log('RecurringActionCommand', f'Handled !recurringaction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

    async def __parseMinutesBetween(self, actionType: RecurringActionType, splits: List[str]) -> int:
        if not isinstance(actionType, RecurringActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')
        elif not utils.hasItems(splits):
            raise TypeError(f'splits argument is malformed: \"{splits}\"')

        if len(splits) < 3:
            return actionType.getDefaultRecurringActionTimingMinutes()

        minutesBetweenStr: Optional[str] = splits[2]
        minutesBetween: Optional[int] = None

        try:
            minutesBetween = int(minutesBetweenStr)
        except:
            pass

        if not utils.isValidInt(minutesBetween) or minutesBetween < actionType.getMinimumRecurringActionTimingMinutes() or minutesBetween > utils.getIntMaxSafeSize():
            minutesBetween = actionType.getDefaultRecurringActionTimingMinutes()

        return minutesBetween

    def __randomRecurringActionType(self) -> RecurringActionType:
        recurringActions: List[RecurringActionType] = list(RecurringActionType)
        return random.choice(recurringActions)


class RemoveBannedTriviaControllerCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise ValueError(f'bannedTriviaGameControllersRepository argument is malformed: \"{bannedTriviaGameControllersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface = bannedTriviaGameControllersRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if user.getHandle().lower() != ctx.getAuthorName().lower() and administrator != ctx.getAuthorId():
            self.__timber.log('RemoveBannedTriviaControllerCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('RemoveBannedTriviaControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to remove banned trivia controller as no username argument was given. Example: !removebannedtriviacontroller {user.getHandle()}')
            return

        userName: Optional[str] = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('RemoveBannedTriviaControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to remove banned trivia controller as username argument is malformed. Example: !removebannedtriviacontroller {user.getHandle()}')
            return

        result = await self.__bannedTriviaGameControllersRepository.removeBannedController(
            userName = userName
        )

        if result is RemoveBannedTriviaGameControllerResult.REMOVED:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Removed {userName} as a banned trivia game controller.')
        elif result is RemoveBannedTriviaGameControllerResult.ERROR:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An error occurred when trying to remove {userName} as a banned trivia game controller!')
        else:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An unknown error occurred when trying to remove {userName} as a banned trivia game controller!')
            self.__timber.log('RemoveBannedTriviaControllerCommand', f'Encountered unknown RemoveBannedTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            raise ValueError(f'Encountered unknown RemoveBannedTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

        self.__timber.log('RemoveBannedTriviaControllerCommand', f'Handled !removebannedtriviacontroller command with {result} result for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class RemoveGlobalTriviaControllerCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface):
            raise ValueError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface = triviaGameGlobalControllersRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

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
        administratorProvider: AdministratorProviderInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise ValueError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameControllersRepository: TriviaGameControllersRepositoryInterface = triviaGameControllersRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return

        twitchChannelId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if twitchChannelId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
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
            twitchChannelId = twitchChannelId,
            userName = userName
        )

        if result is RemoveTriviaGameControllerResult.DOES_NOT_EXIST:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ {userName} is not a trivia game controller')
        elif result is RemoveTriviaGameControllerResult.ERROR:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An error occurred when trying to remove {userName} as a trivia game controller!')
        elif result is RemoveTriviaGameControllerResult.REMOVED:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Removed {userName} as a trivia game controller')
        else:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An unknown error occurred when trying to remove {userName} as a trivia game controller!')
            self.__timber.log('RemoveTriviaControllerCommand', f'Encountered unknown RemoveTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            raise ValueError(f'Encountered unknown RemoveTriviaGameControllerResult value ({result}) when trying to remove \"{userName}\" as a trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

        self.__timber.log('RemoveTriviaControllerCommand', f'Handled !removetriviacontroller command with {result} result for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class RemoveUserCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserName()

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

        await self.__twitchTokensRepository.removeUser(userName)
        userId = await self.__userIdsRepository.requireUserId(userName = userName)

        await self.__modifyUserDataHelper.setUserData(
            actionType = ModifyUserActionType.REMOVE,
            userId = userId,
            userName = userName
        )

        await self.__twitchUtils.safeSend(ctx, f'ⓘ To remove user \"{userName}\" ({userId}), please respond with `!confirm`')
        self.__timber.log('RemoveUserCommand', f'Handled !removeuser command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class SetFuntoonTokenCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        funtoonTokensRepository: FuntoonTokensRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(funtoonTokensRepository, FuntoonTokensRepositoryInterface):
            raise ValueError(f'funtoonTokensRepository argument is malformed: \"{funtoonTokensRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__funtoonTokensRepository: FuntoonTokensRepositoryInterface = funtoonTokensRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if ctx.getAuthorName().lower() != user.getHandle().lower() and ctx.getAuthorId() != administrator:
            self.__timber.log('SetFuntoonTokenCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('SetFuntoonTokenCommand', f'Not enough arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !setfuntoontoken command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Token argument is necessary for the !setfuntoontoken command. Example: !setfuntoontoken {self.__getRandomTokenStr()}')
            return

        token: Optional[str] = splits[1]
        if not utils.isValidStr(token):
            self.__timber.log('SetFuntoonTokenCommand', f'Invalid token argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} for the !setfuntoontoken command: \"{splits}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Token argument is necessary for the !setfuntoontoken command. Example: !setfuntoontoken {self.__getRandomTokenStr()}')
            return

        await self.__funtoonTokensRepository.setToken(
            token = token,
            twitchChannel = user.getHandle()
        )

        self.__timber.log('SetFuntoonTokenCommand', f'Handled !setfuntoontoken command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Funtoon token has been updated')

    def __getRandomTokenStr(self) -> str:
        randomUuid = str(uuid.uuid4())
        randomUuid = randomUuid.replace('-', '')

        if len(randomUuid) > 16:
            randomUuid = randomUuid[0:16]

        return randomUuid


class SetTwitchCodeCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepositoryInterface argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

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

        await self.__twitchTokensRepository.addUser(
            code = code,
            twitchChannel = user.getHandle(),
        )

        self.__timber.log('SetTwitchCodeCommand', f'Handled !settwitchcode command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Twitch code has been updated')

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


class SuperTriviaCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise ValueError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise ValueError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise ValueError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface = triviaGameMachine
        self.__triviaSettingsRepository: TriviaSettingsRepositoryInterface = triviaSettingsRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

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
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId()
        ):
            return

        numberOfGames = 1
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2:
            numberOfGamesStr = splits[1]

            try:
                numberOfGames = int(numberOfGamesStr)
            except (SyntaxError, TypeError, ValueError) as e:
                self.__timber.log('SuperTriviaCommand', f'Unable to convert the numberOfGamesStr ({numberOfGamesStr}) argument into an int (given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}): {e}', e, traceback.format_exc())
                await self.__twitchUtils.safeSend(ctx, f'⚠ Error converting the given count into an int. Example: !supertrivia 2')
                return

            maxNumberOfGames = await self.__triviaSettingsRepository.getMaxSuperTriviaGameQueueSize()

            if numberOfGames < 1 or numberOfGames > maxNumberOfGames:
                self.__timber.log('SuperTriviaCommand', f'The numberOfGames argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is out of bounds ({numberOfGames}) (converted from \"{numberOfGamesStr}\")')
                await self.__twitchUtils.safeSend(ctx, f'⚠ The given count is an unexpected number, please try again. Example: !supertrivia 2')
                return

        startNewSuperTriviaGameAction = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            numberOfGames = numberOfGames
        )

        if startNewSuperTriviaGameAction is None:
            return

        self.__triviaGameMachine.submitAction(startNewSuperTriviaGameAction)
        self.__timber.log('SuperTriviaCommand', f'Handled !supertrivia command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class SwQuoteCommand(AbsCommand):

    def __init__(
        self,
        starWarsQuotesRepository: StarWarsQuotesRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        if not isinstance(starWarsQuotesRepository, StarWarsQuotesRepositoryInterface):
            raise ValueError(f'starWarsQuotesRepository argument is malformed: \"{starWarsQuotesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__starWarsQuotesRepository: StarWarsQuotesRepositoryInterface = starWarsQuotesRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        timeZones = user.getTimeZones()
        if timeZones is None or len(timeZones) == 0:
            return

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
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        translationHelper: TranslationHelper,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 15)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(translationHelper, TranslationHelper):
            raise ValueError(f'translationHelper argument is malformed: \"{translationHelper}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__timber: TimberInterface = timber
        self.__translationHelper: TranslationHelper = translationHelper
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def __determineOptionalLanguageEntry(self, splits: List[str]) -> Optional[LanguageEntry]:
        if not utils.hasItems(splits):
            raise ValueError(f'splits argument is malformed: \"{splits}\"')

        if len(splits[1]) >= 3 and splits[1][0:2] == '--':
            return await self.__languagesRepository.getLanguageForCommand(
                command = splits[1][2:],
                hasIso6391Code = True
            )

        return None

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTranslateEnabled() or not user.isTranslateEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, f'⚠ Please specify the text you want to translate. Example: !translate I like tamales')
            return

        targetLanguageEntry = await self.__determineOptionalLanguageEntry(splits)

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
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise ValueError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise ValueError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise ValueError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise ValueError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('TriviaInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to get trivia question info as an invalid emote argument was given. Example: !triviainfo {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        emote = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('TriviaInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to get trivia question info as an invalid emote argument was given. Example: !triviainfo {self.__triviaEmoteGenerator.getRandomEmote()}')
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
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
            additionalAnswersLen = len(additionalAnswers.getAdditionalAnswers())

        await self.__twitchUtils.safeSend(ctx, f'{normalizedEmote} {reference.getTriviaSource().toStr()}:{reference.getTriviaId()} triviaType:{reference.getTriviaType().toStr()} additionalAnswers:{additionalAnswersLen} isLocal:{str(reference.getTriviaSource().isLocal()).lower()}')
        self.__timber.log('TriviaInfoCommand', f'Handled !triviainfo command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class TtsCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __chooseRandomSoundAlert(self) -> Optional[SoundAlert]:
        soundAlerts: List[Optional[SoundAlert]] = list(SoundAlert)
        soundAlerts.append(None)
        return random.choice(soundAlerts)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isTtsEnabled():
            return

        administrator = await self.__administratorProvider.getAdministratorUserId()

        if user.getHandle().lower() != ctx.getAuthorName() and administrator != ctx.getAuthorId():
            self.__timber.log('TtsCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, '⚠ Missing a message argument! Example: !tts Hello, World!')
            return

        message = ' '.join(splits[1:])
        if not utils.isValidStr(message):
            await self.__twitchUtils.safeSend(ctx, '⚠ Missing a message argument! Example: !tts Hello, World!')
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = await self.__chooseRandomSoundAlert(),
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
            ttsEvent = TtsEvent(
                message = message,
                twitchChannel = user.getHandle(),
                userId = ctx.getAuthorId(),
                userName = ctx.getAuthorName(),
                donation = None,
                provider = TtsProvider.DEC_TALK,
                raidInfo = None
            )
        ))

        self.__timber.log('TtsCommand', f'Handled !tts command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class TwitchInfoCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise ValueError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise ValueError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if ctx.getAuthorId() != administrator:
            self.__timber.log('TwitchInfoCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(user.getHandle())

        if not utils.isValidStr(twitchAccessToken):
            twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
            twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)

            if not utils.isValidStr(twitchAccessToken):
                self.__timber.log('TwitchInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but was unable to retrieve a valid Twitch access token')
                await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to retrieve a valid Twitch access token to use with this command!')
                return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('TwitchInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to retrieve Twitch info as no username argument was given. Example: !twitchinfo {user.getHandle()}')
            return

        userName: Optional[str] = splits[1]
        if not utils.isValidStr(userName) or not utils.strContainsAlphanumericCharacters(userName):
            self.__timber.log('TwitchInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to retrieve Twitch info as no username argument was given. Example: !twitchinfo {user.getHandle()}')
            return

        userInfo: Optional[TwitchUserDetails] = None
        try:
            userInfo = await self.__twitchApiService.fetchUserDetailsWithUserName(
                twitchAccessToken = twitchAccessToken,
                userName = userName
            )
        except:
            pass

        if userInfo is None:
            self.__timber.log('TwitchInfoCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}, but the TwitchApiService call failed')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to retrieve Twitch info for \"{userName}\" as the Twitch API service call failed')
            return

        userInfoStr = await self.__toStr(userInfo)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Twitch info for {userName} — {userInfoStr}')
        self.__timber.log('TwitchInfoCommand', f'Handled !twitchinfo command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

    async def __toStr(self, userInfo: TwitchUserDetails) -> str:
        if not isinstance(userInfo, TwitchUserDetails):
            raise ValueError(f'userInfo argument is malformed: \"{userInfo}\"')

        broadcasterType = userInfo.getBroadcasterType()
        displayName = userInfo.getDisplayName()
        userId = userInfo.getUserId()
        userType = userInfo.getUserType()
        return f'broadcasterType:\"{broadcasterType}\", displayName:\"{displayName}\", userId:\"{userId}\", userType:\"{userType}\"'


class TwitterCommand(AbsCommand):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 5)
    ):
        if not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
        timber: TimberInterface,
        triviaBanHelper: TriviaBanHelperInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaBanHelper, TriviaBanHelperInterface):
            raise TypeError(f'triviaBanHelper argument is malformed: \"{triviaBanHelper}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise TypeError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise TypeError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaBanHelper: TriviaBanHelperInterface = triviaBanHelper
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId(),
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
            twitchChannel = user.getHandle(),
            twitchChannelId = await ctx.getTwitchChannelId()
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
        locationsRepository: LocationsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        weatherRepository: WeatherRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(locationsRepository, LocationsRepositoryInterface):
            raise ValueError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(weatherRepository, WeatherRepositoryInterface):
            raise ValueError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__locationsRepository: LocationsRepositoryInterface = locationsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__weatherRepository: WeatherRepositoryInterface = weatherRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isWeatherEnabled() or not user.isWeatherEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        locationId = user.getLocationId()

        if not utils.isValidStr(locationId):
            await self.__twitchUtils.safeSend(ctx, f'⚠ Weather for {user.getHandle()} is enabled, but no location ID is available')
            return

        location = await self.__locationsRepository.getLocation(locationId)

        try:
            weatherReport = await self.__weatherRepository.fetchWeather(location)
            await self.__twitchUtils.safeSend(ctx, weatherReport.toStr())
        except OneWeatherApiKeyUnavailableException as e:
            self.__timber.log('WeatherCommand', f'Unable to fetch weather as no One Weather API key is available: {e}', e, traceback.format_exc())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WeatherCommand', f'Error fetching weather for \"{locationId}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, '⚠ Error fetching weather')

        self.__timber.log('WeatherCommand', f'Handled !weather command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class WordCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        wordOfTheDayRepository: WordOfTheDayRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise ValueError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface):
            raise ValueError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__wordOfTheDayRepository: WordOfTheDayRepositoryInterface = wordOfTheDayRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isWordOfTheDayEnabled() or not user.isWordOfTheDayEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            exampleEntry = await self.__languagesRepository.getExampleLanguageEntry(hasWotdApiCode = True)
            allWotdApiCodes = await self.__languagesRepository.getAllWotdApiCodes()
            await self.__twitchUtils.safeSend(ctx, f'⚠ A language code is necessary for the !word command. Example: !word {exampleEntry.requireWotdApiCode()}. Available languages: {allWotdApiCodes}')
            return

        language = splits[1]
        languageEntry: LanguageEntry

        try:
            languageEntry = await self.__languagesRepository.requireLanguageForCommand(
                command = language,
                hasWotdApiCode = True
            )
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error retrieving language entry: \"{language}\": {e}', e, traceback.format_exc())
            allWotdApiCodes = await self.__languagesRepository.getAllWotdApiCodes()
            await self.__twitchUtils.safeSend(ctx, f'⚠ The given language code is not supported by the !word command. Available languages: {allWotdApiCodes}')
            return

        try:
            wotd = await self.__wordOfTheDayRepository.fetchWotd(languageEntry)
            await self.__twitchUtils.safeSend(ctx, wotd.toStr())
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error fetching Word Of The Day for \"{languageEntry.getWotdApiCode()}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error fetching Word Of The Day for \"{languageEntry.getWotdApiCode()}\"')

        self.__timber.log('WordCommand', f'Handled !word command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
