import asyncio
import locale
from asyncio import AbstractEventLoop

from src.beanStats.beanStatsPresenter import BeanStatsPresenter
from src.beanStats.beanStatsPresenterInterface import BeanStatsPresenterInterface
from src.beanStats.beanStatsRepository import BeanStatsRepository
from src.beanStats.beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from src.channelPointRedemptions.soundAlertPointRedemption import SoundAlertPointRedemption
from src.chatActions.cheerActionsWizardChatAction import CheerActionsWizardChatAction
from src.chatActions.manager.chatActionsManager import ChatActionsManager
from src.chatActions.manager.chatActionsManagerInterface import ChatActionsManagerInterface
from src.chatActions.persistAllUsersChatAction import PersistAllUsersChatAction
from src.chatBand.chatBandInstrumentSoundsRepository import ChatBandInstrumentSoundsRepository
from src.chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from src.chatLogger.chatLogger import ChatLogger
from src.chatLogger.chatLoggerInterface import ChatLoggerInterface
from src.cheerActions.cheerActionHelper import CheerActionHelper
from src.cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from src.cheerActions.cheerActionJsonMapper import CheerActionJsonMapper
from src.cheerActions.cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from src.cheerActions.cheerActionSettingsRepository import CheerActionSettingsRepository
from src.cheerActions.cheerActionSettingsRepositoryInterface import CheerActionSettingsRepositoryInterface
from src.cheerActions.cheerActionsRepository import CheerActionsRepository
from src.cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from src.cheerActions.cheerActionsWizard import CheerActionsWizard
from src.cheerActions.cheerActionsWizardInterface import CheerActionsWizardInterface
from src.cheerActions.soundAlert.soundAlertCheerActionHelper import SoundAlertCheerActionHelper
from src.cheerActions.soundAlert.soundAlertCheerActionHelperInterface import SoundAlertCheerActionHelperInterface
from src.contentScanner.bannedWordsRepository import BannedWordsRepository
from src.contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from src.contentScanner.contentScanner import ContentScanner
from src.contentScanner.contentScannerInterface import ContentScannerInterface
from src.cynanBot import CynanBot
from src.emojiHelper.emojiHelper import EmojiHelper
from src.emojiHelper.emojiHelperInterface import EmojiHelperInterface
from src.emojiHelper.emojiRepository import EmojiRepository
from src.emojiHelper.emojiRepositoryInterface import EmojiRepositoryInterface
from src.funtoon.apiService.funtoonApiService import FuntoonApiService
from src.funtoon.apiService.funtoonApiServiceInterface import FuntoonApiServiceInterface
from src.funtoon.funtoonHelper import FuntoonHelper
from src.funtoon.funtoonHelperInterface import FuntoonHelperInterface
from src.funtoon.funtoonUserIdProvider import FuntoonUserIdProvider
from src.funtoon.funtoonUserIdProviderInterface import FuntoonUserIdProviderInterface
from src.funtoon.jsonMapper.funtoonJsonMapper import FuntoonJsonMapper
from src.funtoon.jsonMapper.funtoonJsonMapperInterface import FuntoonJsonMapperInterface
from src.funtoon.tokens.funtoonTokensRepository import FuntoonTokensRepository
from src.funtoon.tokens.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from src.google.accessToken.googleApiAccessTokenStorage import GoogleApiAccessTokenStorage
from src.google.accessToken.googleApiAccessTokenStorageInterface import GoogleApiAccessTokenStorageInterface
from src.google.apiService.googleApiService import GoogleApiService
from src.google.apiService.googleApiServiceInterface import GoogleApiServiceInterface
from src.google.jsonMapper.googleJsonMapper import GoogleJsonMapper
from src.google.jsonMapper.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.google.jwtBuilder.googleJwtBuilder import GoogleJwtBuilder
from src.google.jwtBuilder.googleJwtBuilderInterface import GoogleJwtBuilderInterface
from src.language.jsonMapper.languageEntryJsonMapper import LanguageEntryJsonMapper
from src.language.jsonMapper.languageEntryJsonMapperInterface import LanguageEntryJsonMapperInterface
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.location.locationsRepository import LocationsRepository
from src.location.locationsRepositoryInterface import LocationsRepositoryInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.misc.administratorProvider import AdministratorProvider
from src.misc.administratorProviderInterface import AdministratorProviderInterface
from src.misc.authRepository import AuthRepository
from src.misc.backgroundTaskHelper import BackgroundTaskHelper
from src.misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from src.misc.cynanBotUserIdsProvider import CynanBotUserIdsProvider
from src.misc.cynanBotUserIdsProviderInterface import CynanBotUserIdsProviderInterface
from src.misc.generalSettingsRepository import GeneralSettingsRepository
from src.mostRecentChat.mostRecentChatsRepository import MostRecentChatsRepository
from src.mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from src.network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from src.network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.network.networkClientType import NetworkClientType
from src.network.networkJsonMapper import NetworkJsonMapper
from src.network.networkJsonMapperInterface import NetworkJsonMapperInterface
from src.network.requests.requestsClientProvider import RequestsClientProvider
from src.nightbot.nightbotUserIdProvider import NightbotUserIdProvider
from src.nightbot.nightbotUserIdProviderInterface import NightbotUserIdProviderInterface
from src.puptime.puptimeUserIdProvider import PuptimeUserIdProvider
from src.puptime.puptimeUserIdProviderInterface import PuptimeUserIdProviderInterface
from src.sentMessageLogger.sentMessageLogger import SentMessageLogger
from src.sentMessageLogger.sentMessageLoggerInterface import SentMessageLoggerInterface
from src.seryBot.seryBotUserIdProvider import SeryBotUserIdProvider
from src.seryBot.seryBotUserIdProviderInterface import SeryBotUserIdProviderInterface
from src.soundPlayerManager.audioPlayer.audioPlayerSoundPlayerManagerProvider import \
    AudioPlayerSoundPlayerManagerProvider
