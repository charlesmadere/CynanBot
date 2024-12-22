import asyncio
import locale
from asyncio import AbstractEventLoop

from src.aniv.anivContentScanner import AnivContentScanner
from src.aniv.anivContentScannerInterface import AnivContentScannerInterface
from src.aniv.anivCopyMessageTimeoutScorePresenter import AnivCopyMessageTimeoutScorePresenter
from src.aniv.anivCopyMessageTimeoutScorePresenterInterface import AnivCopyMessageTimeoutScorePresenterInterface
from src.aniv.anivCopyMessageTimeoutScoreRepository import AnivCopyMessageTimeoutScoreRepository
from src.aniv.anivCopyMessageTimeoutScoreRepositoryInterface import AnivCopyMessageTimeoutScoreRepositoryInterface
from src.aniv.anivSettingsRepository import AnivSettingsRepository
from src.aniv.anivSettingsRepositoryInterface import AnivSettingsRepositoryInterface
from src.aniv.anivUserIdProvider import AnivUserIdProvider
from src.aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface
from src.aniv.mostRecentAnivMessageRepository import MostRecentAnivMessageRepository
from src.aniv.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from src.aniv.mostRecentAnivMessageTimeoutHelper import MostRecentAnivMessageTimeoutHelper
from src.aniv.mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from src.beanStats.beanStatsPresenter import BeanStatsPresenter
from src.beanStats.beanStatsPresenterInterface import BeanStatsPresenterInterface
from src.beanStats.beanStatsRepository import BeanStatsRepository
from src.beanStats.beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from src.chatActions.chatActionsManager import ChatActionsManager
from src.chatActions.chatActionsManagerInterface import ChatActionsManagerInterface
from src.chatActions.cheerActionsWizardChatAction import CheerActionsWizardChatAction
from src.chatActions.persistAllUsersChatAction import PersistAllUsersChatAction
from src.chatActions.saveMostRecentAnivMessageChatAction import SaveMostRecentAnivMessageChatAction
from src.chatActions.supStreamerChatAction import SupStreamerChatAction
from src.chatActions.ttsChattersChatAction import TtsChattersChatAction
from src.chatBand.chatBandInstrumentSoundsRepositoryInterface import ChatBandInstrumentSoundsRepositoryInterface
from src.chatLogger.chatLogger import ChatLogger
from src.chatLogger.chatLoggerInterface import ChatLoggerInterface
from src.cheerActions.beanChance.beanChanceCheerActionHelper import BeanChanceCheerActionHelper
from src.cheerActions.beanChance.beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
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
from src.cheerActions.crowdControl.crowdControlCheerActionHelper import CrowdControlCheerActionHelper
from src.cheerActions.crowdControl.crowdControlCheerActionHelperInterface import CrowdControlCheerActionHelperInterface
from src.cheerActions.soundAlert.soundAlertCheerActionHelper import SoundAlertCheerActionHelper
from src.cheerActions.soundAlert.soundAlertCheerActionHelperInterface import SoundAlertCheerActionHelperInterface
from src.cheerActions.timeout.timeoutCheerActionHelper import TimeoutCheerActionHelper
from src.cheerActions.timeout.timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from src.cheerActions.timeout.timeoutCheerActionMapper import TimeoutCheerActionMapper
from src.contentScanner.bannedWordsRepository import BannedWordsRepository
from src.contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from src.contentScanner.contentScanner import ContentScanner
from src.contentScanner.contentScannerInterface import ContentScannerInterface
from src.crowdControl.automator.crowdControlAutomator import CrowdControlAutomator
from src.crowdControl.automator.crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from src.crowdControl.bizhawk.bizhawkActionHandler import BizhawkActionHandler
from src.crowdControl.bizhawk.bizhawkKeyMapper import BizhawkKeyMapper
from src.crowdControl.bizhawk.bizhawkKeyMapperInterface import BizhawkKeyMapperInterface
from src.crowdControl.bizhawk.bizhawkSettingsRepository import BizhawkSettingsRepository
from src.crowdControl.bizhawk.bizhawkSettingsRepositoryInterface import BizhawkSettingsRepositoryInterface
from src.crowdControl.crowdControlActionHandler import CrowdControlActionHandler
from src.crowdControl.crowdControlMachine import CrowdControlMachine
from src.crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from src.crowdControl.crowdControlSettingsRepository import CrowdControlSettingsRepository
from src.crowdControl.crowdControlSettingsRepositoryInterface import CrowdControlSettingsRepositoryInterface
from src.crowdControl.idGenerator.crowdControlIdGenerator import CrowdControlIdGenerator
from src.crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from src.crowdControl.message.crowdControlMessageHandler import CrowdControlMessageHandler
from src.crowdControl.message.crowdControlMessagePresenter import CrowdControlMessagePresenter
from src.crowdControl.message.crowdControlMessagePresenterInterface import CrowdControlMessagePresenterInterface
from src.crowdControl.utils.crowdControlUserInputUtils import CrowdControlUserInputUtils
from src.crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from src.cynanBot import CynanBot
from src.decTalk.apiService.decTalkApiService import DecTalkApiService
from src.decTalk.apiService.decTalkApiServiceInterface import DecTalkApiServiceInterface
from src.decTalk.decTalkMessageCleaner import DecTalkMessageCleaner
from src.decTalk.decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from src.decTalk.decTalkVoiceChooser import DecTalkVoiceChooser
from src.decTalk.decTalkVoiceChooserInterface import DecTalkVoiceChooserInterface
from src.decTalk.decTalkVoiceMapper import DecTalkVoiceMapper
from src.decTalk.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from src.decTalk.helper.decTalkHelper import DecTalkHelper
from src.decTalk.helper.decTalkHelperInterface import DecTalkHelperInterface
from src.decTalk.settings.decTalkSettingsRepository import DecTalkSettingsRepository
from src.decTalk.settings.decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
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
from src.google.settings.googleSettingsRepository import GoogleSettingsRepository
from src.google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from src.halfLife.halfLifeMessageCleaner import HalfLifeMessageCleaner
from src.halfLife.halfLifeMessageCleanerInterface import HalfLifeMessageCleanerInterface
from src.halfLife.helper.halfLifeHelper import HalfLifeHelper
from src.halfLife.helper.halfLifeHelperInterface import HalfLifeHelperInterface
from src.halfLife.parser.halfLifeJsonParser import HalfLifeJsonParser
from src.halfLife.parser.halfLifeJsonParserInterface import HalfLifeJsonParserInterface
from src.halfLife.parser.halfLifeMessageVoiceParser import HalfLifeMessageVoiceParser
from src.halfLife.parser.halfLifeMessageVoiceParserInterface import HalfLifeMessageVoiceParserInterface
from src.halfLife.service.halfLifeService import HalfLifeService
from src.halfLife.service.halfLifeServiceInterface import HalfLifeServiceInterface
from src.halfLife.settings.halfLifeSettingsRepository import HalfLifeSettingsRepository
from src.halfLife.settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from src.language.jsonMapper.languageEntryJsonMapper import LanguageEntryJsonMapper
from src.language.jsonMapper.languageEntryJsonMapperInterface import LanguageEntryJsonMapperInterface
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.location.locationsRepository import LocationsRepository
from src.location.locationsRepositoryInterface import LocationsRepositoryInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.microsoftSam.apiService.microsoftSamApiService import MicrosoftSamApiService
from src.microsoftSam.apiService.microsoftSamApiServiceInterface import MicrosoftSamApiServiceInterface
from src.microsoftSam.helper.microsoftSamHelper import MicrosoftSamHelper
from src.microsoftSam.helper.microsoftSamHelperInterface import MicrosoftSamHelperInterface
from src.microsoftSam.microsoftSamJsonParser import MicrosoftSamJsonParser
from src.microsoftSam.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from src.microsoftSam.microsoftSamMessageCleaner import MicrosoftSamMessageCleaner
from src.microsoftSam.microsoftSamMessageCleanerInterface import MicrosoftSamMessageCleanerInterface
from src.microsoftSam.microsoftSamVoiceMapper import MicrosoftSamVoiceMapper
from src.microsoftSam.microsoftSamVoiceMapperInterface import MicrosoftSamVoiceMapperInterface
from src.microsoftSam.parser.microsoftSamMessageVoiceParser import MicrosoftSamMessageVoiceParser
from src.microsoftSam.parser.microsoftSamMessageVoiceParserInterface import MicrosoftSamMessageVoiceParserInterface
from src.microsoftSam.settings.microsoftSamSettingsRepository import MicrosoftSamSettingsRepository
from src.microsoftSam.settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
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
from src.soundPlayerManager.soundAlertJsonMapper import SoundAlertJsonMapper
from src.soundPlayerManager.soundAlertJsonMapperInterface import SoundAlertJsonMapperInterface
from src.soundPlayerManager.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from src.soundPlayerManager.soundPlayerRandomizerHelper import SoundPlayerRandomizerHelper
from src.soundPlayerManager.soundPlayerRandomizerHelperInterface import SoundPlayerRandomizerHelperInterface
from src.soundPlayerManager.soundPlayerSettingsRepository import SoundPlayerSettingsRepository
from src.soundPlayerManager.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
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
from src.storage.tempFileHelper import TempFileHelper
from src.storage.tempFileHelperInterface import TempFileHelperInterface
from src.streamAlertsManager.streamAlertsManager import StreamAlertsManager
from src.streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from src.streamAlertsManager.streamAlertsSettingsRepository import StreamAlertsSettingsRepository
from src.streamAlertsManager.streamAlertsSettingsRepositoryInterface import StreamAlertsSettingsRepositoryInterface
from src.streamElements.apiService.streamElementsApiService import StreamElementsApiService
from src.streamElements.apiService.streamElementsApiServiceInterface import StreamElementsApiServiceInterface
from src.streamElements.helper.streamElementsHelper import StreamElementsHelper
from src.streamElements.helper.streamElementsHelperInterface import StreamElementsHelperInterface
from src.streamElements.parser.streamElementsJsonParser import StreamElementsJsonParser
from src.streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from src.streamElements.parser.streamElementsMessageVoiceParser import StreamElementsMessageVoiceParser
from src.streamElements.parser.streamElementsMessageVoiceParserInterface import \
    StreamElementsMessageVoiceParserInterface
