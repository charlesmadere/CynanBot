from .absChatCommand import AbsChatCommand
from ..aniv.anivSettingsRepositoryInterface import AnivSettingsRepositoryInterface
from ..aniv.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from ..cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from ..cheerActions.timeout.timeoutCheerActionHistoryRepositoryInterface import \
    TimeoutCheerActionHistoryRepositoryInterface
from ..contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from ..funtoon.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from ..language.wordOfTheDayRepositoryInterface import WordOfTheDayRepositoryInterface
from ..location.locationsRepositoryInterface import LocationsRepositoryInterface
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..misc.authRepository import AuthRepository
from ..misc.clearable import Clearable
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from ..soundPlayerManager.soundPlayerRandomizerHelperInterface import SoundPlayerRandomizerHelperInterface
from ..soundPlayerManager.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from ..supStreamer.supStreamerRepositoryInterface import SupStreamerRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..trivia.triviaRepositories.openTriviaDatabaseTriviaQuestionRepository import \
    OpenTriviaDatabaseTriviaQuestionRepository
from ..trivia.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from ..tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from ..twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from ..twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.modifyUserDataHelper import ModifyUserDataHelper
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface
from ..weather.weatherRepositoryInterface import WeatherRepositoryInterface
from ..websocketConnection.websocketConnectionServerInterface import WebsocketConnectionServerInterface


class ClearCachesChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        anivSettingsRepository: AnivSettingsRepositoryInterface | None,
        authRepository: AuthRepository,
        bannedWordsRepository: BannedWordsRepositoryInterface | None,
        cheerActionsRepository: CheerActionsRepositoryInterface | None,
        funtoonTokensRepository: FuntoonTokensRepositoryInterface | None,
        generalSettingsRepository: GeneralSettingsRepository,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface | None,
        locationsRepository: LocationsRepositoryInterface | None,
        modifyUserDataHelper: ModifyUserDataHelper,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface | None,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface | None,
        openTriviaDatabaseTriviaQuestionRepository: OpenTriviaDatabaseTriviaQuestionRepository | None,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface | None,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface | None,
        supStreamerRepository: SupStreamerRepositoryInterface | None,
        timber: TimberInterface,
        timeoutCheerActionHistoryRepository: TimeoutCheerActionHistoryRepositoryInterface | None,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface | None,
        ttsSettingsRepository: TtsSettingsRepositoryInterface | None,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface | None,
        twitchTokensRepository: TwitchTokensRepositoryInterface | None,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        weatherRepository: WeatherRepositoryInterface | None,
        websocketConnectionServer: WebsocketConnectionServerInterface | None,
        wordOfTheDayRepository: WordOfTheDayRepositoryInterface | None
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif anivSettingsRepository is not None and not isinstance(anivSettingsRepository, AnivSettingsRepositoryInterface):
            raise TypeError(f'anivSettingsRepository argument is malformed: \"{anivSettingsRepository}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise TypeError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif bannedWordsRepository is not None and not isinstance(bannedWordsRepository, BannedWordsRepositoryInterface):
            raise TypeError(f'bannedWordsRepository argument is malformed: \"{bannedWordsRepository}\"')
        elif cheerActionsRepository is not None and not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif funtoonTokensRepository is not None and not isinstance(funtoonTokensRepository, FuntoonTokensRepositoryInterface):
            raise TypeError(f'funtoonTokensRepository argument is malformed: \"{funtoonTokensRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif isLiveOnTwitchRepository is not None and not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif locationsRepository is not None and not isinstance(locationsRepository, LocationsRepositoryInterface):
            raise TypeError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise TypeError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif mostRecentAnivMessageRepository is not None and not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif mostRecentChatsRepository is not None and not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise TypeError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif openTriviaDatabaseTriviaQuestionRepository is not None and not isinstance(openTriviaDatabaseTriviaQuestionRepository, OpenTriviaDatabaseTriviaQuestionRepository):
            raise TypeError(f'openTriviaDatabaseTriviaQuestionRepository argument is malformed: \"{openTriviaDatabaseTriviaQuestionRepository}\"')
        elif soundPlayerRandomizerHelper is not None and not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif soundPlayerSettingsRepository is not None and not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif supStreamerRepository is not None and not isinstance(supStreamerRepository, SupStreamerRepositoryInterface):
            raise TypeError(f'supStreamerRepository argument is malformed: \"{supStreamerRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif timeoutCheerActionHistoryRepository is not None and not isinstance(timeoutCheerActionHistoryRepository, TimeoutCheerActionHistoryRepositoryInterface):
            raise TypeError(f'timeoutCheerActionHistoryRepository argument is malformed: \"{timeoutCheerActionHistoryRepository}\"')
        elif triviaSettingsRepository is not None and not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif ttsSettingsRepository is not None and not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif twitchFollowingStatusRepository is not None and not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif twitchTokensRepository is not None and not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif weatherRepository is not None and not isinstance(weatherRepository, WeatherRepositoryInterface):
            raise TypeError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')
        elif wordOfTheDayRepository is not None and not isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface):
            raise TypeError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

        self.__clearables: list[Clearable | None] = list()
        self.__clearables.append(administratorProvider)
        self.__clearables.append(anivSettingsRepository)
        self.__clearables.append(authRepository)
        self.__clearables.append(bannedWordsRepository)
        self.__clearables.append(cheerActionsRepository)
        self.__clearables.append(funtoonTokensRepository)
        self.__clearables.append(generalSettingsRepository)
        self.__clearables.append(isLiveOnTwitchRepository)
        self.__clearables.append(locationsRepository)
        self.__clearables.append(modifyUserDataHelper)
        self.__clearables.append(mostRecentAnivMessageRepository)
        self.__clearables.append(mostRecentChatsRepository)
        self.__clearables.append(openTriviaDatabaseTriviaQuestionRepository)
        self.__clearables.append(soundPlayerRandomizerHelper)
        self.__clearables.append(soundPlayerSettingsRepository)
        self.__clearables.append(supStreamerRepository)
        self.__clearables.append(timeoutCheerActionHistoryRepository)
        self.__clearables.append(triviaSettingsRepository)
        self.__clearables.append(ttsSettingsRepository)
        self.__clearables.append(twitchFollowingStatusRepository)
        self.__clearables.append(twitchTokensRepository)
        self.__clearables.append(userIdsRepository)
        self.__clearables.append(usersRepository)
        self.__clearables.append(weatherRepository)
        self.__clearables.append(websocketConnectionServer)
        self.__clearables.append(wordOfTheDayRepository)

    async def handleChatCommand(self, ctx: TwitchContext):
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