from src.soundPlayerManager.jsonMapper.soundPlayerJsonMapper import SoundPlayerJsonMapper
from src.soundPlayerManager.jsonMapper.soundPlayerJsonMapperInterface import SoundPlayerJsonMapperInterface
from src.soundPlayerManager.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from src.soundPlayerManager.soundPlayerRandomizerHelper import SoundPlayerRandomizerHelper
from src.soundPlayerManager.soundPlayerRandomizerHelperInterface import SoundPlayerRandomizerHelperInterface
from src.soundPlayerManager.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from src.soundPlayerManager.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from src.soundPlayerManager.soundPlayerType import SoundPlayerType
from src.soundPlayerManager.stub.stubSoundPlayerManagerProvider import StubSoundPlayerManagerProvider
from src.soundPlayerManager.vlc.vlcSoundPlayerManagerProvider import VlcSoundPlayerManagerProvider
from src.storage.backingDatabase import BackingDatabase
from src.storage.backingPsqlDatabase import BackingPsqlDatabase
from src.storage.backingSqliteDatabase import BackingSqliteDatabase
from src.storage.databaseType import DatabaseType
from src.storage.jsonFileReader import JsonFileReader
from src.storage.linesFileReader import LinesFileReader
from src.storage.psqlCredentialsProvider import PsqlCredentialsProvider
from src.storage.psqlCredentialsProviderInterface import PsqlCredentialsProviderInterface
from src.storage.storageJsonMapper import StorageJsonMapper
from src.storage.storageJsonMapperInterface import StorageJsonMapperInterface
from src.streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from src.streamAlertsManager.stub.stubStreamAlertsManager import StubStreamAlertsManager
from src.streamElements.streamElementsUserIdProvider import StreamElementsUserIdProvider
from src.streamElements.streamElementsUserIdProviderInterface import StreamElementsUserIdProviderInterface
from src.streamLabs.streamLabsUserIdProvider import StreamLabsUserIdProvider
from src.streamLabs.streamLabsUserIdProviderInterface import StreamLabsUserIdProviderInterface
from src.tangia.tangiaBotUserIdProvider import TangiaBotUserIdProvider
from src.tangia.tangiaBotUserIdProviderInterface import TangiaBotUserIdProviderInterface
from src.timber.timber import Timber
from src.timber.timberInterface import TimberInterface
from src.tts.compositeTtsManagerInterface import CompositeTtsManagerInterface
from src.tts.jsonMapper.ttsJsonMapper import TtsJsonMapper
from src.tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.stub.stubCompositeTtsManager import StubCompositeTtsManager
from src.twitch.absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from src.twitch.activeChatters.activeChattersRepository import ActiveChattersRepository
from src.twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from src.twitch.api.jsonMapper.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.jsonMapper.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.api.twitchApiService import TwitchApiService
from src.twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from src.twitch.channelEditors.stub.stubTwitchChannelEditorsRepository import StubTwitchChannelEditorsRepository
from src.twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from src.twitch.configuration.twitchChannelJoinHelper import TwitchChannelJoinHelper
from src.twitch.configuration.twitchChannelPointRedemptionHandler import TwitchChannelPointRedemptionHandler
from src.twitch.configuration.twitchConfiguration import TwitchConfiguration
from src.twitch.configuration.twitchIo.twitchIoConfiguration import TwitchIoConfiguration
from src.twitch.emotes.twitchEmotesHelper import TwitchEmotesHelper
from src.twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from src.twitch.followingStatus.twitchFollowingStatusRepository import TwitchFollowingStatusRepository
from src.twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from src.twitch.friends.twitchFriendsUserIdRepository import TwitchFriendsUserIdRepository
from src.twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from src.twitch.isLive.isLiveOnTwitchRepository import IsLiveOnTwitchRepository
from src.twitch.isLive.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from src.twitch.officialAccounts.officialTwitchAccountUserIdProvider import OfficialTwitchAccountUserIdProvider
from src.twitch.officialAccounts.officialTwitchAccountUserIdProviderInterface import \
    OfficialTwitchAccountUserIdProviderInterface