from src.streamElements.settings.streamElementsSettingsRepository import StreamElementsSettingsRepository
from src.streamElements.settings.streamElementsSettingsRepositoryInterface import \
    StreamElementsSettingsRepositoryInterface
from src.streamElements.streamElementsMessageCleaner import StreamElementsMessageCleaner
from src.streamElements.streamElementsMessageCleanerInterface import StreamElementsMessageCleanerInterface
from src.streamElements.streamElementsUserIdProvider import StreamElementsUserIdProvider
from src.streamElements.streamElementsUserIdProviderInterface import StreamElementsUserIdProviderInterface
from src.streamElements.userKeyRepository.streamElementsUserKeyRepository import StreamElementsUserKeyRepository
from src.streamElements.userKeyRepository.streamElementsUserKeyRepositoryInterface import \
    StreamElementsUserKeyRepositoryInterface
from src.streamLabs.streamLabsUserIdProvider import StreamLabsUserIdProvider
from src.streamLabs.streamLabsUserIdProviderInterface import StreamLabsUserIdProviderInterface
from src.supStreamer.supStreamerHelper import SupStreamerHelper
from src.supStreamer.supStreamerHelperInterface import SupStreamerHelperInterface
from src.supStreamer.supStreamerRepository import SupStreamerRepository
from src.supStreamer.supStreamerRepositoryInterface import SupStreamerRepositoryInterface
from src.tangia.tangiaBotUserIdProvider import TangiaBotUserIdProvider
from src.tangia.tangiaBotUserIdProviderInterface import TangiaBotUserIdProviderInterface
from src.timber.timber import Timber
from src.timber.timberInterface import TimberInterface
from src.timeout.guaranteedTimeoutUsersRepository import GuaranteedTimeoutUsersRepository
from src.timeout.guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from src.timeout.timeoutActionHelper import TimeoutActionHelper
from src.timeout.timeoutActionHelperInterface import TimeoutActionHelperInterface
from src.timeout.timeoutActionHistoryRepository import TimeoutActionHistoryRepository
from src.timeout.timeoutActionHistoryRepositoryInterface import TimeoutActionHistoryRepositoryInterface
from src.timeout.timeoutActionJsonMapper import TimeoutActionJsonMapper
from src.timeout.timeoutActionJsonMapperInterface import TimeoutActionJsonMapperInterface
from src.timeout.timeoutActionSettingsRepository import TimeoutActionSettingsRepository
from src.timeout.timeoutActionSettingsRepositoryInterface import TimeoutActionSettingsRepositoryInterface
from src.trollmoji.trollmojiHelper import TrollmojiHelper
from src.trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from src.trollmoji.trollmojiSettingsRepository import TrollmojiSettingsRepository
from src.trollmoji.trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from src.tts.compositeTtsManager import CompositeTtsManager
from src.tts.compositeTtsManagerInterface import CompositeTtsManagerInterface
from src.tts.decTalk.decTalkFileManager import DecTalkFileManager
from src.tts.decTalk.decTalkFileManagerInterface import DecTalkFileManagerInterface
from src.tts.decTalk.decTalkTtsManager import DecTalkTtsManager
from src.tts.decTalk.decTalkTtsManagerInterface import DecTalkTtsManagerInterface
from src.tts.decTalk.singingDecTalkTtsManager import SingingDecTalkTtsManager
from src.tts.google.googleFileExtensionHelper import GoogleFileExtensionHelper
from src.tts.google.googleFileExtensionHelperInterface import GoogleFileExtensionHelperInterface
from src.tts.google.googleTtsFileManager import GoogleTtsFileManager
from src.tts.google.googleTtsFileManagerInterface import GoogleTtsFileManagerInterface
from src.tts.google.googleTtsHelper import GoogleTtsHelper
from src.tts.google.googleTtsHelperInterface import GoogleTtsHelperInterface
from src.tts.google.googleTtsManager import GoogleTtsManager
from src.tts.google.googleTtsManagerInterface import GoogleTtsManagerInterface
from src.tts.google.googleTtsMessageCleaner import GoogleTtsMessageCleaner
from src.tts.google.googleTtsMessageCleanerInterface import GoogleTtsMessageCleanerInterface
from src.tts.google.googleTtsVoiceChooser import GoogleTtsVoiceChooser
from src.tts.google.googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface
from src.tts.halfLife.halfLifeTtsManager import HalfLifeTtsManager
from src.tts.halfLife.halfLifeTtsManagerInterface import HalfLifeTtsManagerInterface
from src.tts.microsoftSam.microsoftSamFileManager import MicrosoftSamFileManager
from src.tts.microsoftSam.microsoftSamFileManagerInterface import MicrosoftSamFileManagerInterface
from src.tts.microsoftSam.microsoftSamTtsManager import MicrosoftSamTtsManager
from src.tts.microsoftSam.microsoftSamTtsManagerInterface import MicrosoftSamTtsManagerInterface
from src.tts.streamElements.streamElementsFileManager import StreamElementsFileManager
from src.tts.streamElements.streamElementsFileManagerInterface import StreamElementsFileManagerInterface
from src.tts.streamElements.streamElementsTtsManager import StreamElementsTtsManager
from src.tts.streamElements.streamElementsTtsManagerInterface import StreamElementsTtsManagerInterface
from src.tts.ttsCommandBuilder import TtsCommandBuilder
from src.tts.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from src.tts.ttsJsonMapper import TtsJsonMapper
from src.tts.ttsJsonMapperInterface import TtsJsonMapperInterface
from src.tts.ttsMonster.ttsMonsterFileManager import TtsMonsterFileManager
from src.tts.ttsMonster.ttsMonsterFileManagerInterface import TtsMonsterFileManagerInterface
from src.tts.ttsMonster.ttsMonsterTtsManager import TtsMonsterTtsManager
from src.tts.ttsMonster.ttsMonsterTtsManagerInterface import TtsMonsterTtsManagerInterface
from src.tts.ttsSettingsRepository import TtsSettingsRepository
from src.tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from src.ttsMonster.apiService.ttsMonsterApiService import TtsMonsterApiService
from src.ttsMonster.apiService.ttsMonsterApiServiceInterface import TtsMonsterApiServiceInterface
from src.ttsMonster.apiService.ttsMonsterPrivateApiService import TtsMonsterPrivateApiService
from src.ttsMonster.apiService.ttsMonsterPrivateApiServiceInterface import TtsMonsterPrivateApiServiceInterface
from src.ttsMonster.apiTokens.ttsMonsterApiTokensRepository import TtsMonsterApiTokensRepository
from src.ttsMonster.apiTokens.ttsMonsterApiTokensRepositoryInterface import TtsMonsterApiTokensRepositoryInterface
from src.ttsMonster.helper.ttsMonsterHelper import TtsMonsterHelper
from src.ttsMonster.helper.ttsMonsterHelperInterface import TtsMonsterHelperInterface
from src.ttsMonster.helper.ttsMonsterPrivateApiHelper import TtsMonsterPrivateApiHelper
from src.ttsMonster.helper.ttsMonsterPrivateApiHelperInterface import TtsMonsterPrivateApiHelperInterface
from src.ttsMonster.keyAndUserIdRepository.ttsMonsterKeyAndUserIdRepository import TtsMonsterKeyAndUserIdRepository
from src.ttsMonster.keyAndUserIdRepository.ttsMonsterKeyAndUserIdRepositoryInterface import \
    TtsMonsterKeyAndUserIdRepositoryInterface
