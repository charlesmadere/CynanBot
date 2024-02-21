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
from CynanBot.generalSettingsRepositorySnapshot import \
    GeneralSettingsRepositorySnapshot
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
from CynanBot.trivia.actions.clearSuperTriviaQueueTriviaAction import \
    ClearSuperTriviaQueueTriviaAction
from CynanBot.trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from CynanBot.trivia.banned.addBannedTriviaGameControllerResult import \
    AddBannedTriviaGameControllerResult
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
from CynanBot.trivia.score.triviaScoreRepositoryInterface import \
    TriviaScoreRepositoryInterface
from CynanBot.trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import \
    ShinyTriviaOccurencesRepositoryInterface
from CynanBot.trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import \
    ToxicTriviaOccurencesRepositoryInterface
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
from CynanBot.weather.weatherRepositoryInterface import \
    WeatherRepositoryInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class AbsCommand(ABC):

    @abstractmethod
    async def handleCommand(self, ctx: TwitchContext):
        pass


class AddBannedTriviaControllerCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface), f"malformed {bannedTriviaGameControllersRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface = bannedTriviaGameControllersRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if ctx.getAuthorId() != administrator:
            self.__timber.log('AddBannedTriviaControllerCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('AddBannedTriviaControllerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add banned trivia controller as no username argument was given. Example: !addbannedtriviacontroller {administrator}')
            return

        userName: Optional[str] = utils.removePreceedingAt(splits[1])
        if not utils.isValidStr(userName):
            self.__timber.log('AddBannedTriviaControllerCommand', f'Attempted to handle command for {userName}:{ctx.getAuthorId()} in {user.getHandle()}, but username argument is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to add banned trivia controller as username argument is malformed. Example: !addbannedtriviacontroller {user.getHandle()}')
            return

        result = await self.__bannedTriviaGameControllersRepository.addBannedController(
            userName = userName
        )

        if result is AddBannedTriviaGameControllerResult.ADDED:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Added {userName} as a banned trivia game controller.')
        elif result is AddBannedTriviaGameControllerResult.ALREADY_EXISTS:
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Tried adding {userName} as a banned trivia game controller, but they already were one.')
        elif result is AddBannedTriviaGameControllerResult.ERROR:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An error occurred when trying to add {userName} as a banned trivia game controller!')
        else:
            await self.__twitchUtils.safeSend(ctx, f'⚠ An unknown error occurred when trying to add {userName} as a banned trivia game controller!')
            self.__timber.log('AddBannedTriviaControllerCommand', f'Encountered unknown AddBannedTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
            raise ValueError(f'Encountered unknown AddBannedTriviaGameControllerResult value ({result}) when trying to add \"{userName}\" as a banned trivia game controller for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')

        self.__timber.log('AddBannedTriviaControllerCommand', f'Handled !addbannedtriviacontroller command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}')


class AddGlobalTriviaControllerCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface), f"malformed {triviaGameGlobalControllersRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface = triviaGameGlobalControllersRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if administrator != ctx.getAuthorId():
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
        assert isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface), f"malformed {additionalTriviaAnswersRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface), f"malformed {triviaEmoteGenerator=}"
        assert isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface), f"malformed {triviaHistoryRepository=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(answerDelimiter, str), f"malformed {answerDelimiter=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface), f"malformed {triviaGameControllersRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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

        administrator = await self.__administratorProvider.getAdministratorUserId()

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
        administratorProvider: AdministratorProviderInterface,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(modifyUserDataHelper, ModifyUserDataHelper), f"malformed {modifyUserDataHelper=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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

        actionId = await self.__triviaIdGenerator.generateActionId()
        answer = ' '.join(splits[1:])

        self.__triviaGameMachine.submitAction(CheckAnswerTriviaAction(
            actionId = actionId,
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
        timber: TimberInterface,
        triviaBanHelper: TriviaBanHelperInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaBanHelper, TriviaBanHelperInterface), f"malformed {triviaBanHelper=}"
        assert isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface), f"malformed {triviaEmoteGenerator=}"
        assert isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface), f"malformed {triviaHistoryRepository=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
            userId = ctx.getAuthorId(),
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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(authRepository, AuthRepository), f"malformed {authRepository=}"
        assert bannedWordsRepository is None or isinstance(bannedWordsRepository, BannedWordsRepositoryInterface), f"malformed {bannedWordsRepository=}"
        assert cheerActionsRepository is None or isinstance(cheerActionsRepository, CheerActionsRepositoryInterface), f"malformed {cheerActionsRepository=}"
        assert funtoonTokensRepository is None or isinstance(funtoonTokensRepository, FuntoonTokensRepositoryInterface), f"malformed {funtoonTokensRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isLiveOnTwitchRepository is None or isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface), f"malformed {isLiveOnTwitchRepository=}"
        assert locationsRepository is None or isinstance(locationsRepository, LocationsRepositoryInterface), f"malformed {locationsRepository=}"
        assert isinstance(modifyUserDataHelper, ModifyUserDataHelper), f"malformed {modifyUserDataHelper=}"
        assert mostRecentChatsRepository is None or isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface), f"malformed {mostRecentChatsRepository=}"
        assert openTriviaDatabaseTriviaQuestionRepository is None or isinstance(openTriviaDatabaseTriviaQuestionRepository, OpenTriviaDatabaseTriviaQuestionRepository), f"malformed {openTriviaDatabaseTriviaQuestionRepository=}"
        assert soundPlayerSettingsRepository is None or isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface), f"malformed {soundPlayerSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert triviaSettingsRepository is None or isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface), f"malformed {triviaSettingsRepository=}"
        assert ttsSettingsRepository is None or isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface), f"malformed {ttsSettingsRepository=}"
        assert twitchFollowerRepository is None or isinstance(twitchFollowerRepository, TwitchFollowerRepositoryInterface), f"malformed {twitchFollowerRepository=}"
        assert twitchTokensRepository is None or isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert weatherRepository is None or isinstance(weatherRepository, WeatherRepositoryInterface), f"malformed {weatherRepository=}"
        assert websocketConnectionServer is None or isinstance(websocketConnectionServer, WebsocketConnectionServerInterface), f"malformed {websocketConnectionServer=}"
        assert wordOfTheDayRepository is None or isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface), f"malformed {wordOfTheDayRepository=}"

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


class ClearSuperTriviaQueueCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        triviaIdGenerator: TriviaIdGeneratorInterface,
        triviaUtils: TriviaUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"
        assert isinstance(triviaIdGenerator, TriviaIdGeneratorInterface), f"malformed {triviaIdGenerator=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameMachine: TriviaGameMachineInterface = triviaGameMachine
        self.__triviaIdGenerator: TriviaIdGeneratorInterface = triviaIdGenerator
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

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

        actionId = await self.__triviaIdGenerator.generateActionId()

        self.__triviaGameMachine.submitAction(ClearSuperTriviaQueueTriviaAction(
            actionId = actionId,
            twitchChannel = user.getHandle()
        ))

        self.__timber.log('ClearSuperTriviaQueueCommand', f'Handled !clearsupertriviaqueue command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class CommandsCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaUtils: Optional[TriviaUtilsInterface],
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 30)
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert triviaUtils is None or isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaUtils: Optional[TriviaUtilsInterface] = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def __buildLanguageCommandsList(
        self,
        generalSettings: GeneralSettingsRepositorySnapshot,
        user: UserInterface
    ) -> List[str]:
        assert isinstance(generalSettings, GeneralSettingsRepositorySnapshot), f"malformed {generalSettings=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"

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
        user: UserInterface
    ) -> List[str]:
        assert isinstance(generalSettings, GeneralSettingsRepositorySnapshot), f"malformed {generalSettings=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"

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
        user: UserInterface
    ) -> List[str]:
        if not utils.isValidBool(isMod):
            raise ValueError(f'isMod argument is malformed: \"{isMod}\"')
        assert isinstance(generalSettings, GeneralSettingsRepositorySnapshot), f"malformed {generalSettings=}"
        if not utils.isValidStr(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        assert isinstance(user, UserInterface), f"malformed {user=}"

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
        administratorProvider: AdministratorProviderInterface,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(modifyUserDataHelper, ModifyUserDataHelper), f"malformed {modifyUserDataHelper=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(cutenessRepository, CutenessRepositoryInterface), f"malformed {cutenessRepository=}"
        assert isinstance(cutenessUtils, CutenessUtilsInterface), f"malformed {cutenessUtils=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__cutenessUtils: CutenessUtilsInterface = cutenessUtils
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    def __cutenessLeaderboardResultToStr(self, result: CutenessLeaderboardResult) -> str:
        assert isinstance(result, CutenessLeaderboardResult), f"malformed {result=}"

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
        assert isinstance(result, CutenessResult), f"malformed {result=}"

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
        cutenessRepository: CutenessRepositoryInterface,
        cutenessUtils: CutenessUtilsInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', ',
        cooldown: timedelta = timedelta(seconds = 15)
    ):
        assert isinstance(cutenessRepository, CutenessRepositoryInterface), f"malformed {cutenessRepository=}"
        assert isinstance(cutenessUtils, CutenessUtilsInterface), f"malformed {cutenessUtils=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
            twitchChannel = user.getHandle()
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
        assert isinstance(cutenessRepository, CutenessRepositoryInterface), f"malformed {cutenessRepository=}"
        assert isinstance(cutenessUtils, CutenessUtilsInterface), f"malformed {cutenessUtils=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(entryDelimiter, str), f"malformed {entryDelimiter=}"
        assert isinstance(leaderboardDelimiter, str), f"malformed {leaderboardDelimiter=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(cheerActionIdGenerator, CheerActionIdGeneratorInterface), f"malformed {cheerActionIdGenerator=}"
        assert isinstance(cheerActionsRepository, CheerActionsRepositoryInterface), f"malformed {cheerActionsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__cheerActionIdGenerator: CheerActionIdGeneratorInterface = cheerActionIdGenerator
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __actionToStr(self, action: CheerAction) -> str:
        assert isinstance(action, CheerAction), f"malformed {action=}"

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
        assert isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface), f"malformed {additionalTriviaAnswersRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface), f"malformed {triviaEmoteGenerator=}"
        assert isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface), f"malformed {triviaHistoryRepository=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(answerDelimiter, str), f"malformed {answerDelimiter=}"

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
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface), f"malformed {bannedTriviaGameControllersRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(cheerActionsRepository, CheerActionsRepositoryInterface), f"malformed {cheerActionsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter

    async def __actionsToStr(self, actions: List[CheerAction]) -> str:
        assert isinstance(actions, List), f"malformed {actions=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface), f"malformed {triviaGameGlobalControllersRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface), f"malformed {additionalTriviaAnswersRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface), f"malformed {triviaEmoteGenerator=}"
        assert isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface), f"malformed {triviaHistoryRepository=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(answerDelimiter, str), f"malformed {answerDelimiter=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface), f"malformed {triviaGameControllersRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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

        administrator = await self.__administratorProvider.getAdministratorUserId()

        if user.getHandle().lower() != ctx.getAuthorName().lower() and administrator != ctx.getAuthorId():
            self.__timber.log('GetTriviaControllersCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        controllers = await self.__triviaGameControllersRepository.getControllers(user.getHandle())
        await self.__twitchUtils.safeSend(ctx, await self.__triviaUtils.getTriviaGameControllers(controllers))
        self.__timber.log('GetTriviaControllersCommand', f'Handled !gettriviacontrollers command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class GiveCutenessCommand(AbsCommand):

    def __init__(
        self,
        cutenessRepository: CutenessRepositoryInterface,
        timber: TimberInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(cutenessRepository, CutenessRepositoryInterface), f"malformed {cutenessRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__cutenessRepository: CutenessRepositoryInterface = cutenessRepository
        self.__timber: TimberInterface = timber
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

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

        userName: Optional[str] = splits[1]
        if not utils.isValidStr(userName) or not utils.strContainsAlphanumericCharacters(userName):
            self.__timber.log('GiveCutenessCommand', f'Username given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is malformed: \"{userName}\"')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Username argument is malformed. Example: !givecuteness {user.getHandle()} 5')
            return

        incrementAmountStr: Optional[str] = splits[2]
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
        userId: Optional[str] = await self.__userIdsRepository.fetchUserId(userName = userName)

        if not utils.isValidStr(userId):
            await self.__twitchUtils.safeSend(ctx, f'⚠ Unable to fetch user ID for \"{userName}\"!')
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
        jishoHelper: JishoHelperInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(jishoHelper, JishoHelperInterface), f"malformed {jishoHelper=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(cutenessRepository, CutenessRepositoryInterface), f"malformed {cutenessRepository=}"
        assert isinstance(cutenessUtils, CutenessUtilsInterface), f"malformed {cutenessUtils=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(pokepediaRepository, PokepediaRepository), f"malformed {pokepediaRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(pokepediaRepository, PokepediaRepository), f"malformed {pokepediaRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(languagesRepository, LanguagesRepositoryInterface), f"malformed {languagesRepository=}"
        assert isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface), f"malformed {recurringActionsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __disableRecurringAction(
        self,
        ctx: TwitchContext,
        user: UserInterface,
        actionType: RecurringActionType
    ):
        assert isinstance(ctx, TwitchContext), f"malformed {ctx=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(actionType, RecurringActionType), f"malformed {actionType=}"

        if actionType is RecurringActionType.SUPER_TRIVIA:
            await self.__disableSuperTriviaRecurringAction(
                ctx = ctx,
                user = user
            )
        elif actionType is RecurringActionType.WEATHER:
            await self.__disableWeatherRecurringAction(
                ctx = ctx,
                user = user
            )
        elif actionType is RecurringActionType.WORD_OF_THE_DAY:
            await self.__disableWordOfTheDayRecurringAction(
                ctx = ctx,
                user = user
            )
        else:
            raise RuntimeError(f'actionType is unknown: \"{actionType}\"')

    async def __disableSuperTriviaRecurringAction(
        self,
        ctx: TwitchContext,
        user: UserInterface
    ):
        assert isinstance(ctx, TwitchContext), f"malformed {ctx=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"

        recurringAction = SuperTriviaRecurringAction(
            enabled = False,
            twitchChannel = user.getHandle()
        )

        await self.__recurringActionsRepository.setRecurringAction(recurringAction)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Disabled recurring Super Trivia action')

    async def __disableWeatherRecurringAction(
        self,
        ctx: TwitchContext,
        user: UserInterface
    ):
        assert isinstance(ctx, TwitchContext), f"malformed {ctx=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"

        recurringAction = WeatherRecurringAction(
            enabled = False,
            twitchChannel = user.getHandle()
        )

        await self.__recurringActionsRepository.setRecurringAction(recurringAction)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Disabled recurring Weather action')

    async def __disableWordOfTheDayRecurringAction(
        self,
        ctx: TwitchContext,
        user: UserInterface
    ):
        assert isinstance(ctx, TwitchContext), f"malformed {ctx=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"

        recurringAction = WordOfTheDayRecurringAction(
            enabled = False,
            twitchChannel = user.getHandle()
        )

        await self.__recurringActionsRepository.setRecurringAction(recurringAction)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ Disabled recurring Word Of The Day action')

    async def __enableSuperTriviaRecurringAction(
        self,
        ctx: TwitchContext,
        user: UserInterface,
        splits: List[str]
    ):
        assert isinstance(ctx, TwitchContext), f"malformed {ctx=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"
        if not utils.hasItems(splits):
            raise ValueError(f'splits argument is malformed: \"{splits}\"')

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
        assert isinstance(ctx, TwitchContext), f"malformed {ctx=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"
        if not utils.hasItems(splits):
            raise ValueError(f'splits argument is malformed: \"{splits}\"')

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
        assert isinstance(ctx, TwitchContext), f"malformed {ctx=}"
        assert isinstance(user, UserInterface), f"malformed {user=}"
        if not utils.hasItems(splits):
            raise ValueError(f'splits argument is malformed: \"{splits}\"')

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

        if await self.__parseIsDisabling(splits):
            await self.__disableRecurringAction(
                ctx = ctx,
                user = user,
                actionType = actionType
            )
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

    async def __parseIsDisabling(self, splits: List[str]) -> bool:
        if not utils.hasItems(splits):
            raise ValueError(f'splits argument is malformed: \"{splits}\"')

        if len(splits) >= 3 and utils.isValidStr(splits[2]):
            thirdArgument = splits[2]
            return thirdArgument in ('disable', 'off', '0')

        return False

    async def __parseMinutesBetween(self, actionType: RecurringActionType, splits: List[str]) -> int:
        assert isinstance(actionType, RecurringActionType), f"malformed {actionType=}"
        if not utils.hasItems(splits):
            raise ValueError(f'splits argument is malformed: \"{splits}\"')

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


class RecurringActionsCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', '
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface), f"malformed {recurringActionsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if user.getHandle().lower() != ctx.getAuthorName().lower() and administrator != ctx.getAuthorId():
            self.__timber.log('RecurringActionsCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return

        recurringActions = await self.__recurringActionsRepository.getAllRecurringActions(user.getHandle())

        if utils.hasItems(recurringActions):
            recurringActionsStrs: List[str] = list()

            for recurringAction in recurringActions:
                recurringActionsStrs.append(recurringAction.getActionType().toReadableStr())

            recurringActionsStr = self.__delimiter.join(recurringActionsStrs)
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Your channel\'s recurring action(s): {recurringActionsStr}')
        else:
            await self.__twitchUtils.safeSend(ctx, 'ⓘ Your channel has no recurring actions')

        self.__timber.log('RecurringActionsCommand', f'Handled !recurringactions command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class RemoveBannedTriviaControllerCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface), f"malformed {bannedTriviaGameControllersRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface), f"malformed {triviaGameGlobalControllersRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface), f"malformed {triviaGameControllersRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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

        administrator = await self.__administratorProvider.getAdministratorUserId()

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
        administratorProvider: AdministratorProviderInterface,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: TimberInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(modifyUserDataHelper, ModifyUserDataHelper), f"malformed {modifyUserDataHelper=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(funtoonTokensRepository, FuntoonTokensRepositoryInterface), f"malformed {funtoonTokensRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameBuilder, TriviaGameBuilderInterface), f"malformed {triviaGameBuilder=}"
        assert isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"
        assert isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface), f"malformed {triviaSettingsRepository=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(starWarsQuotesRepository, StarWarsQuotesRepositoryInterface), f"malformed {starWarsQuotesRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(languagesRepository, LanguagesRepositoryInterface), f"malformed {languagesRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(translationHelper, TranslationHelper), f"malformed {translationHelper=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface), f"malformed {additionalTriviaAnswersRepository=}"
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface), f"malformed {triviaEmoteGenerator=}"
        assert isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface), f"malformed {triviaHistoryRepository=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
            additionalAnswersLen = len(additionalAnswers.getAdditionalAnswers())

        await self.__twitchUtils.safeSend(ctx, f'{normalizedEmote} {reference.getTriviaSource().toStr()}:{reference.getTriviaId()} triviaType:{reference.getTriviaType().toStr()} additionalAnswers:{additionalAnswersLen} isLocal:{str(reference.getTriviaSource().isLocal()).lower()}')
        self.__timber.log('TriviaInfoCommand', f'Handled !triviainfo command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')