from src.twitch.timeout.timeoutImmuneUserIdsRepository import TimeoutImmuneUserIdsRepository
from src.twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from src.twitch.timeout.twitchTimeoutHelper import TwitchTimeoutHelper
from src.twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from src.twitch.timeout.twitchTimeoutRemodHelper import TwitchTimeoutRemodHelper
from src.twitch.timeout.twitchTimeoutRemodHelperInterface import TwitchTimeoutRemodHelperInterface
from src.twitch.timeout.twitchTimeoutRemodRepository import TwitchTimeoutRemodRepository
from src.twitch.timeout.twitchTimeoutRemodRepositoryInterface import TwitchTimeoutRemodRepositoryInterface
from src.twitch.tokens.twitchTokensRepository import TwitchTokensRepository
from src.twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from src.twitch.tokens.twitchTokensUtils import TwitchTokensUtils
from src.twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from src.twitch.twitchChannelJoinHelperInterface import TwitchChannelJoinHelperInterface
from src.twitch.twitchMessageStringUtils import TwitchMessageStringUtils
from src.twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from src.twitch.twitchPredictionWebsocketUtils import TwitchPredictionWebsocketUtils
from src.twitch.twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface
from src.twitch.twitchUtils import TwitchUtils
from src.twitch.twitchUtilsInterface import TwitchUtilsInterface
from src.twitch.websocket.connectionAction.twitchWebsocketConnectionActionHelper import \
    TwitchWebsocketConnectionActionHelper
from src.twitch.websocket.connectionAction.twitchWebsocketConnectionActionHelperInterface import \
    TwitchWebsocketConnectionActionHelperInterface
from src.twitch.websocket.endpointHelper.twitchWebsocketEndpointHelper import TwitchWebsocketEndpointHelper
from src.twitch.websocket.endpointHelper.twitchWebsocketEndpointHelperInterface import \
    TwitchWebsocketEndpointHelperInterface
from src.twitch.websocket.instabilityHelper.twitchWebsocketInstabilityHelper import TwitchWebsocketInstabilityHelper
from src.twitch.websocket.instabilityHelper.twitchWebsocketInstabilityHelperInterface import \
    TwitchWebsocketInstabilityHelperInterface
from src.twitch.websocket.sessionIdHelper.twitchWebsocketSessionIdHelper import TwitchWebsocketSessionIdHelper
from src.twitch.websocket.sessionIdHelper.twitchWebsocketSessionIdHelperInterface import \
    TwitchWebsocketSessionIdHelperInterface
from src.twitch.websocket.twitchWebsocketAllowedUsersRepository import TwitchWebsocketAllowedUsersRepository
from src.twitch.websocket.twitchWebsocketAllowedUsersRepositoryInterface import \
    TwitchWebsocketAllowedUsersRepositoryInterface
from src.twitch.websocket.twitchWebsocketClient import TwitchWebsocketClient
from src.twitch.websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from src.twitch.websocket.twitchWebsocketJsonMapper import TwitchWebsocketJsonMapper
from src.twitch.websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from src.users.addOrRemoveUserDataHelper import AddOrRemoveUserDataHelper
from src.users.addOrRemoveUserDataHelperInterface import AddOrRemoveUserDataHelperInterface
from src.users.chatSoundAlert.chatSoundAlertJsonParserInterface import ChatSoundAlertJsonParserInterface
from src.users.chatSoundAlert.stub.stubChatSoundAlertJsonParser import StubChatSoundAlertJsonParser
from src.users.crowdControl.crowdControlJsonParser import CrowdControlJsonParser
from src.users.crowdControl.crowdControlJsonParserInterface import CrowdControlJsonParserInterface
from src.users.cuteness.cutenessBoosterPackJsonParser import CutenessBoosterPackJsonParser
from src.users.cuteness.cutenessBoosterPackJsonParserInterface import CutenessBoosterPackJsonParserInterface
from src.users.decTalkSongs.decTalkSongBoosterPackParser import DecTalkSongBoosterPackParser
from src.users.decTalkSongs.decTalkSongBoosterPackParserInterface import DecTalkSongBoosterPackParserInterface
from src.users.pkmn.pkmnBoosterPackJsonParser import PkmnBoosterPackJsonParser
from src.users.pkmn.pkmnBoosterPackJsonParserInterface import PkmnBoosterPackJsonParserInterface
from src.users.soundAlert.soundAlertRedemptionJsonParserInterface import SoundAlertRedemptionJsonParserInterface
from src.users.soundAlert.stub.stubSoundAlertRedemptionJsonParser import StubSoundAlertRedemptionJsonParser
from src.users.timeout.timeoutBoosterPackJsonParser import TimeoutBoosterPackJsonParser
from src.users.timeout.timeoutBoosterPackJsonParserInterface import TimeoutBoosterPackJsonParserInterface
from src.users.tts.stub.stubTtsBoosterPackParser import StubTtsBoosterPackParser
from src.users.tts.stub.stubTtsChatterBoosterPackParser import StubTtsChatterBoosterPackParser
from src.users.tts.ttsBoosterPackParserInterface import TtsBoosterPackParserInterface
from src.users.ttsChatters.ttsChatterBoosterPackParserInterface import TtsChatterBoosterPackParserInterface
from src.users.userIdsRepository import UserIdsRepository
from src.users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from src.users.usersRepository import UsersRepository
from src.users.usersRepositoryInterface import UsersRepositoryInterface
from src.websocketConnection.stub.stubWebsocketConnectionServer import StubWebsocketConnectionServer
from src.websocketConnection.websocketConnectionServerInterface import WebsocketConnectionServerInterface

# Uncomment this chunk to turn on extra extra debug logging
# logging.basicConfig(
#     filename = 'generalLogging.log',
#     level = logging.DEBUG
# )


locale.setlocale(locale.LC_ALL, 'en_US.utf8')


#################################
## Core initialization section ##
#################################

eventLoop: AbstractEventLoop = asyncio.new_event_loop()
asyncio.set_event_loop(eventLoop)