from src.ttsMonster.mapper.ttsMonsterJsonMapper import TtsMonsterJsonMapper
from src.ttsMonster.mapper.ttsMonsterJsonMapperInterface import TtsMonsterJsonMapperInterface
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapper import TtsMonsterPrivateApiJsonMapper
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapper import TtsMonsterWebsiteVoiceMapper
from src.ttsMonster.mapper.ttsMonsterWebsiteVoiceMapperInterface import TtsMonsterWebsiteVoiceMapperInterface
from src.ttsMonster.messageToVoicesHelper.ttsMonsterMessageToVoicesHelper import TtsMonsterMessageToVoicesHelper
from src.ttsMonster.messageToVoicesHelper.ttsMonsterMessageToVoicesHelperInterface import \
    TtsMonsterMessageToVoicesHelperInterface
from src.ttsMonster.settings.ttsMonsterSettingsRepository import TtsMonsterSettingsRepository
from src.ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from src.ttsMonster.streamerVoices.ttsMonsterStreamerVoicesRepository import TtsMonsterStreamerVoicesRepository
from src.ttsMonster.streamerVoices.ttsMonsterStreamerVoicesRepositoryInterface import \
    TtsMonsterStreamerVoicesRepositoryInterface
from src.ttsMonster.ttsMonsterMessageCleaner import TtsMonsterMessageCleaner
from src.ttsMonster.ttsMonsterMessageCleanerInterface import TtsMonsterMessageCleanerInterface
from src.twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from src.twitch.absTwitchFollowHandler import AbsTwitchFollowHandler
from src.twitch.absTwitchPollHandler import AbsTwitchPollHandler
from src.twitch.absTwitchPredictionHandler import AbsTwitchPredictionHandler
from src.twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from src.twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from src.twitch.activeChatters.activeChattersRepository import ActiveChattersRepository
from src.twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from src.twitch.api.twitchApiService import TwitchApiService
from src.twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from src.twitch.api.twitchJsonMapper import TwitchJsonMapper
from src.twitch.api.twitchJsonMapperInterface import TwitchJsonMapperInterface
from src.twitch.channelEditors.twitchChannelEditorsRepository import TwitchChannelEditorsRepository
from src.twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from src.twitch.configuration.twitchChannelJoinHelper import TwitchChannelJoinHelper
from src.twitch.configuration.twitchCheerHandler import TwitchCheerHandler
from src.twitch.configuration.twitchConfiguration import TwitchConfiguration
from src.twitch.configuration.twitchFollowHandler import TwitchFollowHandler
from src.twitch.configuration.twitchIo.twitchIoConfiguration import TwitchIoConfiguration
from src.twitch.configuration.twitchPollHandler import TwitchPollHandler
from src.twitch.configuration.twitchPredictionHandler import TwitchPredictionHandler
from src.twitch.configuration.twitchRaidHandler import TwitchRaidHandler
from src.twitch.configuration.twitchSubscriptionHandler import TwitchSubscriptionHandler
from src.twitch.emotes.twitchEmotesHelper import TwitchEmotesHelper
from src.twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from src.twitch.followingStatus.twitchFollowingStatusRepository import TwitchFollowingStatusRepository
from src.twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from src.twitch.friends.twitchFriendsUserIdRepository import TwitchFriendsUserIdRepository
from src.twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from src.twitch.isLiveOnTwitchRepository import IsLiveOnTwitchRepository
from src.twitch.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from src.twitch.officialTwitchAccountUserIdProvider import OfficialTwitchAccountUserIdProvider
from src.twitch.officialTwitchAccountUserIdProviderInterface import OfficialTwitchAccountUserIdProviderInterface
from src.twitch.timeout.timeoutImmuneUserIdsRepository import TimeoutImmuneUserIdsRepository
from src.twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from src.twitch.timeout.twitchTimeoutHelper import TwitchTimeoutHelper
from src.twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from src.twitch.timeout.twitchTimeoutRemodHelper import TwitchTimeoutRemodHelper
from src.twitch.timeout.twitchTimeoutRemodHelperInterface import TwitchTimeoutRemodHelperInterface
from src.twitch.timeout.twitchTimeoutRemodRepository import TwitchTimeoutRemodRepository
from src.twitch.timeout.twitchTimeoutRemodRepositoryInterface import TwitchTimeoutRemodRepositoryInterface
from src.twitch.twitchChannelJoinHelperInterface import TwitchChannelJoinHelperInterface
from src.twitch.twitchMessageStringUtils import TwitchMessageStringUtils
from src.twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from src.twitch.twitchPredictionWebsocketUtils import TwitchPredictionWebsocketUtils
from src.twitch.twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface
from src.twitch.twitchTokensRepository import TwitchTokensRepository
from src.twitch.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from src.twitch.twitchTokensUtils import TwitchTokensUtils
from src.twitch.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from src.twitch.twitchUtils import TwitchUtils
from src.twitch.twitchUtilsInterface import TwitchUtilsInterface
from src.twitch.websocket.twitchWebsocketAllowedUsersRepository import TwitchWebsocketAllowedUsersRepository
from src.twitch.websocket.twitchWebsocketAllowedUsersRepositoryInterface import \
    TwitchWebsocketAllowedUsersRepositoryInterface