class TriviaScoreCommand(AbsCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface,
        timber: TimberInterface,
        toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface,
        triviaScoreRepository: TriviaScoreRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 2)
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(shinyTriviaOccurencesRepository, ShinyTriviaOccurencesRepositoryInterface), f"malformed {shinyTriviaOccurencesRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepositoryInterface), f"malformed {toxicTriviaOccurencesRepository=}"
        assert isinstance(triviaScoreRepository, TriviaScoreRepositoryInterface), f"malformed {triviaScoreRepository=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(userIdsRepository, UserIdsRepositoryInterface), f"malformed {userIdsRepository=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface = shinyTriviaOccurencesRepository
        self.__timber: TimberInterface = timber
        self.__toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface = toxicTriviaOccurencesRepository
        self.__triviaScoreRepository: TriviaScoreRepositoryInterface = triviaScoreRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled() and not user.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaScoreEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        userName: Optional[str] = None

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])
        else:
            userName = ctx.getAuthorName()

        userId: Optional[str] = None

        # this means that a user is querying for another user's trivia score
        if userName.lower() != ctx.getAuthorName().lower():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                self.__timber.log('TriviaScoreCommand', f'Unable to find user ID for \"{userName}\" in the database')
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


class TtsCommand(AbsCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(streamAlertsManager, StreamAlertsManagerInterface), f"malformed {streamAlertsManager=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(administratorProvider, AdministratorProviderInterface), f"malformed {administratorProvider=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchApiService, TwitchApiServiceInterface), f"malformed {twitchApiService=}"
        assert isinstance(twitchHandleProvider, TwitchHandleProviderInterface), f"malformed {twitchHandleProvider=}"
        assert isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface), f"malformed {twitchTokensRepository=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        assert isinstance(userInfo, TwitchUserDetails), f"malformed {userInfo=}"

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
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaBanHelper, TriviaBanHelperInterface), f"malformed {triviaBanHelper=}"
        assert isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface), f"malformed {triviaEmoteGenerator=}"
        assert isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface), f"malformed {triviaHistoryRepository=}"
        assert isinstance(triviaUtils, TriviaUtilsInterface), f"malformed {triviaUtils=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"

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
        locationsRepository: LocationsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        weatherRepository: WeatherRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(locationsRepository, LocationsRepositoryInterface), f"malformed {locationsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(weatherRepository, WeatherRepositoryInterface), f"malformed {weatherRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(languagesRepository, LanguagesRepositoryInterface), f"malformed {languagesRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface), f"malformed {wordOfTheDayRepository=}"
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"

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