backgroundTaskHelper: BackgroundTaskHelperInterface = BackgroundTaskHelper(
    eventLoop = eventLoop
)

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

timber: TimberInterface = Timber(
    backgroundTaskHelper = backgroundTaskHelper,
    timeZoneRepository = timeZoneRepository
)

networkJsonMapper: NetworkJsonMapperInterface = NetworkJsonMapper()
soundPlayerJsonMapper: SoundPlayerJsonMapperInterface = SoundPlayerJsonMapper()
storageJsonMapper: StorageJsonMapperInterface = StorageJsonMapper()

generalSettingsRepository = GeneralSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/generalSettingsRepository.json'),
    networkJsonMapper = networkJsonMapper,
    soundPlayerJsonMapper = soundPlayerJsonMapper,
    storageJsonMapper = storageJsonMapper
)

generalSettingsSnapshot = generalSettingsRepository.getAll()

backingDatabase: BackingDatabase
psqlCredentialsProvider: PsqlCredentialsProviderInterface | None = None

match generalSettingsSnapshot.requireDatabaseType():
    case DatabaseType.POSTGRESQL:
        psqlCredentialsProvider = PsqlCredentialsProvider(
            credentialsJsonReader = JsonFileReader('../config/psqlCredentials.json')
        )

        backingDatabase = BackingPsqlDatabase(
            eventLoop = eventLoop,
            psqlCredentialsProvider = psqlCredentialsProvider,
            timber = timber
        )

    case DatabaseType.SQLITE:
        backingDatabase = BackingSqliteDatabase(
            eventLoop = eventLoop
        )

    case _:
        raise RuntimeError(f'Unknown/misconfigured DatabaseType: \"{generalSettingsSnapshot.requireDatabaseType()}\"')

networkClientProvider: NetworkClientProvider
match generalSettingsSnapshot.requireNetworkClientType():
    case NetworkClientType.AIOHTTP:
        aioHttpCookieJarProvider = AioHttpCookieJarProvider(
            eventLoop = eventLoop
        )

        networkClientProvider = AioHttpClientProvider(
            eventLoop = eventLoop,
            cookieJarProvider = aioHttpCookieJarProvider,
            timber = timber
        )

    case NetworkClientType.REQUESTS:
        networkClientProvider = RequestsClientProvider(
            timber = timber
        )

    case _:
        raise RuntimeError(f'Unknown/misconfigured NetworkClientType: \"{generalSettingsSnapshot.requireNetworkClientType()}\"')

authRepository = AuthRepository(
    authJsonReader = JsonFileReader('../config/authRepository.json')
)

twitchJsonMapper: TwitchJsonMapperInterface = TwitchJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchWebsocketJsonMapper: TwitchWebsocketJsonMapperInterface = TwitchWebsocketJsonMapper(
    timber = timber,
    twitchJsonMapper = twitchJsonMapper
)

twitchApiService: TwitchApiServiceInterface = TwitchApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchCredentialsProvider = authRepository,
    twitchJsonMapper = twitchJsonMapper
)

officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface = OfficialTwitchAccountUserIdProvider()

userIdsRepository: UserIdsRepositoryInterface = UserIdsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchApiService = twitchApiService
)

twitchTokensRepository: TwitchTokensRepositoryInterface = TwitchTokensRepository(
    backgroundTaskHelper = backgroundTaskHelper,
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    userIdsRepository = userIdsRepository,
    seedFileReader = JsonFileReader('../config/twitchTokensRepositorySeedFile.json')
)