from src.twitch.websocket.twitchWebsocketClient import TwitchWebsocketClient
from src.twitch.websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from src.twitch.websocket.twitchWebsocketJsonMapper import TwitchWebsocketJsonMapper
from src.twitch.websocket.twitchWebsocketJsonMapperInterface import TwitchWebsocketJsonMapperInterface
from src.users.addOrRemoveUserDataHelper import AddOrRemoveUserDataHelper
from src.users.addOrRemoveUserDataHelperInterface import AddOrRemoveUserDataHelperInterface
from src.users.crowdControl.crowdControlJsonParser import CrowdControlJsonParser
from src.users.crowdControl.crowdControlJsonParserInterface import CrowdControlJsonParserInterface
from src.users.cuteness.cutenessBoosterPackJsonParser import CutenessBoosterPackJsonParser
from src.users.cuteness.cutenessBoosterPackJsonParserInterface import CutenessBoosterPackJsonParserInterface
from src.users.decTalkSongs.decTalkSongBoosterPackParser import DecTalkSongBoosterPackParser
from src.users.decTalkSongs.decTalkSongBoosterPackParserInterface import DecTalkSongBoosterPackParserInterface
from src.users.pkmn.pkmnBoosterPackJsonParser import PkmnBoosterPackJsonParser
from src.users.pkmn.pkmnBoosterPackJsonParserInterface import PkmnBoosterPackJsonParserInterface
from src.users.soundAlert.soundAlertRedemptionJsonParser import SoundAlertRedemptionJsonParser
from src.users.soundAlert.soundAlertRedemptionJsonParserInterface import SoundAlertRedemptionJsonParserInterface
from src.users.timeout.timeoutBoosterPackJsonParser import TimeoutBoosterPackJsonParser
from src.users.timeout.timeoutBoosterPackJsonParserInterface import TimeoutBoosterPackJsonParserInterface
from src.users.tts.ttsBoosterPackParser import TtsBoosterPackParser
from src.users.tts.ttsBoosterPackParserInterface import TtsBoosterPackParserInterface
from src.users.ttsChatters.ttsChatterBoosterPackParser import TtsChatterBoosterPackParser
from src.users.ttsChatters.ttsChatterBoosterPackParserInterface import TtsChatterBoosterPackParserInterface
from src.users.userIdsRepository import UserIdsRepository
from src.users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from src.users.usersRepository import UsersRepository
from src.users.usersRepositoryInterface import UsersRepositoryInterface
from src.websocketConnection.mapper.websocketEventTypeMapper import WebsocketEventTypeMapper
from src.websocketConnection.mapper.websocketEventTypeMapperInterface import WebsocketEventTypeMapperInterface
from src.websocketConnection.settings.websocketConnectionServerSettings import WebsocketConnectionServerSettings
from src.websocketConnection.settings.websocketConnectionServerSettingsInterface import \
    WebsocketConnectionServerSettingsInterface
from src.websocketConnection.websocketConnectionServer import WebsocketConnectionServer
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
storageJsonMapper: StorageJsonMapperInterface = StorageJsonMapper()

generalSettingsRepository = GeneralSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/generalSettingsRepository.json'),
    networkJsonMapper = networkJsonMapper,
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
    twitchJsonMapper = twitchJsonMapper,
    twitchWebsocketJsonMapper = twitchWebsocketJsonMapper,
)

tempFileHelper: TempFileHelperInterface = TempFileHelper(
    eventLoop = eventLoop
)

officialTwitchAccountUserIdProvider: OfficialTwitchAccountUserIdProviderInterface = OfficialTwitchAccountUserIdProvider()