administratorProvider: AdministratorProviderInterface = AdministratorProvider(
    generalSettingsRepository = generalSettingsRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

bannedWordsRepository: BannedWordsRepositoryInterface = BannedWordsRepository(
    bannedWordsLinesReader = LinesFileReader('bannedWords.txt'),
    timber = timber
)

contentScanner: ContentScannerInterface = ContentScanner(
    bannedWordsRepository = bannedWordsRepository,
    timber = timber
)

twitchTokensUtils: TwitchTokensUtilsInterface = TwitchTokensUtils(
    administratorProvider = administratorProvider,
    twitchTokensRepository = twitchTokensRepository
)

twitchEmotesHelper: TwitchEmotesHelperInterface = TwitchEmotesHelper(
    timber = timber,
    twitchApiService = twitchApiService,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface = TwitchFollowingStatusRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    twitchApiService = twitchApiService,
    userIdsRepository = userIdsRepository
)

chatSoundAlertJsonParser: ChatSoundAlertJsonParserInterface = StubChatSoundAlertJsonParser()

crowdControlJsonParser: CrowdControlJsonParserInterface = CrowdControlJsonParser()

cutenessBoosterPackJsonParser: CutenessBoosterPackJsonParserInterface = CutenessBoosterPackJsonParser()

decTalkSongBoosterPackParser: DecTalkSongBoosterPackParserInterface = DecTalkSongBoosterPackParser()

languageEntryJsonMapper: LanguageEntryJsonMapperInterface = LanguageEntryJsonMapper()

pkmnBoosterPackJsonParser: PkmnBoosterPackJsonParserInterface = PkmnBoosterPackJsonParser(
    timber = timber
)

soundAlertRedemptionJsonParser: SoundAlertRedemptionJsonParserInterface = StubSoundAlertRedemptionJsonParser()

timeoutBoosterPackJsonParser: TimeoutBoosterPackJsonParserInterface = TimeoutBoosterPackJsonParser()

ttsJsonMapper: TtsJsonMapperInterface = TtsJsonMapper(
    timber = timber
)

ttsBoosterPackParser: TtsBoosterPackParserInterface = StubTtsBoosterPackParser()

ttsChatterBoosterPackParser: TtsChatterBoosterPackParserInterface = StubTtsChatterBoosterPackParser()

usersRepository: UsersRepositoryInterface = UsersRepository(
    chatSoundAlertJsonParser = chatSoundAlertJsonParser,
    crowdControlJsonParser = crowdControlJsonParser,
    cutenessBoosterPackJsonParser = cutenessBoosterPackJsonParser,
    decTalkSongBoosterPackParser = decTalkSongBoosterPackParser,
    languageEntryJsonMapper = languageEntryJsonMapper,
    pkmnBoosterPackJsonParser = pkmnBoosterPackJsonParser,
    soundAlertRedemptionJsonParser = soundAlertRedemptionJsonParser,
    timber = timber,
    timeoutBoosterPackJsonParser = timeoutBoosterPackJsonParser,
    timeZoneRepository = timeZoneRepository,
    ttsBoosterPackParser = ttsBoosterPackParser,
    ttsChatterBoosterPackParser = ttsChatterBoosterPackParser,
    ttsJsonMapper = ttsJsonMapper
)

twitchChannelJoinHelper: TwitchChannelJoinHelperInterface = TwitchChannelJoinHelper(
    backgroundTaskHelper = backgroundTaskHelper,
    verified = True,
    timber = timber,
    usersRepository = usersRepository
)

twitchPredictionWebsocketUtils: TwitchPredictionWebsocketUtilsInterface = TwitchPredictionWebsocketUtils()

addOrRemoveUserDataHelper: AddOrRemoveUserDataHelperInterface = AddOrRemoveUserDataHelper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

chatLogger: ChatLoggerInterface = ChatLogger(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

activeChattersRepository: ActiveChattersRepositoryInterface = ActiveChattersRepository(
    timeZoneRepository = timeZoneRepository
)


#####################################
## CynanBot initialization section ##
#####################################

cynanBotUserIdsProvider: CynanBotUserIdsProviderInterface = CynanBotUserIdsProvider()

twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface = TwitchFriendsUserIdRepository()


#####################################
## Nightbot initialization section ##
#####################################

nightbotUserIdProvider: NightbotUserIdProviderInterface = NightbotUserIdProvider()


###################################
## Tangia initialization section ##
###################################

tangiaBotUserIdProvider: TangiaBotUserIdProviderInterface = TangiaBotUserIdProvider()


####################################
## Funtoon initialization section ##
####################################

funtoonUserIdProvider: FuntoonUserIdProviderInterface = FuntoonUserIdProvider()

funtoonTokensRepository: FuntoonTokensRepositoryInterface = FuntoonTokensRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    userIdsRepository = userIdsRepository,
    seedFileReader = JsonFileReader('../config/funtoonTokensRepositorySeedFile.json')
)

funtoonJsonMapper: FuntoonJsonMapperInterface = FuntoonJsonMapper()

funtoonApiService: FuntoonApiServiceInterface = FuntoonApiService(
    funtoonJsonMapper = funtoonJsonMapper,
    networkClientProvider = networkClientProvider,
    timber = timber
)

funtoonHelper: FuntoonHelperInterface = FuntoonHelper(
    funtoonApiService = funtoonApiService,
    funtoonJsonMapper = funtoonJsonMapper,
    funtoonTokensRepository = funtoonTokensRepository,
    timber = timber
)

emojiRepository: EmojiRepositoryInterface = EmojiRepository(
    emojiJsonReader = JsonFileReader('emojiRepository.json'),
    timber = timber
)

emojiHelper: EmojiHelperInterface = EmojiHelper(
    emojiRepository = emojiRepository
)

isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = IsLiveOnTwitchRepository(
    administratorProvider = administratorProvider,
    timber = timber,
    twitchApiService = twitchApiService,
    twitchTokensRepository = twitchTokensRepository
)

twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface = StubTwitchChannelEditorsRepository()

languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

locationsRepository: LocationsRepositoryInterface = LocationsRepository(
    locationsJsonReader = JsonFileReader('locationsRepository.json'),
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

mostRecentChatsRepository: MostRecentChatsRepositoryInterface = MostRecentChatsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchConfiguration: TwitchConfiguration = TwitchIoConfiguration(
    userIdsRepository = userIdsRepository
)

sentMessageLogger: SentMessageLoggerInterface = SentMessageLogger(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchTimeoutRemodRepository: TwitchTimeoutRemodRepositoryInterface = TwitchTimeoutRemodRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface = TwitchTimeoutRemodHelper(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    twitchTimeoutRemodRepository = twitchTimeoutRemodRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

twitchMessageStringUtils: TwitchMessageStringUtilsInterface = TwitchMessageStringUtils()

twitchUtils: TwitchUtilsInterface = TwitchUtils(
    backgroundTaskHelper = backgroundTaskHelper,
    generalSettingsRepository = generalSettingsRepository,
    sentMessageLogger = sentMessageLogger,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)

puptimeUserIdProvider: PuptimeUserIdProviderInterface = PuptimeUserIdProvider()

seryBotUserIdProvider: SeryBotUserIdProviderInterface = SeryBotUserIdProvider()

streamElementsUserIdProvider: StreamElementsUserIdProviderInterface = StreamElementsUserIdProvider()

streamLabsUserIdProvider: StreamLabsUserIdProviderInterface = StreamLabsUserIdProvider()

timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface = TimeoutImmuneUserIdsRepository(
    cynanBotUserIdsProvider = cynanBotUserIdsProvider,
    funtoonUserIdProvider = funtoonUserIdProvider,
    nightbotUserIdProvider = nightbotUserIdProvider,
    officialTwitchAccountUserIdProvider = officialTwitchAccountUserIdProvider,
    puptimeUserIdProvider = puptimeUserIdProvider,
    seryBotUserIdProvider = seryBotUserIdProvider,
    streamElementsUserIdProvider = streamElementsUserIdProvider,
    streamLabsUserIdProvider = streamLabsUserIdProvider,
    tangiaBotUserIdProvider = tangiaBotUserIdProvider,
    twitchFriendsUserIdProvider = twitchFriendsUserIdRepository,
    twitchHandleProvider = authRepository,
    userIdsRepository = userIdsRepository
)

twitchTimeoutHelper: TwitchTimeoutHelperInterface = TwitchTimeoutHelper(
    timber = timber,
    timeoutImmuneUserIdsRepository = timeoutImmuneUserIdsRepository,
    twitchApiService = twitchApiService,
    twitchConstants = twitchUtils,
    twitchHandleProvider = authRepository,
    twitchTimeoutRemodHelper = twitchTimeoutRemodHelper,
    userIdsRepository = userIdsRepository
)

googleApiAccessTokenStorage: GoogleApiAccessTokenStorageInterface = GoogleApiAccessTokenStorage(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
)

googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
)

googleJwtBuilder: GoogleJwtBuilderInterface = GoogleJwtBuilder(
    googleCloudCredentialsProvider = authRepository,
    googleJsonMapper = googleJsonMapper,
    timeZoneRepository = timeZoneRepository,
)

googleApiService: GoogleApiServiceInterface = GoogleApiService(
    googleApiAccessTokenStorage = googleApiAccessTokenStorage,
    googleCloudProjectCredentialsProvider = authRepository,
    googleJsonMapper = googleJsonMapper,
    googleJwtBuilder = googleJwtBuilder,
    networkClientProvider = networkClientProvider,
    timber = timber
)

twitchWebsocketAllowedUsersRepository: TwitchWebsocketAllowedUsersRepositoryInterface = TwitchWebsocketAllowedUsersRepository(
    timber = timber,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)

twitchWebsocketInstabilityHelper: TwitchWebsocketInstabilityHelperInterface = TwitchWebsocketInstabilityHelper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

twitchWebsocketEndpointHelper: TwitchWebsocketEndpointHelperInterface = TwitchWebsocketEndpointHelper(
    timber = timber
)

twitchWebsocketSessionIdHelper: TwitchWebsocketSessionIdHelperInterface = TwitchWebsocketSessionIdHelper(
    timber = timber
)

twitchWebsocketConnectionActionHelper: TwitchWebsocketConnectionActionHelperInterface = TwitchWebsocketConnectionActionHelper(
    timber = timber,
    twitchWebsocketEndpointHelper = twitchWebsocketEndpointHelper,
    twitchWebsocketSessionIdHelper = twitchWebsocketSessionIdHelper
)

twitchWebsocketClient: TwitchWebsocketClientInterface | None = None
if generalSettingsSnapshot.isEventSubEnabled():
    twitchWebsocketClient = TwitchWebsocketClient(
        backgroundTaskHelper = backgroundTaskHelper,
        timber = timber,
        timeZoneRepository = timeZoneRepository,
        twitchApiService = twitchApiService,
        twitchTokensRepository = twitchTokensRepository,
        twitchWebsocketAllowedUsersRepository = twitchWebsocketAllowedUsersRepository,
        twitchWebsocketConnectionActionHelper = twitchWebsocketConnectionActionHelper,
        twitchWebsocketEndpointHelper = twitchWebsocketEndpointHelper,
        twitchWebsocketInstabilityHelper = twitchWebsocketInstabilityHelper,
        twitchWebsocketJsonMapper = twitchWebsocketJsonMapper,
        twitchWebsocketSessionIdHelper = twitchWebsocketSessionIdHelper
    )


#################################
## Bean initialization section ##
#################################

beanStatsPresenter: BeanStatsPresenterInterface = BeanStatsPresenter()

beanStatsRepository: BeanStatsRepositoryInterface = BeanStatsRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    userIdsRepository = userIdsRepository
)


######################################
## Chat Band initialization section ##
######################################

chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface = ChatBandInstrumentSoundsRepository(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber
)


#########################################
## Sound Player initialization section ##
#########################################

soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = SoundPlayerSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/soundPlayerSettingsRepository.json')
)

soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface | None = SoundPlayerRandomizerHelper(
    eventLoop = eventLoop,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber
)

soundPlayerManagerProvider: SoundPlayerManagerProviderInterface

match generalSettingsSnapshot.requireSoundPlayerType():
    case SoundPlayerType.AUDIO_PLAYER:
        soundPlayerManagerProvider = AudioPlayerSoundPlayerManagerProvider(
            backgroundTaskHelper = backgroundTaskHelper,
            chatBandInstrumentSoundsRepository = chatBandInstrumentSoundsRepository,
            soundPlayerSettingsRepository = soundPlayerSettingsRepository,
            timber = timber
        )

    case SoundPlayerType.STUB:
        soundPlayerManagerProvider = StubSoundPlayerManagerProvider()

    case SoundPlayerType.VLC:
        soundPlayerManagerProvider = VlcSoundPlayerManagerProvider(
            chatBandInstrumentSoundsRepository = chatBandInstrumentSoundsRepository,
            soundPlayerSettingsRepository = soundPlayerSettingsRepository,
            timber = timber
        )

    case _:
        raise RuntimeError(f'Unknown/misconfigured SoundPlayerType: \"{generalSettingsSnapshot.requireSoundPlayerType()}\"')


################################
## TTS initialization section ##
################################

compositeTtsManager: CompositeTtsManagerInterface = StubCompositeTtsManager()


##################################################
## Stream Alerts Manager initialization section ##
##################################################

streamAlertsManager: StreamAlertsManagerInterface = StubStreamAlertsManager()


##########################################
## Cheer Actions initialization section ##
##########################################

cheerActionJsonMapper: CheerActionJsonMapperInterface = CheerActionJsonMapper(
    timber = timber
)

cheerActionSettingsRepository: CheerActionSettingsRepositoryInterface = CheerActionSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/cheerActionSettings.json')
)

cheerActionsRepository: CheerActionsRepositoryInterface = CheerActionsRepository(
    backingDatabase = backingDatabase,
    cheerActionJsonMapper = cheerActionJsonMapper,
    cheerActionSettingsRepository = cheerActionSettingsRepository,
    timber = timber
)

soundAlertCheerActionHelper: SoundAlertCheerActionHelperInterface | None = SoundAlertCheerActionHelper(
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    soundPlayerManagerProvider = soundPlayerManagerProvider,
    soundPlayerRandomizerHelper = soundPlayerRandomizerHelper,
    timber = timber
)

cheerActionHelper: CheerActionHelperInterface = CheerActionHelper(
    beanChanceCheerActionHelper = None,
    cheerActionsRepository = cheerActionsRepository,
    crowdControlCheerActionHelper = None,
    soundAlertCheerActionHelper = soundAlertCheerActionHelper,
    timeoutCheerActionHelper = None,
    tntCheerActionHelper = None,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)


#########################################
## Chat Actions initialization section ##
#########################################

cheerActionsWizard: CheerActionsWizardInterface = CheerActionsWizard(
    timber = timber
)

cheerActionsWizardChatAction = CheerActionsWizardChatAction(
    cheerActionJsonMapper = cheerActionJsonMapper,
    cheerActionsRepository = cheerActionsRepository,
    cheerActionsWizard = cheerActionsWizard,
    timber = timber,
    twitchUtils = twitchUtils
)