userIdsRepository: UserIdsRepositoryInterface = UserIdsRepository(
    backingDatabase = backingDatabase,
    officialTwitchAccountUserIdProvider = officialTwitchAccountUserIdProvider,
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

crowdControlJsonParser: CrowdControlJsonParserInterface = CrowdControlJsonParser()

cutenessBoosterPackJsonParser: CutenessBoosterPackJsonParserInterface = CutenessBoosterPackJsonParser()

decTalkSongBoosterPackParser: DecTalkSongBoosterPackParserInterface = DecTalkSongBoosterPackParser()

languageEntryJsonMapper: LanguageEntryJsonMapperInterface = LanguageEntryJsonMapper()

pkmnBoosterPackJsonParser: PkmnBoosterPackJsonParserInterface = PkmnBoosterPackJsonParser(
    timber = timber
)

soundAlertJsonMapper: SoundAlertJsonMapperInterface = SoundAlertJsonMapper(
    timber = timber
)

soundAlertRedemptionJsonParser: SoundAlertRedemptionJsonParserInterface = SoundAlertRedemptionJsonParser(
    soundAlertJsonMapper = soundAlertJsonMapper
)

streamElementsJsonParser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

timeoutBoosterPackJsonParser: TimeoutBoosterPackJsonParserInterface = TimeoutBoosterPackJsonParser()

ttsJsonMapper: TtsJsonMapperInterface = TtsJsonMapper(
    timber = timber
)

ttsBoosterPackParser: TtsBoosterPackParserInterface = TtsBoosterPackParser(
    ttsJsonMapper = ttsJsonMapper
)

halfLifeJsonParser: HalfLifeJsonParserInterface = HalfLifeJsonParser()

microsoftSamJsonParser: MicrosoftSamJsonParserInterface = MicrosoftSamJsonParser()

ttsChatterBoosterPackParser: TtsChatterBoosterPackParserInterface = TtsChatterBoosterPackParser(
    halfLifeJsonParser = halfLifeJsonParser,
    microsoftSamJsonParser = microsoftSamJsonParser,
    streamElementsJsonParser = streamElementsJsonParser,
    ttsJsonMapper = ttsJsonMapper
)

usersRepository: UsersRepositoryInterface = UsersRepository(
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


######################################
## Trollmoji initialization section ##
######################################

trollmojiSettingsRepository: TrollmojiSettingsRepositoryInterface = TrollmojiSettingsRepository(
    twitchFriendsUserIdRepository = twitchFriendsUserIdRepository
)

trollmojiHelper: TrollmojiHelperInterface = TrollmojiHelper(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    trollmojiSettingsRepository = trollmojiSettingsRepository,
    twitchEmotesHelper = twitchEmotesHelper
)


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

twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface = TwitchChannelEditorsRepository(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchApiService = twitchApiService,
    twitchTokensRepository = twitchTokensRepository
)

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

twitchWebsocketClient: TwitchWebsocketClientInterface | None = None
if generalSettingsSnapshot.isEventSubEnabled():
    twitchWebsocketClient = TwitchWebsocketClient(
        backgroundTaskHelper = backgroundTaskHelper,
        timber = timber,
        timeZoneRepository = timeZoneRepository,
        twitchApiService = twitchApiService,
        twitchHandleProvider = authRepository,
        twitchTokensRepository = twitchTokensRepository,
        twitchWebsocketAllowedUsersRepository = twitchWebsocketAllowedUsersRepository,
        twitchWebsocketJsonMapper = twitchWebsocketJsonMapper
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

chatBandInstrumentSoundsRepository: ChatBandInstrumentSoundsRepositoryInterface | None = None


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

soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = VlcSoundPlayerManagerProvider(
    chatBandInstrumentSoundsRepository = chatBandInstrumentSoundsRepository,
    soundPlayerSettingsRepository = soundPlayerSettingsRepository,
    timber = timber
)


################################
## TTS initialization section ##
################################

ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/ttsSettingsRepository.json')
)

ttsCommandBuilder: TtsCommandBuilderInterface = TtsCommandBuilder()

decTalkFileManager: DecTalkFileManagerInterface = DecTalkFileManager(
    tempFileHelper = tempFileHelper
)

decTalkVoiceMapper: DecTalkVoiceMapperInterface = DecTalkVoiceMapper()

decTalkSettingsRepository: DecTalkSettingsRepositoryInterface = DecTalkSettingsRepository(
    decTalkVoiceMapper = decTalkVoiceMapper,
    settingsJsonReader = JsonFileReader('../config/decTalkSettingsRepository.json')
)

decTalkApiService: DecTalkApiServiceInterface = DecTalkApiService(
    decTalkFileManager = decTalkFileManager,
    decTalkSettingsRepository = decTalkSettingsRepository,
    timber = timber
)

decTalkHelper: DecTalkHelperInterface = DecTalkHelper(
    apiService = decTalkApiService,
    timber = timber
)

decTalkMessageCleaner: DecTalkMessageCleanerInterface = DecTalkMessageCleaner(
    emojiHelper = emojiHelper,
    timber = timber,
    ttsSettingsRepository = ttsSettingsRepository
)

singingDecTalkMessageCleaner: DecTalkMessageCleanerInterface = DecTalkMessageCleaner(
    emojiHelper = emojiHelper,
    timber = timber,
    ttsSettingsRepository = ttsSettingsRepository,
    sing = True
)

decTalkVoiceChooser: DecTalkVoiceChooserInterface = DecTalkVoiceChooser()

singingDecTalkTtsManager: DecTalkTtsManagerInterface | None = SingingDecTalkTtsManager(
    decTalkHelper = decTalkHelper,
    decTalkMessageCleaner = singingDecTalkMessageCleaner,
    decTalkSettingsRepository = decTalkSettingsRepository,
    decTalkVoiceChooser = decTalkVoiceChooser,
    soundPlayerManager = soundPlayerManagerProvider.getSharedSoundPlayerManagerInstance(),
    timber = timber,
    ttsCommandBuilder = ttsCommandBuilder,
    ttsSettingsRepository = ttsSettingsRepository
)

decTalkTtsManager: DecTalkTtsManagerInterface | None = DecTalkTtsManager(
    decTalkHelper = decTalkHelper,
    decTalkMessageCleaner = decTalkMessageCleaner,
    decTalkSettingsRepository = decTalkSettingsRepository,
    decTalkVoiceChooser = decTalkVoiceChooser,
    soundPlayerManager = soundPlayerManagerProvider.getSharedSoundPlayerManagerInstance(),
    timber = timber,
    ttsCommandBuilder = ttsCommandBuilder,
    ttsSettingsRepository = ttsSettingsRepository
)

googleSettingsRepository: GoogleSettingsRepositoryInterface = GoogleSettingsRepository(
    googleJsonMapper = googleJsonMapper,
    settingsJsonReader = JsonFileReader('../config/googleSettingsRepository.json')
)

googleFileExtensionHelper: GoogleFileExtensionHelperInterface = GoogleFileExtensionHelper()

googleTtsFileManager: GoogleTtsFileManagerInterface = GoogleTtsFileManager(
    eventLoop = eventLoop,
    googleFileExtensionHelper = googleFileExtensionHelper,
    googleSettingsRepository = googleSettingsRepository,
    tempFileHelper = tempFileHelper,
    timber = timber
)

googleTtsMessageCleaner: GoogleTtsMessageCleanerInterface = GoogleTtsMessageCleaner(
    ttsSettingsRepository = ttsSettingsRepository
)

googleTtsVoiceChooser: GoogleTtsVoiceChooserInterface = GoogleTtsVoiceChooser()

googleTtsHelper: GoogleTtsHelperInterface = GoogleTtsHelper(
    googleApiService = googleApiService,
    googleSettingsRepository = googleSettingsRepository,
    googleTtsFileManager = googleTtsFileManager,
    googleTtsVoiceChooser = googleTtsVoiceChooser,
    timber = timber
)

googleTtsManager: GoogleTtsManagerInterface | None = GoogleTtsManager(
    googleSettingsRepository = googleSettingsRepository,
    googleTtsHelper = googleTtsHelper,
    googleTtsMessageCleaner = googleTtsMessageCleaner,
    soundPlayerManager = soundPlayerManagerProvider.getSharedSoundPlayerManagerInstance(),
    timber = timber,
    ttsCommandBuilder = ttsCommandBuilder,
    ttsSettingsRepository = ttsSettingsRepository
)

halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface = HalfLifeSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/halfLifeTtsSettingsRepository.json'),
    halfLifeJsonParser = halfLifeJsonParser
)

halfLifeService: HalfLifeServiceInterface = HalfLifeService(
    timber = timber
)

halfLifeMessageVoiceParser: HalfLifeMessageVoiceParserInterface = HalfLifeMessageVoiceParser(
    halfLifeJsonParser = halfLifeJsonParser
)

halfLifeHelper: HalfLifeHelperInterface = HalfLifeHelper(
    halfLifeService = halfLifeService,
    halfLifeMessageVoiceParser = halfLifeMessageVoiceParser,
    halfLifeSettingsRepository = halfLifeSettingsRepository
)

halfLifeMessageCleaner: HalfLifeMessageCleanerInterface = HalfLifeMessageCleaner(
    ttsSettingsRepository = ttsSettingsRepository
)

halfLifeTtsManager: HalfLifeTtsManagerInterface | None = HalfLifeTtsManager(
    halfLifeHelper = halfLifeHelper,
    halfLifeMessageCleaner = halfLifeMessageCleaner,
    halfLifeSettingsRepository = halfLifeSettingsRepository,
    soundPlayerManager = soundPlayerManagerProvider.getSharedSoundPlayerManagerInstance(),
    timber = timber,
    ttsSettingsRepository = ttsSettingsRepository,
    ttsCommandBuilder = ttsCommandBuilder
)

microsoftSamFileManager: MicrosoftSamFileManagerInterface = MicrosoftSamFileManager(
    eventLoop = eventLoop,
    tempFileHelper = tempFileHelper,
    timber = timber
)

microsoftSamApiService: MicrosoftSamApiServiceInterface = MicrosoftSamApiService(
    networkClientProvider = networkClientProvider,
    timber = timber
)

microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface = MicrosoftSamSettingsRepository(
    microsoftSamJsonParser = microsoftSamJsonParser,
    settingsJsonReader = JsonFileReader('../config/microsoftSamSettingsRepository.json')
)

microsoftSamVoiceMapper: MicrosoftSamVoiceMapperInterface = MicrosoftSamVoiceMapper()

microsoftSamMessageVoiceParser: MicrosoftSamMessageVoiceParserInterface = MicrosoftSamMessageVoiceParser()

microsoftSamHelper: MicrosoftSamHelperInterface = MicrosoftSamHelper(
    apiService = microsoftSamApiService,
    microsoftSamMessageVoiceParser = microsoftSamMessageVoiceParser,
    microsoftSamSettingsRepository = microsoftSamSettingsRepository,
    microsoftSamVoiceMapper = microsoftSamVoiceMapper,
    timber = timber
)

microsoftSamMessageCleaner: MicrosoftSamMessageCleanerInterface = MicrosoftSamMessageCleaner(
    ttsSettingsRepository = ttsSettingsRepository
)

microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface = MicrosoftSamSettingsRepository(
    microsoftSamJsonParser = microsoftSamJsonParser,
    settingsJsonReader = JsonFileReader('../config/microsoftSamSettingsRepository.json')
)

microsoftSamTtsManager: MicrosoftSamTtsManagerInterface = MicrosoftSamTtsManager(
    microsoftSamFileManager = microsoftSamFileManager,
    microsoftSamHelper = microsoftSamHelper,
    microsoftSamMessageCleaner = microsoftSamMessageCleaner,
    microsoftSamSettingsRepository = microsoftSamSettingsRepository,
    soundPlayerManager = soundPlayerManagerProvider.getSharedSoundPlayerManagerInstance(),
    timber = timber,
    ttsCommandBuilder = ttsCommandBuilder,
    ttsSettingsRepository = ttsSettingsRepository
)

streamElementsApiService: StreamElementsApiServiceInterface = StreamElementsApiService(
    networkClientProvider = networkClientProvider,
    timber = timber
)

streamElementsMessageCleaner: StreamElementsMessageCleanerInterface = StreamElementsMessageCleaner(
    ttsSettingsRepository = ttsSettingsRepository
)

streamElementsMessageVoiceParser: StreamElementsMessageVoiceParserInterface = StreamElementsMessageVoiceParser()

streamElementsJsonParser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface = StreamElementsSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/streamElementsSettingsRepository.json'),
    streamElementsJsonParser = streamElementsJsonParser
)

streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface = StreamElementsUserKeyRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    userIdsRepository = userIdsRepository,
    seedFileReader = JsonFileReader('../config/streamElementsUserKeyRepositorySeedFile.json')
)

streamElementsHelper: StreamElementsHelperInterface = StreamElementsHelper(
    streamElementsApiService = streamElementsApiService,
    streamElementsMessageVoiceParser = streamElementsMessageVoiceParser,
    streamElementsSettingsRepository = streamElementsSettingsRepository,
    streamElementsUserKeyRepository = streamElementsUserKeyRepository,
    timber = timber
)