persistAllUsersChatAction = PersistAllUsersChatAction(
    generalSettingsRepository = generalSettingsRepository,
    userIdsRepository = userIdsRepository
)

chatActionsManager: ChatActionsManagerInterface = ChatActionsManager(
    activeChattersRepository = activeChattersRepository,
    anivCheckChatAction = None,
    chatBackMessagesChatAction = None,
    chatLoggerChatAction = None,
    cheerActionsWizardChatAction = cheerActionsWizardChatAction,
    generalSettingsRepository = generalSettingsRepository,
    mostRecentAnivMessageTimeoutHelper = None,
    mostRecentChatsRepository = mostRecentChatsRepository,
    persistAllUsersChatAction = persistAllUsersChatAction,
    recurringActionsWizardChatAction = None,
    saveMostRecentAnivMessageChatAction = None,
    soundAlertChatAction = None,
    supStreamerChatAction = None,
    ttsChattersChatAction = None,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)


######################################################
## Channel Point Redemptions initialization section ##
######################################################

if soundPlayerManagerProvider is None or soundPlayerRandomizerHelper is None or streamAlertsManager is None:
    soundAlertPointRedemption: SoundAlertPointRedemption | None = None
else:
    soundAlertPointRedemption: SoundAlertPointRedemption | None = SoundAlertPointRedemption(
        soundPlayerManagerProvider = soundPlayerManagerProvider,
        soundPlayerRandomizerHelper = soundPlayerRandomizerHelper,
        streamAlertsManager = streamAlertsManager
    )

twitchChannelPointRedemptionHandler: AbsTwitchChannelPointRedemptionHandler | None = TwitchChannelPointRedemptionHandler(
    casualGamePollPointRedemption = None,
    cutenessPointRedemption = None,
    decTalkSongPointRedemption = None,
    pkmnBattlePointRedemption = None,
    pkmnCatchPointRedemption = None,
    pkmnEvolvePointRedemption = None,
    pkmnShinyPointRedemption = None,
    shizaPointRedemption = None,
    soundAlertPointRedemption = soundAlertPointRedemption,
    superTriviaGamePointRedemption = None,
    timeoutPointRedemption = None,
    triviaGamePointRedemption = None,
    timber = timber,
    userIdsRepository = userIdsRepository
)


########################################################
## Websocket Connection Server initialization section ##
########################################################

websocketConnectionServer: WebsocketConnectionServerInterface = StubWebsocketConnectionServer()


#####################################
## CynanBot initialization section ##
#####################################

cynanBot = CynanBot(
    eventLoop = eventLoop,
    twitchChannelPointRedemptionHandler = twitchChannelPointRedemptionHandler,
    twitchCheerHandler = None,
    twitchFollowHandler = None,
    twitchPollHandler = None,
    twitchPredictionHandler = None,
    twitchRaidHandler = None,
    twitchSubscriptionHandler = None,
    activeChattersRepository = activeChattersRepository,
    additionalTriviaAnswersRepository = None,
    addOrRemoveUserDataHelper = addOrRemoveUserDataHelper,
    administratorProvider = administratorProvider,
    anivCopyMessageTimeoutScorePresenter = None,
    anivCopyMessageTimeoutScoreRepository = None,
    anivSettingsRepository = None,
    authRepository = authRepository,
    backgroundTaskHelper = backgroundTaskHelper,
    bannedTriviaGameControllersRepository = None,
    bannedWordsRepository = None,
    beanChanceCheerActionHelper = None,
    beanStatsPresenter = None,
    beanStatsRepository = None,
    bizhawkSettingsRepository = None,
    chatActionsManager = chatActionsManager,
    chatLogger = chatLogger,
    cheerActionHelper = None,
    cheerActionJsonMapper = None,
    cheerActionSettingsRepository = None,
    cheerActionsRepository = None,
    cheerActionsWizard = None,
    compositeTtsManager = compositeTtsManager,
    crowdControlActionHandler = None,
    crowdControlAutomator = None,
    crowdControlIdGenerator = None,
    crowdControlMachine = None,
    crowdControlMessageHandler = None,
    crowdControlSettingsRepository = None,
    crowdControlUserInputUtils = None,
    cutenessPresenter = None,
    cutenessRepository = None,
    cutenessUtils = None,
    funtoonHelper = None,
    funtoonTokensRepository = None,
    generalSettingsRepository = generalSettingsRepository,
    halfLifeService = None,
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    jishoHelper = None,
    languagesRepository = languagesRepository,
    locationsRepository = locationsRepository,
    mostRecentAnivMessageRepository = None,
    mostRecentAnivMessageTimeoutHelper = None,
    mostRecentChatsRepository = mostRecentChatsRepository,
    openTriviaDatabaseSessionTokenRepository = None,
    pokepediaRepository = None,
    psqlCredentialsProvider = psqlCredentialsProvider,
    recurringActionsEventHandler = None,
    recurringActionsHelper = None,
    recurringActionsMachine = None,
    recurringActionsRepository = None,
    recurringActionsWizard = None,
    sentMessageLogger = sentMessageLogger,
    shinyTriviaOccurencesRepository = None,
    soundPlayerManagerProvider = soundPlayerManagerProvider,
    soundPlayerRandomizerHelper = soundPlayerRandomizerHelper,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    starWarsQuotesRepository = None,
    streamAlertsManager = streamAlertsManager,
    streamAlertsSettingsRepository = None,
    streamElementsSettingsRepository = None,
    streamElementsUserKeyRepository = None,
    supStreamerRepository = None,
    timber = timber,
    timeoutActionHelper = None,
    timeoutActionHistoryRepository = None,
    timeoutActionSettingsRepository = None,
    timeZoneRepository = timeZoneRepository,
    toxicTriviaOccurencesRepository = None,
    translationHelper = None,
    triviaBanHelper = None,
    triviaEmoteGenerator = None,
    triviaEventHandler = None,
    triviaGameBuilder = None,
    triviaGameControllersRepository = None,
    triviaGameGlobalControllersRepository = None,
    triviaGameMachine = None,
    triviaHistoryRepository = None,
    triviaIdGenerator = None,
    triviaRepository = None,
    triviaScoreRepository = None,
    triviaSettingsRepository = None,
    triviaTwitchEmoteHelper = None,
    triviaUtils = None,
    trollmojiHelper = None,
    trollmojiSettingsRepository = None,
    ttsJsonMapper = None,
    ttsMonsterApiTokensRepository = None,
    ttsMonsterKeyAndUserIdRepository = None,
    ttsMonsterTtsManager = None,
    ttsMonsterSettingsRepository = None,
    ttsMonsterStreamerVoicesRepository = None,
    ttsSettingsRepository = None,
    twitchApiService = twitchApiService,
    twitchChannelEditorsRepository = twitchChannelEditorsRepository,
    twitchChannelJoinHelper = twitchChannelJoinHelper,
    twitchConfiguration = twitchConfiguration,
    twitchEmotesHelper = twitchEmotesHelper,
    twitchFollowingStatusRepository = None,
    twitchFriendsUserIdRepository = twitchFriendsUserIdRepository,
    twitchMessageStringUtils = twitchMessageStringUtils,
    twitchPredictionWebsocketUtils = None,
    twitchTimeoutHelper = twitchTimeoutHelper,
    twitchTimeoutRemodHelper = twitchTimeoutRemodHelper,
    twitchTokensRepository = twitchTokensRepository,
    twitchTokensUtils = twitchTokensUtils,
    twitchUtils = twitchUtils,
    twitchWebsocketClient = twitchWebsocketClient,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository,
    weatherReportPresenter = None,
    weatherRepository = None,
    websocketConnectionServer = websocketConnectionServer,
    wordOfTheDayPresenter = None,
    wordOfTheDayRepository = None
)


#########################################
## Section for starting the actual bot ##
#########################################

timber.log('initCynanBot', 'Starting CynanBot...')
cynanBot.run()