streamElementsFileManager: StreamElementsFileManagerInterface = StreamElementsFileManager(
    eventLoop = eventLoop,
    tempFileHelper = tempFileHelper,
    timber = timber
)

streamElementsTtsManager: StreamElementsTtsManagerInterface | None = StreamElementsTtsManager(
    soundPlayerManager = soundPlayerManagerProvider.getSharedSoundPlayerManagerInstance(),
    streamElementsFileManager = streamElementsFileManager,
    streamElementsHelper = streamElementsHelper,
    streamElementsMessageCleaner = streamElementsMessageCleaner,
    streamElementsSettingsRepository = streamElementsSettingsRepository,
    timber = timber,
    ttsCommandBuilder = ttsCommandBuilder,
    ttsSettingsRepository = ttsSettingsRepository
)

ttsMonsterApiTokensRepository: TtsMonsterApiTokensRepositoryInterface = TtsMonsterApiTokensRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    userIdsRepository = userIdsRepository,
    seedFileReader = JsonFileReader('../config/ttsMonsterApiTokensRepositorySeedFile.json')
)

ttsMonsterWebsiteVoiceMapper: TtsMonsterWebsiteVoiceMapperInterface = TtsMonsterWebsiteVoiceMapper()

ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface = TtsMonsterSettingsRepository(
    ttsMonsterWebsiteVoiceMapper = ttsMonsterWebsiteVoiceMapper,
    settingsJsonReader = JsonFileReader('../config/ttsMonsterSettingsRepository.json')
)

ttsMonsterJsonMapper: TtsMonsterJsonMapperInterface = TtsMonsterJsonMapper(
    timber = timber,
    websiteVoiceMapper = ttsMonsterWebsiteVoiceMapper
)

ttsMonsterApiService: TtsMonsterApiServiceInterface = TtsMonsterApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    ttsMonsterJsonMapper = ttsMonsterJsonMapper
)

ttsMonsterMessageToVoicesHelper: TtsMonsterMessageToVoicesHelperInterface = TtsMonsterMessageToVoicesHelper(
    ttsMonsterSettingsRepository = ttsMonsterSettingsRepository
)

ttsMonsterKeyAndUserIdRepository: TtsMonsterKeyAndUserIdRepositoryInterface = TtsMonsterKeyAndUserIdRepository(
    settingsJsonReader = JsonFileReader('../config/ttsMonsterKeyAndUserIdRepository.json')
)

ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface = TtsMonsterPrivateApiJsonMapper()

ttsMonsterPrivateApiService: TtsMonsterPrivateApiServiceInterface = TtsMonsterPrivateApiService(
    networkClientProvider = networkClientProvider,
    timber = timber,
    ttsMonsterPrivateApiJsonMapper = ttsMonsterPrivateApiJsonMapper
)

ttsMonsterPrivateApiHelper: TtsMonsterPrivateApiHelperInterface = TtsMonsterPrivateApiHelper(
    timber = timber,
    ttsMonsterKeyAndUserIdRepository = ttsMonsterKeyAndUserIdRepository,
    ttsMonsterPrivateApiService = ttsMonsterPrivateApiService
)

ttsMonsterStreamerVoicesRepository: TtsMonsterStreamerVoicesRepositoryInterface = TtsMonsterStreamerVoicesRepository(
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    ttsMonsterApiService = ttsMonsterApiService,
    ttsMonsterApiTokensRepository = ttsMonsterApiTokensRepository
)

ttsMonsterMessageCleaner: TtsMonsterMessageCleanerInterface = TtsMonsterMessageCleaner(
    ttsSettingsRepository = ttsSettingsRepository
)

ttsMonsterHelper: TtsMonsterHelperInterface = TtsMonsterHelper(
    timber = timber,
    ttsMonsterApiService = ttsMonsterApiService,
    ttsMonsterApiTokensRepository = ttsMonsterApiTokensRepository,
    ttsMonsterMessageToVoicesHelper = ttsMonsterMessageToVoicesHelper,
    ttsMonsterPrivateApiHelper = ttsMonsterPrivateApiHelper,
    ttsMonsterSettingsRepository = ttsMonsterSettingsRepository,
    ttsMonsterStreamerVoicesRepository = ttsMonsterStreamerVoicesRepository
)

ttsMonsterFileManager: TtsMonsterFileManagerInterface = TtsMonsterFileManager(
    eventLoop = eventLoop,
    tempFileHelper = tempFileHelper,
    timber = timber,
    ttsMonsterApiService = ttsMonsterApiService
)

ttsMonsterTtsManager: TtsMonsterTtsManagerInterface | None = TtsMonsterTtsManager(
    soundPlayerManager = soundPlayerManagerProvider.getSharedSoundPlayerManagerInstance(),
    timber = timber,
    ttsMonsterFileManager = ttsMonsterFileManager,
    ttsMonsterHelper = ttsMonsterHelper,
    ttsMonsterMessageCleaner = ttsMonsterMessageCleaner,
    ttsMonsterSettingsRepository = ttsMonsterSettingsRepository,
    ttsSettingsRepository = ttsSettingsRepository,
    twitchUtils = twitchUtils
)

compositeTtsManager: CompositeTtsManagerInterface | None = CompositeTtsManager(
    backgroundTaskHelper = backgroundTaskHelper,
    decTalkTtsManager = decTalkTtsManager,
    googleTtsManager = googleTtsManager,
    halfLifeTtsManager = halfLifeTtsManager,
    microsoftSamTtsManager = microsoftSamTtsManager,
    singingDecTalkTtsManager = singingDecTalkTtsManager,
    streamElementsTtsManager = streamElementsTtsManager,
    timber = timber,
    ttsMonsterTtsManager = ttsMonsterTtsManager,
    ttsSettingsRepository = ttsSettingsRepository
)


#################################
## Aniv initialization section ##
#################################

anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface = AnivCopyMessageTimeoutScorePresenter()

anivCopyMessageTimeoutScoreRepository: AnivCopyMessageTimeoutScoreRepositoryInterface = AnivCopyMessageTimeoutScoreRepository(
    backingDatabase = backingDatabase,
    timeZoneRepository = timeZoneRepository,
    userIdsRepository = userIdsRepository
)

anivSettingsRepository: AnivSettingsRepositoryInterface = AnivSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/anivSettingsRepository.json')
)

anivContentScanner: AnivContentScannerInterface = AnivContentScanner(
    contentScanner = contentScanner,
    timber = timber
)

anivUserIdProvider: AnivUserIdProviderInterface = AnivUserIdProvider()

guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface = GuaranteedTimeoutUsersRepository(
    anivUserIdProvider = anivUserIdProvider,
    twitchFriendsUserIdRepository = twitchFriendsUserIdRepository
)

mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface | None = MostRecentAnivMessageRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None = None
if mostRecentAnivMessageRepository is not None:
    mostRecentAnivMessageTimeoutHelper = MostRecentAnivMessageTimeoutHelper(
        anivCopyMessageTimeoutScoreRepository = anivCopyMessageTimeoutScoreRepository,
        anivSettingsRepository = anivSettingsRepository,
        anivUserIdProvider = anivUserIdProvider,
        mostRecentAnivMessageRepository = mostRecentAnivMessageRepository,
        timber = timber,
        timeoutImmuneUserIdsRepository = timeoutImmuneUserIdsRepository,
        timeZoneRepository = timeZoneRepository,
        trollmojiHelper = trollmojiHelper,
        twitchChannelEditorsRepository = twitchChannelEditorsRepository,
        twitchHandleProvider = authRepository,
        twitchTimeoutHelper = twitchTimeoutHelper,
        twitchTokensRepository = twitchTokensRepository,
        twitchUtils = twitchUtils
    )


##########################################
## Crowd Control initialization section ##
##########################################

crowdControlIdGenerator: CrowdControlIdGeneratorInterface = CrowdControlIdGenerator()

crowdControlMessagePresenter: CrowdControlMessagePresenterInterface = CrowdControlMessagePresenter(
    trollmojiHelper = trollmojiHelper
)

crowdControlMessageHandler = CrowdControlMessageHandler(
    crowdControlMessagePresenter = crowdControlMessagePresenter,
    twitchUtils = twitchUtils
)

crowdControlSettingsRepository: CrowdControlSettingsRepositoryInterface = CrowdControlSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/crowdControlSettingsRepository.json')
)

crowdControlMachine: CrowdControlMachineInterface = CrowdControlMachine(
    backgroundTaskHelper = backgroundTaskHelper,
    crowdControlIdGenerator = crowdControlIdGenerator,
    crowdControlSettingsRepository = crowdControlSettingsRepository,
    soundPlayerManagerProvider = soundPlayerManagerProvider,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

crowdControlAutomator: CrowdControlAutomatorInterface = CrowdControlAutomator(
    backgroundTaskHelper = backgroundTaskHelper,
    crowdControlIdGenerator = crowdControlIdGenerator,
    crowdControlMachine = crowdControlMachine,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    twitchHandleProvider = authRepository,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)

crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface = CrowdControlUserInputUtils()

crowdControlCheerActionHelper: CrowdControlCheerActionHelperInterface = CrowdControlCheerActionHelper(
    crowdControlIdGenerator = crowdControlIdGenerator,
    crowdControlMachine = crowdControlMachine,
    crowdControlSettingsRepository = crowdControlSettingsRepository,
    crowdControlUserInputUtils = crowdControlUserInputUtils,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

bizhawkKeyMapper: BizhawkKeyMapperInterface = BizhawkKeyMapper(
    timber = timber
)

bizhawkSettingsRepository: BizhawkSettingsRepositoryInterface = BizhawkSettingsRepository(
    bizhawkKeyMapper = bizhawkKeyMapper,
    settingsJsonReader = JsonFileReader('../config/bizhawkSettingsRepository.json')
)

crowdControlActionHandler: CrowdControlActionHandler = BizhawkActionHandler(
    backgroundTaskHelper = backgroundTaskHelper,
    bizhawkSettingsRepository = bizhawkSettingsRepository,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)


##################################################
## Stream Alerts Manager initialization section ##
##################################################

streamAlertsSettingsRepository: StreamAlertsSettingsRepositoryInterface = StreamAlertsSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/streamAlertsSettingsRepository.json')
)

streamAlertsManager: StreamAlertsManagerInterface = StreamAlertsManager(
    backgroundTaskHelper = backgroundTaskHelper,
    compositeTtsManager = compositeTtsManager,
    soundPlayerManager = soundPlayerManagerProvider.getSharedSoundPlayerManagerInstance(),
    streamAlertsSettingsRepository = streamAlertsSettingsRepository,
    timber = timber
)


####################################
## Timeout initialization section ##
####################################

timeoutActionJsonMapper: TimeoutActionJsonMapperInterface = TimeoutActionJsonMapper(
    timber = timber
)

timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface = TimeoutActionSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/timeoutActionSettings.json')
)

timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface = TimeoutActionHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeoutActionJsonMapper = timeoutActionJsonMapper,
    timeZoneRepository = timeZoneRepository
)

timeoutActionHelper: TimeoutActionHelperInterface = TimeoutActionHelper(
    guaranteedTimeoutUsersRepository = guaranteedTimeoutUsersRepository,
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    streamAlertsManager = streamAlertsManager,
    timber = timber,
    timeoutActionHistoryRepository = timeoutActionHistoryRepository,
    timeoutActionSettingsRepository = timeoutActionSettingsRepository,
    timeoutImmuneUserIdsRepository = timeoutImmuneUserIdsRepository,
    timeZoneRepository = timeZoneRepository,
    trollmojiHelper = trollmojiHelper,
    twitchChannelEditorsRepository = twitchChannelEditorsRepository,
    twitchConstants = twitchUtils,
    twitchFollowingStatusRepository = twitchFollowingStatusRepository,
    twitchTimeoutHelper = twitchTimeoutHelper,
    twitchUtils = twitchUtils
)


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

beanChanceCheerActionHelper: BeanChanceCheerActionHelperInterface | None = BeanChanceCheerActionHelper(
    beanStatsRepository = beanStatsRepository,
    soundPlayerManagerProvider = soundPlayerManagerProvider,
    timber = timber,
    twitchEmotesHelper = twitchEmotesHelper,
    twitchFriendsUserIdRepository = twitchFriendsUserIdRepository,
    twitchUtils = twitchUtils
)

soundAlertCheerActionHelper: SoundAlertCheerActionHelperInterface | None = SoundAlertCheerActionHelper(
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    soundPlayerManagerProvider = soundPlayerManagerProvider,
    soundPlayerRandomizerHelper = soundPlayerRandomizerHelper,
    timber = timber
)

timeoutActionJsonMapper: TimeoutActionJsonMapperInterface = TimeoutActionJsonMapper(
    timber = timber
)

timeoutActionSettingsRepository: TimeoutActionSettingsRepositoryInterface = TimeoutActionSettingsRepository(
    settingsJsonReader = JsonFileReader('../config/timeoutActionSettings.json')
)

timeoutActionHistoryRepository: TimeoutActionHistoryRepositoryInterface = TimeoutActionHistoryRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeoutActionJsonMapper = timeoutActionJsonMapper,
    timeZoneRepository = timeZoneRepository
)

timeoutCheerActionMapper: TimeoutCheerActionMapper = TimeoutCheerActionMapper()

timeoutCheerActionHelper: TimeoutCheerActionHelperInterface | None = TimeoutCheerActionHelper(
    timber = timber,
    timeoutActionHelper = timeoutActionHelper,
    timeoutCheerActionMapper = timeoutCheerActionMapper,
    twitchMessageStringUtils = twitchMessageStringUtils,
    userIdsRepository = userIdsRepository
)

cheerActionHelper: CheerActionHelperInterface = CheerActionHelper(
    beanChanceCheerActionHelper = beanChanceCheerActionHelper,
    cheerActionsRepository = cheerActionsRepository,
    crowdControlCheerActionHelper = crowdControlCheerActionHelper,
    soundAlertCheerActionHelper = soundAlertCheerActionHelper,
    timeoutCheerActionHelper = timeoutCheerActionHelper,
    twitchHandleProvider = authRepository,
    twitchTokensRepository = twitchTokensRepository,
    userIdsRepository = userIdsRepository
)


#########################################
## Chat Actions initialization section ##
#########################################

activeChattersRepository: ActiveChattersRepositoryInterface = ActiveChattersRepository(
    timeZoneRepository = timeZoneRepository
)

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

saveMostRecentAnivMessageChatAction: SaveMostRecentAnivMessageChatAction | None = SaveMostRecentAnivMessageChatAction(
    anivUserIdProvider = anivUserIdProvider,
    mostRecentAnivMessageRepository = mostRecentAnivMessageRepository
)

supStreamerRepository: SupStreamerRepositoryInterface = SupStreamerRepository(
    backingDatabase = backingDatabase,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

supStreamerHelper: SupStreamerHelperInterface = SupStreamerHelper()

supStreamerChatAction: SupStreamerChatAction | None = SupStreamerChatAction(
    streamAlertsManager = streamAlertsManager,
    supStreamerHelper = supStreamerHelper,
    supStreamerRepository = supStreamerRepository,
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

ttsChattersChatAction: TtsChattersChatAction = TtsChattersChatAction(
    streamAlertsManager = streamAlertsManager
)

chatActionsManager: ChatActionsManagerInterface = ChatActionsManager(
    activeChattersRepository = activeChattersRepository,
    anivCheckChatAction = None,
    chatBackMessagesChatAction = None,
    chatLoggerChatAction = None,
    cheerActionsWizardChatAction = cheerActionsWizardChatAction,
    generalSettingsRepository = generalSettingsRepository,
    mostRecentAnivMessageTimeoutHelper = mostRecentAnivMessageTimeoutHelper,
    mostRecentChatsRepository = mostRecentChatsRepository,
    persistAllUsersChatAction = persistAllUsersChatAction,
    recurringActionsWizardChatAction = None,
    saveMostRecentAnivMessageChatAction = saveMostRecentAnivMessageChatAction,
    supStreamerChatAction = supStreamerChatAction,
    timber = timber,
    ttsChattersChatAction = ttsChattersChatAction,
    twitchUtils = twitchUtils,
    userIdsRepository = userIdsRepository,
    usersRepository = usersRepository
)


########################################################
## Websocket Connection Server initialization section ##
########################################################

websocketConnectionServerSettings: WebsocketConnectionServerSettingsInterface = WebsocketConnectionServerSettings(
    settingsJsonReader = JsonFileReader('../config/websocketConnectionServerSettings.json')
)

websocketEventTypeMapper: WebsocketEventTypeMapperInterface = WebsocketEventTypeMapper()

websocketConnectionServer: WebsocketConnectionServerInterface = WebsocketConnectionServer(
    backgroundTaskHelper = backgroundTaskHelper,
    timber = timber,
    timeZoneRepository = timeZoneRepository,
    websocketConnectionServerSettings = websocketConnectionServerSettings,
    websocketEventTypeMapper = websocketEventTypeMapper
)


##########################################
## Twitch events initialization section ##
##########################################

twitchCheerHandler: AbsTwitchCheerHandler | None = TwitchCheerHandler(
    cheerActionHelper = cheerActionHelper,
    streamAlertsManager = streamAlertsManager,
    timber = timber,
    triviaGameBuilder = None,
    triviaGameMachine = None
)

twitchFollowHandler: AbsTwitchFollowHandler | None = TwitchFollowHandler(
    timber = timber,
    twitchFollowingStatusRepository = twitchFollowingStatusRepository
)

twitchPollHandler: AbsTwitchPollHandler | None = TwitchPollHandler(
    streamAlertsManager = streamAlertsManager,
    timber = timber,
    twitchUtils = twitchUtils
)

twitchPredictionHandler: AbsTwitchPredictionHandler | None = TwitchPredictionHandler(
    streamAlertsManager = streamAlertsManager,
    timber = timber,
    twitchUtils = twitchUtils,
    twitchPredictionWebsocketUtils = twitchPredictionWebsocketUtils,
    websocketConnectionServer = websocketConnectionServer
)

twitchRaidHandler: AbsTwitchRaidHandler | None = TwitchRaidHandler(
    chatLogger = chatLogger,
    streamAlertsManager = streamAlertsManager,
    timber = timber
)

twitchSubscriptionHandler: AbsTwitchSubscriptionHandler | None = TwitchSubscriptionHandler(
    streamAlertsManager = streamAlertsManager,
    timber = timber,
    triviaGameBuilder = None,
    triviaGameMachine = None,
    twitchEmotesHelper = twitchEmotesHelper,
    twitchHandleProvider = authRepository,
    twitchTokensUtils = twitchTokensUtils,
    twitchUtils = twitchUtils,
    userIdsRepository = userIdsRepository
)


#####################################
## CynanBot initialization section ##
#####################################

cynanBot = CynanBot(
    eventLoop = eventLoop,
    twitchCheerHandler = twitchCheerHandler,
    twitchFollowHandler = twitchFollowHandler,
    twitchPollHandler = twitchPollHandler,
    twitchPredictionHandler = twitchPredictionHandler,
    twitchRaidHandler = twitchRaidHandler,
    twitchSubscriptionHandler = twitchSubscriptionHandler,
    additionalTriviaAnswersRepository = None,
    addOrRemoveUserDataHelper = addOrRemoveUserDataHelper,
    administratorProvider = administratorProvider,
    anivCopyMessageTimeoutScorePresenter = anivCopyMessageTimeoutScorePresenter,
    anivCopyMessageTimeoutScoreRepository = anivCopyMessageTimeoutScoreRepository,
    anivSettingsRepository = anivSettingsRepository,
    authRepository = authRepository,
    backgroundTaskHelper = backgroundTaskHelper,
    bannedTriviaGameControllersRepository = None,
    bannedWordsRepository = bannedWordsRepository,
    beanChanceCheerActionHelper = beanChanceCheerActionHelper,
    beanStatsPresenter = beanStatsPresenter,
    beanStatsRepository = beanStatsRepository,
    bizhawkSettingsRepository = bizhawkSettingsRepository,
    chatActionsManager = chatActionsManager,
    chatLogger = chatLogger,
    cheerActionHelper = cheerActionHelper,
    cheerActionJsonMapper = cheerActionJsonMapper,
    cheerActionSettingsRepository = cheerActionSettingsRepository,
    cheerActionsRepository = cheerActionsRepository,
    cheerActionsWizard = cheerActionsWizard,
    compositeTtsManager = compositeTtsManager,
    crowdControlActionHandler = crowdControlActionHandler,
    crowdControlAutomator = crowdControlAutomator,
    crowdControlIdGenerator = crowdControlIdGenerator,
    crowdControlMachine = crowdControlMachine,
    crowdControlMessageHandler = crowdControlMessageHandler,
    crowdControlSettingsRepository = crowdControlSettingsRepository,
    crowdControlUserInputUtils = crowdControlUserInputUtils,
    cutenessPresenter = None,
    cutenessRepository = None,
    cutenessUtils = None,
    funtoonHelper = funtoonHelper,
    funtoonTokensRepository = funtoonTokensRepository,
    generalSettingsRepository = generalSettingsRepository,
    halfLifeService = halfLifeService,
    isLiveOnTwitchRepository = isLiveOnTwitchRepository,
    jishoHelper = None,
    languagesRepository = languagesRepository,
    locationsRepository = locationsRepository,
    mostRecentAnivMessageRepository = mostRecentAnivMessageRepository,
    mostRecentAnivMessageTimeoutHelper = mostRecentAnivMessageTimeoutHelper,
    mostRecentChatsRepository = mostRecentChatsRepository,
    openTriviaDatabaseSessionTokenRepository = None,
    pokepediaRepository = None,
    psqlCredentialsProvider = psqlCredentialsProvider,
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
    streamAlertsSettingsRepository = streamAlertsSettingsRepository,
    streamElementsSettingsRepository = streamElementsSettingsRepository,
    streamElementsUserKeyRepository = streamElementsUserKeyRepository,
    supStreamerRepository = supStreamerRepository,
    timber = timber,
    timeoutActionHelper = timeoutActionHelper,
    timeoutActionHistoryRepository = timeoutActionHistoryRepository,
    timeoutActionSettingsRepository = timeoutActionSettingsRepository,
    timeZoneRepository = timeZoneRepository,
    toxicTriviaOccurencesRepository = None,
    translationHelper = None,
    triviaBanHelper = None,
    triviaEmoteGenerator = None,
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
    trollmojiHelper = trollmojiHelper,
    trollmojiSettingsRepository = trollmojiSettingsRepository,
    ttsJsonMapper = ttsJsonMapper,
    ttsMonsterApiTokensRepository = ttsMonsterApiTokensRepository,
    ttsMonsterKeyAndUserIdRepository = ttsMonsterKeyAndUserIdRepository,
    ttsMonsterTtsManager = ttsMonsterTtsManager,
    ttsMonsterSettingsRepository = ttsMonsterSettingsRepository,
    ttsMonsterStreamerVoicesRepository = ttsMonsterStreamerVoicesRepository,
    ttsSettingsRepository = ttsSettingsRepository,
    twitchApiService = twitchApiService,
    twitchChannelEditorsRepository = twitchChannelEditorsRepository,
    twitchChannelJoinHelper = twitchChannelJoinHelper,
    twitchConfiguration = twitchConfiguration,
    twitchEmotesHelper = twitchEmotesHelper,
    twitchFollowingStatusRepository = twitchFollowingStatusRepository,
    twitchFriendsUserIdRepository = twitchFriendsUserIdRepository,
    twitchMessageStringUtils = twitchMessageStringUtils,
    twitchPredictionWebsocketUtils = twitchPredictionWebsocketUtils,
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
