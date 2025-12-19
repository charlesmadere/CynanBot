import traceback
from asyncio import AbstractEventLoop
from typing import Final

from twitchio import Channel, Message, User
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import CommandNotFound

from .aniv.helpers.anivCopyMessageTimeoutScoreHelperInterface import AnivCopyMessageTimeoutScoreHelperInterface
from .aniv.helpers.mostRecentAnivMessageTimeoutHelperInterface import MostRecentAnivMessageTimeoutHelperInterface
from .aniv.presenters.anivCopyMessageTimeoutScorePresenterInterface import \
    AnivCopyMessageTimeoutScorePresenterInterface
from .aniv.repositories.mostRecentAnivMessageRepositoryInterface import MostRecentAnivMessageRepositoryInterface
from .aniv.settings.anivSettingsInterface import AnivSettingsInterface
from .asplodieStats.asplodieStatsPresenter import AsplodieStatsPresenter
from .asplodieStats.repository.asplodieStatsRepositoryInterface import AsplodieStatsRepositoryInterface
from .beanStats.beanStatsPresenterInterface import BeanStatsPresenterInterface
from .beanStats.beanStatsRepositoryInterface import BeanStatsRepositoryInterface
from .chatActions.manager.chatActionsManagerInterface import ChatActionsManagerInterface
from .chatCommands.absChatCommand import AbsChatCommand
from .chatCommands.addBannedTriviaControllerChatCommand import AddBannedTriviaControllerChatCommand
from .chatCommands.addCrowdControlCheerActionChatCommand import AddCrowdControlCheerActionChatCommand
from .chatCommands.addGameShuffleAutomatorChatCommand import AddGameShuffleAutomatorChatCommand
from .chatCommands.addGameShuffleCheerActionChatCommand import AddGameShuffleCheerActionChatCommand
from .chatCommands.addGlobalTriviaControllerChatCommand import AddGlobalTriviaControllerChatCommand
from .chatCommands.addItemUseCheerActionChatCommand import AddItemUseCheerActionChatCommand
from .chatCommands.addRecurringCutenessActionChatCommand import AddRecurringCutenessActionChatCommand
from .chatCommands.addRecurringSuperTriviaActionChatCommand import AddRecurringSuperTriviaActionChatCommand
from .chatCommands.addRecurringWeatherActionChatCommand import AddRecurringWeatherActionChatCommand
from .chatCommands.addRecurringWordOfTheDayActionChatCommand import AddRecurringWordOfTheDayActionChatCommand
from .chatCommands.addSoundAlertCheerActionCommand import AddSoundAlertCheerActionCommand
from .chatCommands.addTriviaAnswerChatCommand import AddTriviaAnswerChatCommand
from .chatCommands.addTriviaControllerChatCommand import AddTriviaControllerChatCommand
from .chatCommands.addUserChatCommand import AddUserChatCommand
from .chatCommands.addVoicemailCheerActionCommand import AddVoicemailCheerActionCommand
from .chatCommands.anivTimeoutsChatCommand import AnivTimeoutsChatCommand
from .chatCommands.answerChatCommand import AnswerChatCommand
from .chatCommands.asplodieStatsChatCommand import AsplodieStatsChatCommand
from .chatCommands.banTriviaQuestionChatCommand import BanTriviaQuestionChatCommand
from .chatCommands.beanInstructionsChatCommand import BeanInstructionsChatCommand
from .chatCommands.beanStatsChatCommand import BeanStatsChatCommand
from .chatCommands.blueSkyChatCommand import BlueSkyChatCommand
from .chatCommands.chatterInventoryChatCommand import ChatterInventoryChatCommand
from .chatCommands.clearCachesChatCommand import ClearCachesChatCommand
from .chatCommands.clearSuperTriviaQueueChatCommand import ClearSuperTriviaQueueChatCommand
from .chatCommands.commandsChatCommand import CommandsChatCommand
from .chatCommands.confirmChatCommand import ConfirmChatCommand
from .chatCommands.crowdControlChatCommand import CrowdControlChatCommand
from .chatCommands.cutenessChampionsChatCommand import CutenessChampionsChatCommand
from .chatCommands.cutenessChatCommand import CutenessChatCommand
from .chatCommands.cutenessHistoryChatCommand import CutenessHistoryChatCommand
from .chatCommands.cynanSourceChatCommand import CynanSourceChatCommand
from .chatCommands.deleteCheerActionChatCommand import DeleteCheerActionChatCommand
from .chatCommands.deleteTriviaAnswersChatCommand import DeleteTriviaAnswersChatCommand
from .chatCommands.disableCheerActionChatCommand import DisableCheerActionChatCommand
from .chatCommands.discordChatCommand import DiscordChatCommand
from .chatCommands.eccoChatCommand import EccoChatCommand
from .chatCommands.enableCheerActionChatCommand import EnableCheerActionChatCommand
from .chatCommands.freeGiveChatterItemChatCommand import FreeGiveChatterItemChatCommand
from .chatCommands.getBannedTriviaControllersChatCommand import GetBannedTriviaControllersChatCommand
from .chatCommands.getChatterPreferredNameChatCommand import GetChatterPreferredNameChatCommand
from .chatCommands.getChatterPreferredTtsChatCommand import GetChatterPreferredTtsChatCommand
from .chatCommands.getCheerActionsChatCommand import GetCheerActionsChatCommand
from .chatCommands.getGlobalTriviaControllersChatCommand import GetGlobalTriviaControllersChatCommand
from .chatCommands.getRecurringActionsChatCommand import GetRecurringActionsChatCommand
from .chatCommands.getTriviaAnswersChatCommand import GetTriviaAnswersChatCommand
from .chatCommands.getTriviaControllersChatCommand import GetTriviaControllersChatCommand
from .chatCommands.giveChatterItemChatCommand import GiveChatterItemChatCommand
from .chatCommands.giveCutenessChatCommand import GiveCutenessChatCommand
from .chatCommands.jishoChatCommand import JishoChatCommand
from .chatCommands.loremIpsumChatCommand import LoremIpsumChatCommand
from .chatCommands.myCutenessChatCommand import MyCutenessChatCommand
from .chatCommands.pkMonChatCommand import PkMonChatCommand
from .chatCommands.pkMoveChatCommand import PkMoveChatCommand
from .chatCommands.playVoicemailChatCommand import PlayVoicemailChatCommand
from .chatCommands.removeBannedTriviaControllerChatCommand import RemoveBannedTriviaControllerChatCommand
from .chatCommands.removeChatterPreferredNameChatCommand import RemoveChatterPreferredNameChatCommand
from .chatCommands.removeChatterPreferredTtsChatCommand import RemoveChatterPreferredTtsChatCommand
from .chatCommands.removeGameShuffleAutomatorChatCommand import RemoveGameShuffleAutomatorChatCommand
from .chatCommands.removeGlobalTriviaControllerChatCommand import RemoveGlobalTriviaControllerChatCommand
from .chatCommands.removeRecurringCutenessActionChatCommand import RemoveRecurringCutenessActionChatCommand
from .chatCommands.removeRecurringSuperTriviaActionCommand import RemoveRecurringSuperTriviaActionCommand
from .chatCommands.removeRecurringWeatherActionCommand import RemoveRecurringWeatherActionCommand
from .chatCommands.removeRecurringWordOfTheDayAction import RemoveRecurringWordOfTheDayActionCommand
from .chatCommands.removeTriviaControllerChatCommand import RemoveTriviaControllerChatCommand
from .chatCommands.removeTtsChatterChatCommand import RemoveTtsChatterChatCommand
from .chatCommands.removeUserChatCommand import RemoveUserChatCommand
from .chatCommands.setChatterPreferredNameChatCommand import SetChatterPreferredNameChatCommand
from .chatCommands.setChatterPreferredTtsChatCommand import SetChatterPreferredTtsChatCommand
from .chatCommands.setFuntoonTokenChatCommand import SetFuntoonTokenChatCommand
from .chatCommands.setTwitchCodeChatCommand import SetTwitchCodeChatCommand
from .chatCommands.skipTtsChatCommand import SkipTtsChatCommand
from .chatCommands.stubChatCommand import StubChatCommand
from .chatCommands.superAnswerChatCommand import SuperAnswerChatCommand
from .chatCommands.superTriviaChatCommand import SuperTriviaChatCommand
from .chatCommands.swQuoteChatCommand import SwQuoteChatCommand
from .chatCommands.testCheerChatCommand import TestCheerChatCommand
from .chatCommands.timeChatCommand import TimeChatCommand
from .chatCommands.translateChatCommand import TranslateChatCommand
from .chatCommands.triviaInfoChatCommand import TriviaInfoChatCommand
from .chatCommands.triviaScoreChatCommand import TriviaScoreChatCommand
from .chatCommands.ttsChatCommand import TtsChatCommand
from .chatCommands.twitchUserInfoChatCommand import TwitchUserInfoChatCommand
from .chatCommands.unbanTriviaQuestionChatCommand import UnbanTriviaQuestionChatCommand
from .chatCommands.useChatterItemChatCommand import UseChatterItemChatCommand
from .chatCommands.voicemailsChatCommand import VoicemailsChatCommand
from .chatCommands.vulnerableChattersChatCommand import VulnerableChattersChatCommand
from .chatCommands.weatherChatCommand import WeatherChatCommand
from .chatCommands.wordChatCommand import WordChatCommand
from .chatLogger.chatLoggerInterface import ChatLoggerInterface
from .chatterInventory.configuration.absChatterItemEventHandler import AbsChatterItemEventHandler
from .chatterInventory.helpers.chatterInventoryHelperInterface import ChatterInventoryHelperInterface
from .chatterInventory.helpers.useChatterItemHelperInterface import UseChatterItemHelperInterface
from .chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from .chatterInventory.machine.chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from .chatterInventory.mappers.chatterInventoryMapperInterface import ChatterInventoryMapperInterface
from .chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from .chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from .chatterPreferredName.repositories.chatterPreferredNameRepositoryInterface import \
    ChatterPreferredNameRepositoryInterface
from .chatterPreferredName.settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from .chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from .chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from .chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelperInterface import \
    ChatterPreferredTtsUserMessageHelperInterface
from .chatterPreferredTts.repository.chatterPreferredTtsRepositoryInterface import \
    ChatterPreferredTtsRepositoryInterface
from .chatterPreferredTts.settings.chatterPreferredTtsSettingsRepositoryInterface import \
    ChatterPreferredTtsSettingsRepositoryInterface
from .cheerActions.airStrike.airStrikeCheerActionHelperInterface import AirStrikeCheerActionHelperInterface
from .cheerActions.beanChance.beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
from .cheerActions.cheerActionHelperInterface import CheerActionHelperInterface
from .cheerActions.cheerActionJsonMapperInterface import CheerActionJsonMapperInterface
from .cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from .cheerActions.cheerActionsWizardInterface import CheerActionsWizardInterface
from .cheerActions.settings.cheerActionSettingsRepositoryInterface import CheerActionSettingsRepositoryInterface
from .commodoreSam.settings.commodoreSamSettingsRepositoryInterface import CommodoreSamSettingsRepositoryInterface
from .contentScanner.bannedWordsRepositoryInterface import BannedWordsRepositoryInterface
from .crowdControl.automator.crowdControlAutomatorInterface import CrowdControlAutomatorInterface
from .crowdControl.bizhawk.bizhawkSettingsRepositoryInterface import BizhawkSettingsRepositoryInterface
from .crowdControl.crowdControlActionHandler import CrowdControlActionHandler
from .crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from .crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from .crowdControl.message.crowdControlMessageListener import CrowdControlMessageListener
from .crowdControl.settings.crowdControlSettingsRepositoryInterface import CrowdControlSettingsRepositoryInterface
from .crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from .cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from .cuteness.cutenessRepositoryInterface import CutenessRepositoryInterface
from .cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from .decTalk.settings.decTalkSettingsRepositoryInterface import DecTalkSettingsRepositoryInterface
from .ecco.eccoHelperInterface import EccoHelperInterface
from .funtoon.funtoonHelperInterface import FuntoonHelperInterface
from .funtoon.tokens.funtoonTokensRepositoryInterface import FuntoonTokensRepositoryInterface
from .google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from .halfLife.settings.halfLifeSettingsRepositoryInterface import HalfLifeSettingsRepositoryInterface
from .language.jishoHelperInterface import JishoHelperInterface
from .language.languagesRepositoryInterface import LanguagesRepositoryInterface
from .language.translationHelperInterface import TranslationHelperInterface
from .language.wordOfTheDay.wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from .language.wordOfTheDay.wordOfTheDayRepositoryInterface import WordOfTheDayRepositoryInterface
from .location.locationsRepositoryInterface import LocationsRepositoryInterface
from .location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from .microsoftSam.settings.microsoftSamSettingsRepositoryInterface import MicrosoftSamSettingsRepositoryInterface
from .misc import utils as utils
from .misc.administratorProviderInterface import AdministratorProviderInterface
from .misc.authRepository import AuthRepository
from .misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .misc.generalSettingsRepository import GeneralSettingsRepository
from .mostRecentChat.mostRecentChatsRepositoryInterface import MostRecentChatsRepositoryInterface
from .pixelsDice.listeners.pixelsDiceEventListener import PixelsDiceEventListener
from .pixelsDice.machine.pixelsDiceMachineInterface import PixelsDiceMachineInterface
from .pkmn.pokepediaRepositoryInterface import PokepediaRepositoryInterface
from .recurringActions.configuration.absRecurringActionsEventHandler import AbsRecurringActionsEventHandler
from .recurringActions.recurringActionsHelperInterface import RecurringActionsHelperInterface
from .recurringActions.recurringActionsMachineInterface import RecurringActionsMachineInterface
from .recurringActions.recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from .recurringActions.recurringActionsWizardInterface import RecurringActionsWizardInterface
from .sentMessageLogger.sentMessageLoggerInterface import SentMessageLoggerInterface
from .soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from .soundPlayerManager.randomizerHelper.soundPlayerRandomizerHelper import SoundPlayerRandomizerHelperInterface
from .soundPlayerManager.settings.soundPlayerSettingsRepositoryInterface import SoundPlayerSettingsRepositoryInterface
from .starWars.starWarsQuotesRepositoryInterface import StarWarsQuotesRepositoryInterface
from .storage.psql.psqlCredentialsProviderInterface import PsqlCredentialsProviderInterface
from .streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from .streamAlertsManager.streamAlertsSettingsRepositoryInterface import StreamAlertsSettingsRepositoryInterface
from .streamElements.settings.streamElementsSettingsRepositoryInterface import StreamElementsSettingsRepositoryInterface
from .streamElements.userKeyRepository.streamElementsUserKeyRepositoryInterface import \
    StreamElementsUserKeyRepositoryInterface
from .supStreamer.supStreamerRepositoryInterface import SupStreamerRepositoryInterface
from .timber.timberInterface import TimberInterface
from .timeout.configuration.absTimeoutEventHandler import AbsTimeoutEventHandler
from .timeout.guaranteedTimeoutUsersRepositoryInterface import GuaranteedTimeoutUsersRepositoryInterface
from .timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from .timeout.settings.timeoutActionSettingsInterface import TimeoutActionSettingsInterface
from .trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from .trivia.banned.bannedTriviaGameControllersRepositoryInterface import BannedTriviaGameControllersRepositoryInterface
from .trivia.banned.triviaBanHelperInterface import TriviaBanHelperInterface
from .trivia.builder.triviaGameBuilderInterface import TriviaGameBuilderInterface
from .trivia.configuration.absTriviaEventHandler import AbsTriviaEventHandler
from .trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from .trivia.emotes.twitch.triviaTwitchEmoteHelperInterface import TriviaTwitchEmoteHelperInterface
from .trivia.gameController.triviaGameControllersRepositoryInterface import TriviaGameControllersRepositoryInterface
from .trivia.gameController.triviaGameGlobalControllersRepositoryInterface import \
    TriviaGameGlobalControllersRepositoryInterface
from .trivia.history.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from .trivia.history.triviaQuestionOccurrencesRepositoryInterface import TriviaQuestionOccurrencesRepositoryInterface
from .trivia.score.triviaScoreRepositoryInterface import TriviaScoreRepositoryInterface
from .trivia.settings.triviaSettingsRepositoryInterface import TriviaSettingsRepositoryInterface
from .trivia.specialStatus.shinyTriviaOccurencesRepositoryInterface import ShinyTriviaOccurencesRepositoryInterface
from .trivia.specialStatus.toxicTriviaOccurencesRepositoryInterface import ToxicTriviaOccurencesRepositoryInterface
from .trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from .trivia.triviaIdGeneratorInterface import TriviaIdGeneratorInterface
from .trivia.triviaRepositories.openTriviaDatabase.openTriviaDatabaseSessionTokenRepositoryInterface import \
    OpenTriviaDatabaseSessionTokenRepositoryInterface
from .trivia.triviaRepositories.triviaRepositoryInterface import TriviaRepositoryInterface
from .trivia.triviaUtilsInterface import TriviaUtilsInterface
from .trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from .trollmoji.trollmojiSettingsRepositoryInterface import TrollmojiSettingsRepositoryInterface
from .tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from .tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from .tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from .ttsChatter.repository.ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from .ttsChatter.settings.ttsChatterSettingsRepositoryInterface import TtsChatterSettingsRepositoryInterface
from .ttsMonster.settings.ttsMonsterSettingsRepositoryInterface import TtsMonsterSettingsRepositoryInterface
from .ttsMonster.tokens.ttsMonsterTokensRepositoryInterface import \
    TtsMonsterTokensRepositoryInterface
from .twitch.absTwitchChannelPointRedemptionHandler import AbsTwitchChannelPointRedemptionHandler
from .twitch.absTwitchChatHandler import AbsTwitchChatHandler
from .twitch.absTwitchCheerHandler import AbsTwitchCheerHandler
from .twitch.absTwitchFollowHandler import AbsTwitchFollowHandler
from .twitch.absTwitchHypeTrainHandler import AbsTwitchHypeTrainHandler
from .twitch.absTwitchPollHandler import AbsTwitchPollHandler
from .twitch.absTwitchPredictionHandler import AbsTwitchPredictionHandler
from .twitch.absTwitchRaidHandler import AbsTwitchRaidHandler
from .twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from .twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from .twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from .twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from .twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from .twitch.configuration.absChannelJoinEvent import AbsChannelJoinEvent
from .twitch.configuration.channelJoinListener import ChannelJoinListener
from .twitch.configuration.finishedJoiningChannelsEvent import FinishedJoiningChannelsEvent
from .twitch.configuration.joinChannelsEvent import JoinChannelsEvent
from .twitch.configuration.twitchChannel import TwitchChannel
from .twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from .twitch.configuration.twitchConfiguration import TwitchConfiguration
from .twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider
from .twitch.emotes.twitchEmotesHelperInterface import TwitchEmotesHelperInterface
from .twitch.followingStatus.twitchFollowingStatusRepositoryInterface import TwitchFollowingStatusRepositoryInterface
from .twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from .twitch.ircReconnectHelper.twitchIrcReconnectHelperInterface import TwitchIrcReconnectHelperInterface
from .twitch.isLive.isLiveOnTwitchRepositoryInterface import IsLiveOnTwitchRepositoryInterface
from .twitch.subscribers.twitchSubscriptionsRepositoryInterface import TwitchSubscriptionsRepositoryInterface
from .twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from .twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from .twitch.timeout.twitchTimeoutRemodHelperInterface import TwitchTimeoutRemodHelperInterface
from .twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from .twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from .twitch.twitchChannelJoinHelperInterface import TwitchChannelJoinHelperInterface
from .twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface
from .twitch.twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface
from .twitch.twitchUtilsInterface import TwitchUtilsInterface
from .twitch.twitchWebsocketDataBundleHandler import TwitchWebsocketDataBundleHandler
from .twitch.websocket.settings.twitchWebsocketSettingsRepositoryInterface import \
    TwitchWebsocketSettingsRepositoryInterface
from .twitch.websocket.twitchWebsocketClientInterface import TwitchWebsocketClientInterface
from .users.addOrRemoveUserActionType import AddOrRemoveUserActionType
from .users.addOrRemoveUserData import AddOrRemoveUserData
from .users.addOrRemoveUserDataHelperInterface import AddOrRemoveUserDataHelperInterface
from .users.addOrRemoveUserEventListener import AddOrRemoveUserEventListener
from .users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from .users.userInterface import UserInterface
from .users.usersRepositoryInterface import UsersRepositoryInterface
from .voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from .voicemail.repositories.voicemailsRepositoryInterface import VoicemailsRepositoryInterface
from .voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface
from .weather.weatherReportPresenterInterface import WeatherReportPresenterInterface
from .weather.weatherRepositoryInterface import WeatherRepositoryInterface
from .websocketConnection.websocketConnectionServerInterface import WebsocketConnectionServerInterface


class CynanBot(
    commands.Bot,
    AddOrRemoveUserEventListener,
    ChannelJoinListener,
    TwitchChannelProvider,
    TwitchConnectionReadinessProvider,
):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        twitchChannelPointRedemptionHandler: AbsTwitchChannelPointRedemptionHandler | None,
        twitchChatHandler: AbsTwitchChatHandler | None,
        twitchCheerHandler: AbsTwitchCheerHandler | None,
        twitchFollowHandler: AbsTwitchFollowHandler | None,
        twitchHypeTrainHandler: AbsTwitchHypeTrainHandler | None,
        twitchPollHandler: AbsTwitchPollHandler | None,
        twitchPredictionHandler: AbsTwitchPredictionHandler | None,
        twitchRaidHandler: AbsTwitchRaidHandler | None,
        twitchSubscriptionHandler: AbsTwitchSubscriptionHandler | None,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface | None,
        addOrRemoveUserDataHelper: AddOrRemoveUserDataHelperInterface,
        administratorProvider: AdministratorProviderInterface,
        airStrikeCheerActionHelper: AirStrikeCheerActionHelperInterface | None,
        anivCopyMessageTimeoutScoreHelper: AnivCopyMessageTimeoutScoreHelperInterface | None,
        anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface | None,
        anivSettings: AnivSettingsInterface | None,
        asplodieStatsPresenter: AsplodieStatsPresenter | None,
        asplodieStatsRepository: AsplodieStatsRepositoryInterface | None,
        authRepository: AuthRepository,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        bannedTriviaGameControllersRepository: BannedTriviaGameControllersRepositoryInterface | None,
        bannedWordsRepository: BannedWordsRepositoryInterface | None,
        beanChanceCheerActionHelper: BeanChanceCheerActionHelperInterface | None,
        beanStatsPresenter: BeanStatsPresenterInterface | None,
        beanStatsRepository: BeanStatsRepositoryInterface | None,
        bizhawkSettingsRepository: BizhawkSettingsRepositoryInterface | None,
        chatActionsManager: ChatActionsManagerInterface | None,
        chatLogger: ChatLoggerInterface,
        chatterInventoryHelper: ChatterInventoryHelperInterface | None,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface | None,
        chatterInventoryItemUseMachine: ChatterInventoryItemUseMachineInterface | None,
        chatterInventoryMapper: ChatterInventoryMapperInterface | None,
        chatterInventorySettings: ChatterInventorySettingsInterface | None,
        chatterItemEventHandler: AbsChatterItemEventHandler | None,
        chatterPreferredNameHelper: ChatterPreferredNameHelperInterface | None,
        chatterPreferredNameRepository: ChatterPreferredNameRepositoryInterface | None,
        chatterPreferredNameSettings: ChatterPreferredNameSettingsInterface | None,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface | None,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter | None,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface | None,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface | None,
        chatterPreferredTtsUserMessageHelper: ChatterPreferredTtsUserMessageHelperInterface | None,
        cheerActionHelper: CheerActionHelperInterface | None,
        cheerActionJsonMapper: CheerActionJsonMapperInterface | None,
        cheerActionSettingsRepository: CheerActionSettingsRepositoryInterface | None,
        cheerActionsRepository: CheerActionsRepositoryInterface | None,
        cheerActionsWizard: CheerActionsWizardInterface | None,
        commodoreSamSettingsRepository: CommodoreSamSettingsRepositoryInterface | None,
        compositeTtsManagerProvider: CompositeTtsManagerProviderInterface,
        crowdControlActionHandler: CrowdControlActionHandler | None,
        crowdControlAutomator: CrowdControlAutomatorInterface | None,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface | None,
        crowdControlMachine: CrowdControlMachineInterface | None,
        crowdControlMessageListener: CrowdControlMessageListener | None,
        crowdControlSettingsRepository: CrowdControlSettingsRepositoryInterface | None,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface | None,
        cutenessPresenter: CutenessPresenterInterface | None,
        cutenessRepository: CutenessRepositoryInterface | None,
        cutenessUtils: CutenessUtilsInterface | None,
        decTalkSettingsRepository: DecTalkSettingsRepositoryInterface | None,
        eccoHelper: EccoHelperInterface | None,
        funtoonHelper: FuntoonHelperInterface | None,
        funtoonTokensRepository: FuntoonTokensRepositoryInterface | None,
        generalSettingsRepository: GeneralSettingsRepository,
        googleSettingsRepository: GoogleSettingsRepositoryInterface | None,
        guaranteedTimeoutUsersRepository: GuaranteedTimeoutUsersRepositoryInterface | None,
        halfLifeSettingsRepository: HalfLifeSettingsRepositoryInterface | None,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface | None,
        jishoHelper: JishoHelperInterface | None,
        languagesRepository: LanguagesRepositoryInterface,
        locationsRepository: LocationsRepositoryInterface | None,
        microsoftSamSettingsRepository: MicrosoftSamSettingsRepositoryInterface | None,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface | None,
        mostRecentAnivMessageTimeoutHelper: MostRecentAnivMessageTimeoutHelperInterface | None,
        mostRecentChatsRepository: MostRecentChatsRepositoryInterface | None,
        openTriviaDatabaseSessionTokenRepository: OpenTriviaDatabaseSessionTokenRepositoryInterface | None,
        pixelsDiceEventListener: PixelsDiceEventListener | None,
        pixelsDiceMachine: PixelsDiceMachineInterface | None,
        pokepediaRepository: PokepediaRepositoryInterface | None,
        psqlCredentialsProvider: PsqlCredentialsProviderInterface | None,
        recurringActionsEventHandler: AbsRecurringActionsEventHandler | None,
        recurringActionsHelper: RecurringActionsHelperInterface | None,
        recurringActionsMachine: RecurringActionsMachineInterface | None,
        recurringActionsRepository: RecurringActionsRepositoryInterface | None,
        recurringActionsWizard: RecurringActionsWizardInterface | None,
        sentMessageLogger: SentMessageLoggerInterface,
        shinyTriviaOccurencesRepository: ShinyTriviaOccurencesRepositoryInterface | None,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface | None,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface | None,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface | None,
        starWarsQuotesRepository: StarWarsQuotesRepositoryInterface | None,
        streamAlertsManager: StreamAlertsManagerInterface,
        streamAlertsSettingsRepository: StreamAlertsSettingsRepositoryInterface | None,
        streamElementsSettingsRepository: StreamElementsSettingsRepositoryInterface | None,
        streamElementsUserKeyRepository: StreamElementsUserKeyRepositoryInterface | None,
        supStreamerRepository: SupStreamerRepositoryInterface | None,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface | None,
        timeoutActionSettings: TimeoutActionSettingsInterface | None,
        timeoutEventHandler: AbsTimeoutEventHandler | None,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface | None,
        timeZoneRepository: TimeZoneRepositoryInterface,
        toxicTriviaOccurencesRepository: ToxicTriviaOccurencesRepositoryInterface | None,
        translationHelper: TranslationHelperInterface | None,
        triviaBanHelper: TriviaBanHelperInterface | None,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface | None,
        triviaEventHandler: AbsTriviaEventHandler | None,
        triviaGameBuilder: TriviaGameBuilderInterface | None,
        triviaGameControllersRepository: TriviaGameControllersRepositoryInterface | None,
        triviaGameGlobalControllersRepository: TriviaGameGlobalControllersRepositoryInterface | None,
        triviaGameMachine: TriviaGameMachineInterface | None,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface | None,
        triviaIdGenerator: TriviaIdGeneratorInterface | None,
        triviaRepository: TriviaRepositoryInterface | None,
        triviaQuestionOccurrencesRepository: TriviaQuestionOccurrencesRepositoryInterface | None,
        triviaScoreRepository: TriviaScoreRepositoryInterface | None,
        triviaSettingsRepository: TriviaSettingsRepositoryInterface |  None,
        triviaTwitchEmoteHelper: TriviaTwitchEmoteHelperInterface | None,
        triviaUtils: TriviaUtilsInterface | None,
        trollmojiHelper: TrollmojiHelperInterface | None,
        trollmojiSettingsRepository: TrollmojiSettingsRepositoryInterface | None,
        ttsChatterRepository: TtsChatterRepositoryInterface | None,
        ttsChatterSettingsRepository: TtsChatterSettingsRepositoryInterface | None,
        ttsJsonMapper: TtsJsonMapperInterface | None,
        ttsMonsterSettingsRepository: TtsMonsterSettingsRepositoryInterface | None,
        ttsMonsterTokensRepository: TtsMonsterTokensRepositoryInterface | None,
        ttsSettingsRepository: TtsSettingsRepositoryInterface | None,
        twitchApiService: TwitchApiServiceInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchChannelJoinHelper: TwitchChannelJoinHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchConfiguration: TwitchConfiguration,
        twitchEmotesHelper: TwitchEmotesHelperInterface,
        twitchFollowingStatusRepository: TwitchFollowingStatusRepositoryInterface | None,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface | None,
        twitchIrcReconnectHelper: TwitchIrcReconnectHelperInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        twitchPredictionWebsocketUtils: TwitchPredictionWebsocketUtilsInterface | None,
        twitchSubscriptionsRepository: TwitchSubscriptionsRepositoryInterface | None,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface | None,
        twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface | None,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        twitchWebsocketClient: TwitchWebsocketClientInterface | None,
        twitchWebsocketSettingsRepository: TwitchWebsocketSettingsRepositoryInterface | None,
        useChatterItemHelper: UseChatterItemHelperInterface | None,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        voicemailHelper: VoicemailHelperInterface | None,
        voicemailsRepository: VoicemailsRepositoryInterface | None,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface | None,
        weatherReportPresenter: WeatherReportPresenterInterface | None,
        weatherRepository: WeatherRepositoryInterface | None,
        websocketConnectionServer: WebsocketConnectionServerInterface | None,
        wordOfTheDayPresenter: WordOfTheDayPresenterInterface | None,
        wordOfTheDayRepository: WordOfTheDayRepositoryInterface | None,
    ):
        super().__init__(
            client_secret = authRepository.getAll().requireTwitchClientSecret(),
            initial_channels = list(),
            loop = eventLoop,
            nick = authRepository.getAll().requireTwitchHandle(),
            prefix = '!',
            retain_cache = True,
            token = authRepository.getAll().requireTwitchIrcAuthToken(),
            heartbeat = 15,
        )

        if not isinstance(eventLoop, AbstractEventLoop):
            raise TypeError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif twitchChannelPointRedemptionHandler is not None and not isinstance(twitchChannelPointRedemptionHandler, AbsTwitchChannelPointRedemptionHandler):
            raise TypeError(f'twitchChannelPointRedemptionHandler argument is malformed: \"{twitchChannelPointRedemptionHandler}\"')
        elif twitchChatHandler is not None and not isinstance(twitchChatHandler, AbsTwitchChatHandler):
            raise TypeError(f'twitchChatHandler argument is malformed: \"{twitchChatHandler}\"')
        elif twitchCheerHandler is not None and not isinstance(twitchCheerHandler, AbsTwitchCheerHandler):
            raise TypeError(f'twitchCheerHandler argument is malformed: \"{twitchCheerHandler}\"')
        elif twitchFollowHandler is not None and not isinstance(twitchFollowHandler, AbsTwitchFollowHandler):
            raise TypeError(f'twitchFollowHandler argument is malformed: \"{twitchFollowHandler}\"')
        elif twitchHypeTrainHandler is not None and not isinstance(twitchHypeTrainHandler, AbsTwitchHypeTrainHandler):
            raise TypeError(f'twitchHypeTrainHandler argument is malformed: \"{twitchHypeTrainHandler}\"')
        elif twitchPollHandler is not None and not isinstance(twitchPollHandler, AbsTwitchPollHandler):
            raise TypeError(f'twitchPollHandler argument is malformed: \"{twitchPollHandler}\"')
        elif twitchPredictionHandler is not None and not isinstance(twitchPredictionHandler, AbsTwitchPredictionHandler):
            raise TypeError(f'twitchPredictionHandler argument is malformed: \"{twitchPredictionHandler}\"')
        elif twitchRaidHandler is not None and not isinstance(twitchRaidHandler, AbsTwitchRaidHandler):
            raise TypeError(f'twitchRaidHandler argument is malformed: \"{twitchRaidHandler}\"')
        elif twitchSubscriptionHandler is not None and not isinstance(twitchSubscriptionHandler, AbsTwitchSubscriptionHandler):
            raise TypeError(f'twitchSubscriptionHandler argument is malformed: \"{twitchSubscriptionHandler}\"')
        elif not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif additionalTriviaAnswersRepository is not None and not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(addOrRemoveUserDataHelper, AddOrRemoveUserDataHelperInterface):
            raise TypeError(f'addOrRemoveUserDataHelper argument is malformed: \"{addOrRemoveUserDataHelper}\"')
        elif airStrikeCheerActionHelper is not None and not isinstance(airStrikeCheerActionHelper, AirStrikeCheerActionHelperInterface):
            raise TypeError(f'airStrikeCheerActionHelper argument is malformed: \"{airStrikeCheerActionHelper}\"')
        elif not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif anivCopyMessageTimeoutScoreHelper is not None and not isinstance(anivCopyMessageTimeoutScoreHelper, AnivCopyMessageTimeoutScoreHelperInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreHelper argument is malformed: \"{anivCopyMessageTimeoutScoreHelper}\"')
        elif anivCopyMessageTimeoutScorePresenter is not None and not isinstance(anivCopyMessageTimeoutScorePresenter, AnivCopyMessageTimeoutScorePresenterInterface):
            raise TypeError(f'anivCopyMessageTimeoutScorePresenter argument is malformed: \"{anivCopyMessageTimeoutScorePresenter}\"')
        elif anivSettings is not None and not isinstance(anivSettings, AnivSettingsInterface):
            raise TypeError(f'anivSettings argument is malformed: \"{anivSettings}\"')
        elif asplodieStatsPresenter is not None and not isinstance(asplodieStatsPresenter, AsplodieStatsPresenter):
            raise TypeError(f'asplodieStatsPresenter argument is malformed: \"{asplodieStatsPresenter}\"')
        elif asplodieStatsRepository is not None and not isinstance(asplodieStatsRepository, AsplodieStatsRepositoryInterface):
            raise TypeError(f'asplodieStatsRepository argument is malformed: \"{asplodieStatsRepository}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise TypeError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif bannedTriviaGameControllersRepository is not None and not isinstance(bannedTriviaGameControllersRepository, BannedTriviaGameControllersRepositoryInterface):
            raise TypeError(f'bannedTriviaGameControllersRepository argument is malformed: \"{bannedTriviaGameControllersRepository}\"')
        elif bannedWordsRepository is not None and not isinstance(bannedWordsRepository, BannedWordsRepositoryInterface):
            raise TypeError(f'bannedWordsRepository argument is malformed: \"{bannedWordsRepository}\"')
        elif beanChanceCheerActionHelper is not None and not isinstance(beanChanceCheerActionHelper, BeanChanceCheerActionHelperInterface):
            raise TypeError(f'beanChanceCheerActionHelper argument is malformed: \"{beanChanceCheerActionHelper}\"')
        elif beanStatsPresenter is not None and not isinstance(beanStatsPresenter, BeanStatsPresenterInterface):
            raise TypeError(f'beanStatsPresenter argument is malformed: \"{beanStatsPresenter}\"')
        elif beanStatsRepository is not None and not isinstance(beanStatsRepository, BeanStatsRepositoryInterface):
            raise TypeError(f'beanStatsRepository argument is malformed: \"{beanStatsRepository}\"')
        elif bizhawkSettingsRepository is not None and not isinstance(bizhawkSettingsRepository, BizhawkSettingsRepositoryInterface):
            raise TypeError(f'bizhawkSettingsRepository argument is malformed: \"{bizhawkSettingsRepository}\"')
        elif chatActionsManager is not None and not isinstance(chatActionsManager, ChatActionsManagerInterface):
            raise TypeError(f'chatActionsManager argument is malformed: \"{chatActionsManager}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif chatterInventoryHelper is not None and not isinstance(chatterInventoryHelper, ChatterInventoryHelperInterface):
            raise TypeError(f'chatterInventoryHelper argument is malformed: \"{chatterInventoryHelper}\"')
        elif chatterInventoryIdGenerator is not None and not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif chatterInventoryItemUseMachine is not None and not isinstance(chatterInventoryItemUseMachine, ChatterInventoryItemUseMachineInterface):
            raise TypeError(f'chatterInventoryItemUseMachine argument is malformed: \"{chatterInventoryItemUseMachine}\"')
        elif chatterInventoryMapper is not None and not isinstance(chatterInventoryMapper, ChatterInventoryMapperInterface):
            raise TypeError(f'chatterInventoryMapper argument is malformed: \"{chatterInventoryMapper}\"')
        elif chatterInventorySettings is not None and not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif chatterItemEventHandler is not None and not isinstance(chatterItemEventHandler, AbsChatterItemEventHandler):
            raise TypeError(f'chatterItemEventHandler argument is malformed: \"{chatterItemEventHandler}\"')
        elif chatterPreferredNameHelper is not None and not isinstance(chatterPreferredNameHelper, ChatterPreferredNameHelperInterface):
            raise TypeError(f'chatterPreferredNameHelper argument is malformed: \"{chatterPreferredNameHelper}\"')
        elif chatterPreferredNameRepository is not None and not isinstance(chatterPreferredNameRepository, ChatterPreferredNameRepositoryInterface):
            raise TypeError(f'chatterPreferredNameRepository argument is malformed: \"{chatterPreferredNameRepository}\"')
        elif chatterPreferredNameSettings is not None and not isinstance(chatterPreferredNameSettings, ChatterPreferredNameSettingsInterface):
            raise TypeError(f'chatterPreferredNameSettings argument is malformed: \"{chatterPreferredNameSettings}\"')
        elif chatterPreferredTtsHelper is not None and not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif chatterPreferredTtsPresenter is not None and not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif chatterPreferredTtsRepository is not None and not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif chatterPreferredTtsSettingsRepository is not None and not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif chatterPreferredTtsUserMessageHelper is not None and not isinstance(chatterPreferredTtsUserMessageHelper, ChatterPreferredTtsUserMessageHelperInterface):
            raise TypeError(f'chatterPreferredTtsUserMessageHelper argument is malformed: \"{chatterPreferredTtsUserMessageHelper}\"')
        elif cheerActionHelper is not None and not isinstance(cheerActionHelper, CheerActionHelperInterface):
            raise TypeError(f'cheerActionHelper argument is malformed: \"{cheerActionHelper}\"')
        elif cheerActionJsonMapper is not None and not isinstance(cheerActionJsonMapper, CheerActionJsonMapperInterface):
            raise TypeError(f'cheerActionJsonMapper argument is malformed: \"{cheerActionJsonMapper}\"')
        elif cheerActionSettingsRepository is not None and not isinstance(cheerActionSettingsRepository, CheerActionSettingsRepositoryInterface):
            raise TypeError(f'cheerActionSettingsRepository argument is malformed: \"{cheerActionSettingsRepository}\"')
        elif cheerActionsRepository is not None and not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif cheerActionsWizard is not None and not isinstance(cheerActionsWizard, CheerActionsWizardInterface):
            raise TypeError(f'cheerActionsWizard argument is malformed: \"{cheerActionsWizard}\"')
        elif commodoreSamSettingsRepository is not None and not isinstance(commodoreSamSettingsRepository, CommodoreSamSettingsRepositoryInterface):
            raise TypeError(f'commodoreSamSettingsRepository argument is malformed: \"{commodoreSamSettingsRepository}\"')
        elif not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif crowdControlActionHandler is not None and not isinstance(crowdControlActionHandler, CrowdControlActionHandler):
            raise TypeError(f'crowdControlActionHandler argument is malformed: \"{crowdControlActionHandler}\"')
        elif crowdControlAutomator is not None and not isinstance(crowdControlAutomator, CrowdControlAutomatorInterface):
            raise TypeError(f'crowdControlAutomator argument is malformed: \"{crowdControlAutomator}\"')
        elif crowdControlIdGenerator is not None and not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif crowdControlMachine is not None and not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif crowdControlMessageListener is not None and not isinstance(crowdControlMessageListener, CrowdControlMessageListener):
            raise TypeError(f'crowdControlMessageListener argument is malformed: \"{crowdControlMessageListener}\"')
        elif crowdControlSettingsRepository is not None and not isinstance(crowdControlSettingsRepository, CrowdControlSettingsRepositoryInterface):
            raise TypeError(f'crowdControlSettingsRepository argument is malformed: \"{crowdControlSettingsRepository}\"')
        elif crowdControlUserInputUtils is not None and not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils argument is malformed: \"{crowdControlUserInputUtils}\"')
        elif cutenessPresenter is not None and not isinstance(cutenessPresenter, CutenessPresenterInterface):
            raise TypeError(f'cutenessPresenter argument is malformed: \"{cutenessPresenter}\"')
        elif cutenessRepository is not None and not isinstance(cutenessRepository, CutenessRepositoryInterface):
            raise TypeError(f'cutenessRepository argument is malformed: \"{cutenessRepository}\"')
        elif cutenessUtils is not None and not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise TypeError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif decTalkSettingsRepository is not None and not isinstance(decTalkSettingsRepository, DecTalkSettingsRepositoryInterface):
            raise TypeError(f'decTalkSettingsRepository argument is malformed: \"{decTalkSettingsRepository}\"')
        elif eccoHelper is not None and not isinstance(eccoHelper, EccoHelperInterface):
            raise TypeError(f'eccoHelper argument is malformed: \"{eccoHelper}\"')
        elif funtoonHelper is not None and not isinstance(funtoonHelper, FuntoonHelperInterface):
            raise TypeError(f'funtoonHelper argument is malformed: \"{funtoonHelper}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif googleSettingsRepository is not None and not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif guaranteedTimeoutUsersRepository is not None and not isinstance(guaranteedTimeoutUsersRepository, GuaranteedTimeoutUsersRepositoryInterface):
            raise TypeError(f'guaranteedTimeoutUsersRepository argument is malformed: \"{guaranteedTimeoutUsersRepository}\"')
        elif halfLifeSettingsRepository is not None and not isinstance(halfLifeSettingsRepository, HalfLifeSettingsRepositoryInterface):
            raise TypeError(f'halfLifeSettingsRepository argument is malformed: \"{halfLifeSettingsRepository}\"')
        elif isLiveOnTwitchRepository is not None and not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif jishoHelper is not None and not isinstance(jishoHelper, JishoHelperInterface):
            raise TypeError(f'jishoHelper argument is malformed: \"{jishoHelper}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif locationsRepository is not None and not isinstance(locationsRepository, LocationsRepositoryInterface):
            raise TypeError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif microsoftSamSettingsRepository is not None and not isinstance(microsoftSamSettingsRepository, MicrosoftSamSettingsRepositoryInterface):
            raise TypeError(f'microsoftSamSettingsRepository argument is malformed: \"{microsoftSamSettingsRepository}\"')
        elif mostRecentAnivMessageRepository is not None and not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif mostRecentAnivMessageTimeoutHelper is not None and not isinstance(mostRecentAnivMessageTimeoutHelper, MostRecentAnivMessageTimeoutHelperInterface):
            raise TypeError(f'mostRecentAnivMessageTimeoutHelper argument is malformed: \"{mostRecentAnivMessageTimeoutHelper}\"')
        elif mostRecentChatsRepository is not None and not isinstance(mostRecentChatsRepository, MostRecentChatsRepositoryInterface):
            raise TypeError(f'mostRecentChatsRepository argument is malformed: \"{mostRecentChatsRepository}\"')
        elif openTriviaDatabaseSessionTokenRepository is not None and not isinstance(openTriviaDatabaseSessionTokenRepository, OpenTriviaDatabaseSessionTokenRepositoryInterface):
            raise TypeError(f'openTriviaDatabaseSessionTokenRepository argument is malformed: \"{openTriviaDatabaseSessionTokenRepository}\"')
        elif pixelsDiceEventListener is not None and not isinstance(pixelsDiceEventListener, PixelsDiceEventListener):
            raise TypeError(f'pixelsDiceEventListener argument is malformed: \"{pixelsDiceEventListener}\"')
        elif pixelsDiceMachine is not None and not isinstance(pixelsDiceMachine, PixelsDiceMachineInterface):
            raise TypeError(f'pixelsDiceMachine argument is malformed:\"{pixelsDiceMachine}\"')
        elif pokepediaRepository is not None and not isinstance(pokepediaRepository, PokepediaRepositoryInterface):
            raise TypeError(f'pokepediaRepository argument is malformed: \"{pokepediaRepository}\"')
        elif psqlCredentialsProvider is not None and not isinstance(psqlCredentialsProvider, PsqlCredentialsProviderInterface):
            raise TypeError(f'psqlCredentialsProvider argument is malformed: \"{psqlCredentialsProvider}\"')
        elif recurringActionsEventHandler is not None and not isinstance(recurringActionsEventHandler, AbsRecurringActionsEventHandler):
            raise TypeError(f'recurringActionsEventHandler argument is malformed: \"{recurringActionsEventHandler}\"')
        elif recurringActionsHelper is not None and not isinstance(recurringActionsHelper, RecurringActionsHelperInterface):
            raise TypeError(f'recurringActionsHelper argument is malformed: \"{recurringActionsHelper}\"')
        elif recurringActionsMachine is not None and not isinstance(recurringActionsMachine, RecurringActionsMachineInterface):
            raise TypeError(f'recurringActionsMachine argument is malformed: \"{recurringActionsMachine}\"')
        elif recurringActionsRepository is not None and not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif recurringActionsWizard is not None and not isinstance(recurringActionsWizard, RecurringActionsWizardInterface):
            raise TypeError(f'recurringActionsWizard argument is malformed: \"{recurringActionsWizard}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif shinyTriviaOccurencesRepository is not None and not isinstance(shinyTriviaOccurencesRepository, ShinyTriviaOccurencesRepositoryInterface):
            raise TypeError(f'shinyTriviaOccurencesRepository argument is malformed: \"{shinyTriviaOccurencesRepository}\"')
        elif soundPlayerManagerProvider is not None and not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif soundPlayerRandomizerHelper is not None and not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif soundPlayerSettingsRepository is not None and not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise TypeError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif starWarsQuotesRepository is not None and not isinstance(starWarsQuotesRepository, StarWarsQuotesRepositoryInterface):
            raise TypeError(f'starWarsQuotesRepository argument is malformed: \"{starWarsQuotesRepository}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif streamAlertsSettingsRepository is not None and not isinstance(streamAlertsSettingsRepository, StreamAlertsSettingsRepositoryInterface):
            raise TypeError(f'streamAlertsSettingsRepository argument is malformed: \"{streamAlertsSettingsRepository}\"')
        elif streamElementsSettingsRepository is not None and not isinstance(streamElementsSettingsRepository, StreamElementsSettingsRepositoryInterface):
            raise TypeError(f'streamElementsSettingsRepository argument is malformed: \"{streamElementsSettingsRepository}\"')
        elif streamElementsUserKeyRepository is not None and not isinstance(streamElementsUserKeyRepository, StreamElementsUserKeyRepositoryInterface):
            raise TypeError(f'streamElementsUserKeyRepository argument is malformed: \"{streamElementsUserKeyRepository}\"')
        elif supStreamerRepository is not None and not isinstance(supStreamerRepository, SupStreamerRepositoryInterface):
            raise TypeError(f'supStreamerRepository argument is malformed: \"{supStreamerRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif timeoutActionMachine is not None and not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif timeoutActionSettings is not None and not isinstance(timeoutActionSettings, TimeoutActionSettingsInterface):
            raise TypeError(f'timeoutActionSettings argument is malformed: \"{timeoutActionSettings}\"')
        elif timeoutEventHandler is not None and not isinstance(timeoutEventHandler, AbsTimeoutEventHandler):
            raise TypeError(f'timeoutEventHandler argument is malformed: \"{timeoutEventHandler}\"')
        elif timeoutImmuneUserIdsRepository is not None and not isinstance(timeoutImmuneUserIdsRepository, TimeoutImmuneUserIdsRepositoryInterface):
            raise TypeError(f'timeoutImmuneUserIdsRepository argument is malformed: \"{timeoutImmuneUserIdsRepository}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif toxicTriviaOccurencesRepository is not None and not isinstance(toxicTriviaOccurencesRepository, ToxicTriviaOccurencesRepositoryInterface):
            raise TypeError(f'toxicTriviaOccurencesRepository argument is malformed: \"{toxicTriviaOccurencesRepository}\"')
        elif translationHelper is not None and not isinstance(translationHelper, TranslationHelperInterface):
            raise TypeError(f'translationHelper argument is malformed: \"{translationHelper}\"')
        elif triviaBanHelper is not None and not isinstance(triviaBanHelper, TriviaBanHelperInterface):
            raise TypeError(f'triviaBanHelper argument is malformed: \"{triviaBanHelper}\"')
        elif triviaEmoteGenerator is not None and not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise TypeError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif triviaEventHandler is not None and not isinstance(triviaEventHandler, AbsTriviaEventHandler):
            raise TypeError(f'triviaEventHandler argument is malformed: \"{triviaEventHandler}\"')
        elif triviaGameBuilder is not None and not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif triviaGameControllersRepository is not None and not isinstance(triviaGameControllersRepository, TriviaGameControllersRepositoryInterface):
            raise TypeError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif triviaGameGlobalControllersRepository is not None and not isinstance(triviaGameGlobalControllersRepository, TriviaGameGlobalControllersRepositoryInterface):
            raise TypeError(f'triviaGameGlobalControllersRepository argument is malformed: \"{triviaGameGlobalControllersRepository}\"')
        elif triviaGameMachine is not None and not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif triviaHistoryRepository is not None and not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise TypeError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif triviaIdGenerator is not None and not isinstance(triviaIdGenerator, TriviaIdGeneratorInterface):
            raise TypeError(f'triviaIdGenerator argument is malformed: \"{triviaIdGenerator}\"')
        elif triviaQuestionOccurrencesRepository is not None and not isinstance(triviaQuestionOccurrencesRepository, TriviaQuestionOccurrencesRepositoryInterface):
            raise TypeError(f'triviaQuestionOccurrencesRepository argument is malformed: \"{triviaQuestionOccurrencesRepository}\"')
        elif triviaRepository is not None and not isinstance(triviaRepository, TriviaRepositoryInterface):
            raise TypeError(f'triviaRepository argument is malformed: \"{triviaRepository}\"')
        elif triviaScoreRepository is not None and not isinstance(triviaScoreRepository, TriviaScoreRepositoryInterface):
            raise TypeError(f'triviaScoreRepository argument is malformed: \"{triviaScoreRepository}\"')
        elif triviaSettingsRepository is not None and not isinstance(triviaSettingsRepository, TriviaSettingsRepositoryInterface):
            raise TypeError(f'triviaSettingsRepository argument is malformed: \"{triviaSettingsRepository}\"')
        elif triviaTwitchEmoteHelper is not None and not isinstance(triviaTwitchEmoteHelper, TriviaTwitchEmoteHelperInterface):
            raise TypeError(f'triviaTwitchEmoteHelper argument is malformed: \"{triviaTwitchEmoteHelper}\"')
        elif triviaUtils is not None and not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif trollmojiHelper is not None and not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif trollmojiSettingsRepository is not None and not isinstance(trollmojiSettingsRepository, TrollmojiSettingsRepositoryInterface):
            raise TypeError(f'trollmojiSettingsRepository argument is malformed: \"{trollmojiSettingsRepository}\"')
        elif ttsChatterRepository is not None and not isinstance(ttsChatterRepository, TtsChatterRepositoryInterface):
            raise TypeError(f'ttsChatterRepository argument is malformed: \"{ttsChatterRepository}\"')
        elif ttsChatterSettingsRepository is not None and not isinstance(ttsChatterSettingsRepository, TtsChatterSettingsRepositoryInterface):
            raise TypeError(f'ttsChatterSettingsRepository argument is malformed: \"{ttsChatterSettingsRepository}\"')
        elif ttsJsonMapper is not None and not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif ttsMonsterSettingsRepository is not None and not isinstance(ttsMonsterSettingsRepository, TtsMonsterSettingsRepositoryInterface):
            raise TypeError(f'ttsMonsterSettingsRepository argument is malformed: \"{ttsMonsterSettingsRepository}\"')
        elif ttsMonsterTokensRepository is not None and not isinstance(ttsMonsterTokensRepository, TtsMonsterTokensRepositoryInterface):
            raise TypeError(f'ttsMonsterTokensRepository argument is malformed: \"{ttsMonsterTokensRepository}\"')
        elif ttsSettingsRepository is not None and not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')
        elif not isinstance(twitchChannelJoinHelper, TwitchChannelJoinHelperInterface):
            raise TypeError(f'twitchChannelJoinHelper argument is malformed: \"{twitchChannelJoinHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchConfiguration, TwitchConfiguration):
            raise TypeError(f'twitchConfiguration argument is malformed: \"{twitchConfiguration}\"')
        elif not isinstance(twitchEmotesHelper, TwitchEmotesHelperInterface):
            raise TypeError(f'twitchEmotesHelper argument is malformed: \"{twitchEmotesHelper}\"')
        elif twitchFollowingStatusRepository is not None and not isinstance(twitchFollowingStatusRepository, TwitchFollowingStatusRepositoryInterface):
            raise TypeError(f'twitchFollowingStatusRepository argument is malformed: \"{twitchFollowingStatusRepository}\"')
        elif twitchFriendsUserIdRepository is not None and not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not isinstance(twitchIrcReconnectHelper, TwitchIrcReconnectHelperInterface):
            raise TypeError(f'twitchIrcReconnectHelper argument is malformed: \"{twitchIrcReconnectHelper}\"')
        elif twitchMessageStringUtils is not None and not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise TypeError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif twitchSubscriptionsRepository is not None and not isinstance(twitchSubscriptionsRepository, TwitchSubscriptionsRepositoryInterface):
            raise TypeError(f'twitchSubscriptionsRepository argument is malformed: \"{twitchSubscriptionsRepository}\"')
        elif twitchTimeoutHelper is not None and not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif twitchTimeoutRemodHelper is not None and not isinstance(twitchTimeoutRemodHelper, TwitchTimeoutRemodHelperInterface):
            raise TypeError(f'twitchTimeoutRemodHelper argument is malformed: \"{twitchTimeoutRemodHelper}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif twitchWebsocketClient is not None and not isinstance(twitchWebsocketClient, TwitchWebsocketClientInterface):
            raise TypeError(f'twitchWebsocketClient argument is malformed: \"{twitchWebsocketClient}\"')
        elif twitchWebsocketSettingsRepository is not None and not isinstance(twitchWebsocketSettingsRepository, TwitchWebsocketSettingsRepositoryInterface):
            raise TypeError(f'twitchWebsocketSettingsRepository argument is malformed: \"{twitchWebsocketSettingsRepository}\"')
        elif useChatterItemHelper is not None and not isinstance(useChatterItemHelper, UseChatterItemHelperInterface):
            raise TypeError(f'useChatterItemHelper argument is malformed: \"{useChatterItemHelper}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif voicemailHelper is not None and not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif voicemailsRepository is not None and not isinstance(voicemailsRepository, VoicemailsRepositoryInterface):
            raise TypeError(f'voicemailsRepository argument is malformed: \"{voicemailsRepository}\"')
        elif voicemailSettingsRepository is not None and not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')
        elif weatherReportPresenter is not None and not isinstance(weatherReportPresenter, WeatherReportPresenterInterface):
            raise TypeError(f'weatherReportPresenter argument is malformed: \"{weatherReportPresenter}\"')
        elif weatherRepository is not None and not isinstance(weatherRepository, WeatherRepositoryInterface):
            raise TypeError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')
        elif wordOfTheDayPresenter is not None and not isinstance(wordOfTheDayPresenter, WordOfTheDayPresenterInterface):
            raise TypeError(f'wordOfTheDayPresenter argument is malformed: \"{wordOfTheDayPresenter}\"')
        elif wordOfTheDayRepository is not None and not isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface):
            raise TypeError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')

        self.__twitchChannelPointRedemptionHandler: Final[AbsTwitchChannelPointRedemptionHandler | None] = twitchChannelPointRedemptionHandler
        self.__twitchChatHandler: Final[AbsTwitchChatHandler | None] = twitchChatHandler
        self.__twitchCheerHandler: Final[AbsTwitchCheerHandler | None] = twitchCheerHandler
        self.__twitchFollowHandler: Final[AbsTwitchFollowHandler | None] = twitchFollowHandler
        self.__twitchHypeTrainHandler: Final[AbsTwitchHypeTrainHandler | None] = twitchHypeTrainHandler
        self.__twitchPollHandler: Final[AbsTwitchPollHandler | None] = twitchPollHandler
        self.__twitchPredictionHandler: Final[AbsTwitchPredictionHandler | None] = twitchPredictionHandler
        self.__twitchRaidHandler: Final[AbsTwitchRaidHandler | None] = twitchRaidHandler
        self.__twitchSubscriptionHandler: Final[AbsTwitchSubscriptionHandler | None] = twitchSubscriptionHandler
        self.__addOrRemoveUserDataHelper: Final[AddOrRemoveUserDataHelperInterface] = addOrRemoveUserDataHelper
        self.__airStrikeCheerActionHelper: Final[AirStrikeCheerActionHelperInterface | None] = airStrikeCheerActionHelper
        self.__authRepository: Final[AuthRepository] = authRepository
        self.__beanChanceCheerActionHelper: Final[BeanChanceCheerActionHelperInterface | None] = beanChanceCheerActionHelper
        self.__chatActionsManager: Final[ChatActionsManagerInterface | None] = chatActionsManager
        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__chatterInventoryItemUseMachine: Final[ChatterInventoryItemUseMachineInterface | None] = chatterInventoryItemUseMachine
        self.__chatterItemEventHandler: Final[AbsChatterItemEventHandler | None] = chatterItemEventHandler
        self.__crowdControlActionHandler: Final[CrowdControlActionHandler | None] = crowdControlActionHandler
        self.__crowdControlMachine: Final[CrowdControlMachineInterface | None] = crowdControlMachine
        self.__crowdControlMessageListener: Final[CrowdControlMessageListener | None] = crowdControlMessageListener
        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__mostRecentAnivMessageTimeoutHelper: Final[MostRecentAnivMessageTimeoutHelperInterface | None] = mostRecentAnivMessageTimeoutHelper
        self.__pixelsDiceEventListener: Final[PixelsDiceEventListener | None] = pixelsDiceEventListener
        self.__pixelsDiceMachine: Final[PixelsDiceMachineInterface | None] = pixelsDiceMachine
        self.__recurringActionsEventHandler: Final[AbsRecurringActionsEventHandler | None] = recurringActionsEventHandler
        self.__recurringActionsMachine: Final[RecurringActionsMachineInterface | None] = recurringActionsMachine
        self.__sentMessageLogger: Final[SentMessageLoggerInterface] = sentMessageLogger
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface | None] = timeoutActionMachine
        self.__timeoutEventHandler: Final[AbsTimeoutEventHandler | None] = timeoutEventHandler
        self.__triviaEventHandler: Final[AbsTriviaEventHandler | None] = triviaEventHandler
        self.__triviaGameMachine: TriviaGameMachineInterface | None = triviaGameMachine
        self.__triviaRepository: TriviaRepositoryInterface | None = triviaRepository
        self.__ttsChatterRepository: Final[TtsChatterRepositoryInterface | None] = ttsChatterRepository
        self.__twitchChannelJoinHelper: Final[TwitchChannelJoinHelperInterface] = twitchChannelJoinHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchConfiguration: Final[TwitchConfiguration] = twitchConfiguration
        self.__twitchIrcReconnectHelper: Final[TwitchIrcReconnectHelperInterface] = twitchIrcReconnectHelper
        self.__twitchTimeoutRemodHelper: TwitchTimeoutRemodHelperInterface | None = twitchTimeoutRemodHelper
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__twitchWebsocketClient: Final[TwitchWebsocketClientInterface | None] = twitchWebsocketClient
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__websocketConnectionServer: Final[WebsocketConnectionServerInterface | None] = websocketConnectionServer

        #######################################
        ## Initialization of command objects ##
        #######################################

        self.__addUserCommand: AbsChatCommand = AddUserChatCommand(addOrRemoveUserDataHelper, administratorProvider, timber, twitchTokensRepository, twitchChatMessenger, userIdsRepository, usersRepository)
        self.__blueSkyCommand: AbsChatCommand = BlueSkyChatCommand(timber, twitchChatMessenger, usersRepository)
        self.__clearCachesCommand: AbsChatCommand = ClearCachesChatCommand(addOrRemoveUserDataHelper, administratorProvider, anivSettings, asplodieStatsRepository, authRepository, bannedTriviaGameControllersRepository, bannedWordsRepository, bizhawkSettingsRepository, chatterPreferredTtsRepository, chatterPreferredTtsSettingsRepository, cheerActionSettingsRepository, cheerActionsRepository, commodoreSamSettingsRepository, crowdControlSettingsRepository, decTalkSettingsRepository, funtoonTokensRepository, generalSettingsRepository, googleSettingsRepository, guaranteedTimeoutUsersRepository, halfLifeSettingsRepository, isLiveOnTwitchRepository, locationsRepository, microsoftSamSettingsRepository, mostRecentAnivMessageRepository, mostRecentChatsRepository, openTriviaDatabaseSessionTokenRepository, psqlCredentialsProvider, soundPlayerRandomizerHelper, soundPlayerSettingsRepository, streamAlertsSettingsRepository, streamElementsSettingsRepository, streamElementsUserKeyRepository, supStreamerRepository, timber, timeoutActionSettings, triviaGameControllersRepository, triviaGameGlobalControllersRepository, triviaSettingsRepository, trollmojiHelper, trollmojiSettingsRepository, ttsChatterRepository, ttsChatterSettingsRepository, ttsMonsterSettingsRepository, ttsMonsterTokensRepository, ttsSettingsRepository, twitchChannelEditorsRepository, twitchEmotesHelper, twitchFollowingStatusRepository, twitchSubscriptionsRepository, twitchTokensRepository, twitchChatMessenger, twitchWebsocketSettingsRepository, userIdsRepository, usersRepository, voicemailsRepository, voicemailSettingsRepository, weatherRepository, wordOfTheDayRepository)
        self.__commandsCommand: AbsChatCommand = CommandsChatCommand(timber, twitchChatMessenger, usersRepository)
        self.__confirmCommand: AbsChatCommand = ConfirmChatCommand(addOrRemoveUserDataHelper, administratorProvider, timber, twitchChatMessenger, usersRepository)
        self.__cynanSourceCommand: AbsChatCommand = CynanSourceChatCommand(timber, twitchChatMessenger, usersRepository)
        self.__discordCommand: AbsChatCommand = DiscordChatCommand(timber, twitchChatMessenger, usersRepository)
        self.__loremIpsumCommand: AbsChatCommand = LoremIpsumChatCommand(administratorProvider, timber, twitchChatMessenger, usersRepository)
        self.__removeUserCommand: AbsChatCommand = RemoveUserChatCommand(addOrRemoveUserDataHelper, administratorProvider, timber, twitchTokensRepository, twitchUtils, userIdsRepository, usersRepository)
        self.__setTwitchCodeCommand: AbsChatCommand = SetTwitchCodeChatCommand(administratorProvider, timber, twitchTokensRepository, twitchUtils, usersRepository)
        self.__skipTtsCommand: AbsChatCommand = SkipTtsChatCommand(administratorProvider, compositeTtsManagerProvider, timber, twitchChannelEditorsRepository)
        self.__timeCommand: AbsChatCommand = TimeChatCommand(timber, twitchChatMessenger, usersRepository)
        self.__twitchUserInfoCommand: AbsChatCommand = TwitchUserInfoChatCommand(administratorProvider, timber, twitchApiService, twitchChatMessenger, authRepository, twitchTokensRepository, userIdsRepository, usersRepository)

        if asplodieStatsPresenter is None or asplodieStatsRepository is None:
            self.__asplodieStatsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__asplodieStatsCommand: AbsChatCommand = AsplodieStatsChatCommand(asplodieStatsPresenter, asplodieStatsRepository, timber, twitchChatMessenger, userIdsRepository, usersRepository)

        if beanStatsPresenter is None or beanStatsRepository is None:
            self.__beanStatsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__beanStatsCommand: AbsChatCommand = BeanStatsChatCommand(beanStatsPresenter, beanStatsRepository, timber, twitchUtils, userIdsRepository, usersRepository)

        if chatterInventoryHelper is None or chatterInventoryIdGenerator is None or chatterInventoryItemUseMachine is None or chatterInventoryMapper is None or chatterInventorySettings is None or useChatterItemHelper is None:
            self.__chatterInventoryCommand: AbsChatCommand = StubChatCommand()
            self.__freeGiveChatterItemCommand: AbsChatCommand = StubChatCommand()
            self.__giveChatterItemCommand: AbsChatCommand = StubChatCommand()
            self.__useChatterItemCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__chatterInventoryCommand: AbsChatCommand = ChatterInventoryChatCommand(chatterInventoryHelper, chatterInventorySettings, timber, twitchChatMessenger, usersRepository)
            self.__freeGiveChatterItemCommand: AbsChatCommand = FreeGiveChatterItemChatCommand(administratorProvider, chatterInventoryHelper, chatterInventoryMapper, chatterInventorySettings, timber, twitchChannelEditorsRepository, twitchChatMessenger, twitchTokensUtils, userIdsRepository, usersRepository)
            self.__giveChatterItemCommand: AbsChatCommand = GiveChatterItemChatCommand(chatterInventoryIdGenerator, chatterInventoryItemUseMachine, chatterInventoryMapper, chatterInventorySettings, timber, twitchChatMessenger, twitchTokensUtils, userIdsRepository, usersRepository)
            self.__useChatterItemCommand: AbsChatCommand = UseChatterItemChatCommand(chatterInventoryIdGenerator, timber, twitchChatMessenger, useChatterItemHelper, usersRepository)

        if cheerActionJsonMapper is None or cheerActionsRepository is None or cheerActionsWizard is None:
            self.__addCrowdControlCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__addGameShuffleCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__addItemUseCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__addSoundAlertCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__addVoicemailCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__beanInstructionsCommand: AbsChatCommand = StubChatCommand()
            self.__deleteCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__disableCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__enableCheerActionCommand: AbsChatCommand = StubChatCommand()
            self.__getCheerActionsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__addCrowdControlCheerActionCommand: AbsChatCommand = AddCrowdControlCheerActionChatCommand(administratorProvider, cheerActionsWizard, timber, twitchChatMessenger, usersRepository)
            self.__addGameShuffleCheerActionCommand: AbsChatCommand = AddGameShuffleCheerActionChatCommand(administratorProvider, cheerActionsWizard, timber, twitchChatMessenger, usersRepository)
            self.__addItemUseCheerActionCommand: AbsChatCommand = AddItemUseCheerActionChatCommand(administratorProvider, cheerActionsWizard, timber, twitchChatMessenger, usersRepository)
            self.__addSoundAlertCheerActionCommand: AbsChatCommand = AddSoundAlertCheerActionCommand(administratorProvider, cheerActionsWizard, timber, twitchChatMessenger, usersRepository)
            self.__addVoicemailCheerActionCommand: AbsChatCommand = AddVoicemailCheerActionCommand(administratorProvider, cheerActionsWizard, timber, twitchChatMessenger, usersRepository)
            self.__beanInstructionsCommand: AbsChatCommand = BeanInstructionsChatCommand(cheerActionsRepository, timber, twitchChatMessenger, usersRepository)
            self.__deleteCheerActionCommand: AbsChatCommand = DeleteCheerActionChatCommand(administratorProvider, cheerActionsRepository, timber, twitchChatMessenger, userIdsRepository, usersRepository)
            self.__disableCheerActionCommand: AbsChatCommand = DisableCheerActionChatCommand(administratorProvider, cheerActionsRepository, timber, twitchChatMessenger, usersRepository)
            self.__enableCheerActionCommand: AbsChatCommand = EnableCheerActionChatCommand(administratorProvider, cheerActionsRepository, timber, twitchChatMessenger, usersRepository)
            self.__getCheerActionsCommand: AbsChatCommand = GetCheerActionsChatCommand(administratorProvider, cheerActionsRepository, timber, twitchChatMessenger, usersRepository)

        if crowdControlAutomator is None or crowdControlIdGenerator is None or crowdControlMachine is None or crowdControlUserInputUtils is None:
            self.__addGameShuffleAutomatorCommand: AbsChatCommand = StubChatCommand()
            self.__crowdControlCommand: AbsChatCommand = StubChatCommand()
            self.__removeGameShuffleAutomatorCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__addGameShuffleAutomatorCommand: AbsChatCommand = AddGameShuffleAutomatorChatCommand(administratorProvider, crowdControlAutomator, timber, twitchChatMessenger, usersRepository)
            self.__crowdControlCommand: AbsChatCommand = CrowdControlChatCommand(administratorProvider, crowdControlIdGenerator, crowdControlMachine, crowdControlUserInputUtils, timber, timeZoneRepository, twitchChatMessenger, usersRepository)
            self.__removeGameShuffleAutomatorCommand: AbsChatCommand = RemoveGameShuffleAutomatorChatCommand(administratorProvider, crowdControlAutomator, timber, twitchChatMessenger, usersRepository)

        if recurringActionsHelper is None or recurringActionsMachine is None or recurringActionsRepository is None or recurringActionsWizard is None:
            self.__addRecurringCutenessActionCommand: AbsChatCommand = StubChatCommand()
            self.__addRecurringSuperTriviaActionCommand: AbsChatCommand = StubChatCommand()
            self.__addRecurringWeatherActionCommand: AbsChatCommand = StubChatCommand()
            self.__addRecurringWordOfTheDayActionCommand: AbsChatCommand = StubChatCommand()
            self.__getRecurringActionsCommand: AbsChatCommand = StubChatCommand()
            self.__removeRecurringCutenessActionCommand: AbsChatCommand = StubChatCommand()
            self.__removeRecurringSuperTriviaActionCommand: AbsChatCommand = StubChatCommand()
            self.__removeRecurringWeatherActionCommand: AbsChatCommand = StubChatCommand()
            self.__removeRecurringWordOfTheDayActionCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__addRecurringCutenessActionCommand: AbsChatCommand = AddRecurringCutenessActionChatCommand(administratorProvider, recurringActionsWizard, timber, twitchChatMessenger, usersRepository)
            self.__addRecurringSuperTriviaActionCommand: AbsChatCommand = AddRecurringSuperTriviaActionChatCommand(administratorProvider, recurringActionsWizard, timber, twitchChatMessenger, usersRepository)
            self.__addRecurringWeatherActionCommand: AbsChatCommand = AddRecurringWeatherActionChatCommand(administratorProvider, recurringActionsWizard, timber, twitchChatMessenger, usersRepository)
            self.__addRecurringWordOfTheDayActionCommand: AbsChatCommand = AddRecurringWordOfTheDayActionChatCommand(administratorProvider, recurringActionsWizard, timber, twitchChatMessenger, usersRepository)
            self.__getRecurringActionsCommand: AbsChatCommand = GetRecurringActionsChatCommand(administratorProvider, recurringActionsRepository, timber, twitchChatMessenger, usersRepository)
            self.__removeRecurringCutenessActionCommand: AbsChatCommand = RemoveRecurringCutenessActionChatCommand(administratorProvider, recurringActionsHelper, recurringActionsRepository, timber, twitchChatMessenger, usersRepository)
            self.__removeRecurringSuperTriviaActionCommand: AbsChatCommand = RemoveRecurringSuperTriviaActionCommand(administratorProvider, recurringActionsHelper, recurringActionsRepository, timber, twitchUtils, usersRepository)
            self.__removeRecurringWeatherActionCommand: AbsChatCommand = RemoveRecurringWeatherActionCommand(administratorProvider, recurringActionsHelper, recurringActionsRepository, timber, twitchUtils, usersRepository)
            self.__removeRecurringWordOfTheDayActionCommand: AbsChatCommand = RemoveRecurringWordOfTheDayActionCommand(administratorProvider, recurringActionsHelper, recurringActionsRepository, timber, twitchUtils, usersRepository)

        if bannedTriviaGameControllersRepository is None or triviaUtils is None:
            self.__addBannedTriviaControllerCommand: AbsChatCommand = StubChatCommand()
            self.__getBannedTriviaControllersCommand: AbsChatCommand = StubChatCommand()
            self.__removeBannedTriviaControllerCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__addBannedTriviaControllerCommand: AbsChatCommand = AddBannedTriviaControllerChatCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, twitchChatMessenger, authRepository, twitchTokensUtils, userIdsRepository, usersRepository)
            self.__getBannedTriviaControllersCommand: AbsChatCommand = GetBannedTriviaControllersChatCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, triviaUtils, twitchChatMessenger, usersRepository)
            self.__removeBannedTriviaControllerCommand: AbsChatCommand = RemoveBannedTriviaControllerChatCommand(administratorProvider, bannedTriviaGameControllersRepository, timber, twitchChatMessenger, authRepository, twitchTokensUtils, userIdsRepository, usersRepository)

        if chatterPreferredNameHelper is None or chatterPreferredNameRepository is None or chatterPreferredNameSettings is None:
            self.__getChatterPreferredNameCommand: AbsChatCommand = StubChatCommand()
            self.__removeChatterPreferredNameCommand: AbsChatCommand = StubChatCommand()
            self.__setChatterPreferredNameCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__getChatterPreferredNameCommand: AbsChatCommand = GetChatterPreferredNameChatCommand(chatterPreferredNameHelper, chatterPreferredNameSettings, timber, twitchChatMessenger)
            self.__removeChatterPreferredNameCommand: AbsChatCommand = RemoveChatterPreferredNameChatCommand(administratorProvider, chatterPreferredNameRepository, chatterPreferredNameSettings, timber, twitchChatMessenger, authRepository, twitchTokensUtils, userIdsRepository, usersRepository)
            self.__setChatterPreferredNameCommand: AbsChatCommand = SetChatterPreferredNameChatCommand(administratorProvider, chatterPreferredNameHelper, chatterPreferredNameSettings, timber, twitchChatMessenger, authRepository, twitchTokensUtils, userIdsRepository, usersRepository)

        if chatterPreferredTtsHelper is None or chatterPreferredTtsPresenter is None or chatterPreferredTtsRepository is None or chatterPreferredTtsSettingsRepository is None or chatterPreferredTtsUserMessageHelper is None or ttsJsonMapper is None:
            self.__getChatterPreferredTtsCommand: AbsChatCommand = StubChatCommand()
            self.__removeChatterPreferredTtsCommand: AbsChatCommand = StubChatCommand()
            self.__setChatterPreferredTtsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__getChatterPreferredTtsCommand: AbsChatCommand = GetChatterPreferredTtsChatCommand(chatterPreferredTtsPresenter, chatterPreferredTtsRepository, chatterPreferredTtsSettingsRepository, timber, twitchTokensUtils, twitchChatMessenger, userIdsRepository, usersRepository)
            self.__removeChatterPreferredTtsCommand: AbsChatCommand = RemoveChatterPreferredTtsChatCommand(chatterPreferredTtsPresenter, chatterPreferredTtsRepository, timber, twitchChatMessenger, usersRepository)
            self.__setChatterPreferredTtsCommand: AbsChatCommand = SetChatterPreferredTtsChatCommand(administratorProvider, chatterPreferredTtsHelper, chatterPreferredTtsPresenter, chatterPreferredTtsSettingsRepository, timber, ttsJsonMapper, authRepository, twitchTokensUtils, twitchChatMessenger, userIdsRepository, usersRepository)

        if additionalTriviaAnswersRepository is None or cutenessRepository is None or cutenessUtils is None or shinyTriviaOccurencesRepository is None or toxicTriviaOccurencesRepository is None or triviaBanHelper is None or triviaEmoteGenerator is None or triviaGameBuilder is None or triviaGameControllersRepository is None or triviaGameGlobalControllersRepository is None or triviaGameMachine is None or triviaHistoryRepository is None or triviaIdGenerator is None or triviaQuestionOccurrencesRepository is None or triviaScoreRepository is None or triviaSettingsRepository is None or triviaUtils is None:
            self.__addGlobalTriviaControllerCommand: AbsChatCommand = StubChatCommand()
            self.__addTriviaAnswerCommand: AbsChatCommand = StubChatCommand()
            self.__addTriviaControllerCommand: AbsChatCommand = StubChatCommand()
            self.__answerCommand: AbsChatCommand = StubChatCommand()
            self.__banTriviaQuestionCommand: AbsChatCommand = StubChatCommand()
            self.__clearSuperTriviaQueueCommand: AbsChatCommand = StubChatCommand()
            self.__deleteTriviaAnswersCommand: AbsChatCommand = StubChatCommand()
            self.__getGlobalTriviaControllersCommand: AbsChatCommand = StubChatCommand()
            self.__getTriviaAnswersCommand: AbsChatCommand = StubChatCommand()
            self.__getTriviaControllersCommand: AbsChatCommand = StubChatCommand()
            self.__removeTriviaControllerChatCommand: AbsChatCommand = StubChatCommand()
            self.__superAnswerCommand: AbsChatCommand = StubChatCommand()
            self.__superTriviaCommand: AbsChatCommand = StubChatCommand()
            self.__triviaInfoCommand: AbsChatCommand = StubChatCommand()
            self.__triviaScoreCommand: AbsChatCommand = StubChatCommand()
            self.__removeGlobalTriviaControllerChatCommand: AbsChatCommand = StubChatCommand()
            self.__unbanTriviaQuestionChatCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__addGlobalTriviaControllerCommand: AbsChatCommand = AddGlobalTriviaControllerChatCommand(administratorProvider, timber, triviaGameGlobalControllersRepository, twitchChatMessenger, authRepository, twitchTokensUtils, userIdsRepository, usersRepository)
            self.__addTriviaControllerCommand: AbsChatCommand = AddTriviaControllerChatCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, twitchChatMessenger, authRepository, twitchTokensUtils, userIdsRepository, usersRepository)
            self.__addTriviaAnswerCommand: AbsChatCommand = AddTriviaAnswerChatCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchChatMessenger, usersRepository)
            self.__answerCommand: AbsChatCommand = AnswerChatCommand(generalSettingsRepository, timber, triviaGameMachine, triviaIdGenerator, usersRepository)
            self.__banTriviaQuestionCommand: AbsChatCommand = BanTriviaQuestionChatCommand(generalSettingsRepository, timber, timeZoneRepository, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchChatMessenger, usersRepository)
            self.__clearSuperTriviaQueueCommand: AbsChatCommand = ClearSuperTriviaQueueChatCommand(generalSettingsRepository, timber, triviaGameMachine, triviaIdGenerator, triviaUtils, usersRepository)
            self.__deleteTriviaAnswersCommand: AbsChatCommand = DeleteTriviaAnswersChatCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchChatMessenger, usersRepository)
            self.__getGlobalTriviaControllersCommand: AbsChatCommand = GetGlobalTriviaControllersChatCommand(administratorProvider, generalSettingsRepository, timber, triviaGameGlobalControllersRepository, triviaUtils, twitchChatMessenger, usersRepository)
            self.__getTriviaAnswersCommand: AbsChatCommand = GetTriviaAnswersChatCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchChatMessenger, usersRepository)
            self.__getTriviaControllersCommand: AbsChatCommand = GetTriviaControllersChatCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, triviaUtils, twitchChatMessenger, usersRepository)
            self.__removeGlobalTriviaControllerChatCommand: AbsChatCommand = RemoveGlobalTriviaControllerChatCommand(administratorProvider, timber, triviaGameGlobalControllersRepository, twitchChatMessenger, authRepository, twitchTokensUtils, userIdsRepository, usersRepository)
            self.__removeTriviaControllerChatCommand: AbsChatCommand = RemoveTriviaControllerChatCommand(administratorProvider, generalSettingsRepository, timber, triviaGameControllersRepository, twitchChatMessenger, authRepository, twitchTokensUtils, userIdsRepository, usersRepository)
            self.__superAnswerCommand: AbsChatCommand = SuperAnswerChatCommand(generalSettingsRepository, timber, triviaGameMachine, triviaIdGenerator, usersRepository)
            self.__superTriviaCommand: AbsChatCommand = SuperTriviaChatCommand(generalSettingsRepository, timber, triviaGameBuilder, triviaGameMachine, triviaSettingsRepository, triviaUtils, twitchChatMessenger, usersRepository)
            self.__triviaInfoCommand: AbsChatCommand = TriviaInfoChatCommand(additionalTriviaAnswersRepository, generalSettingsRepository, timber, timeZoneRepository, triviaEmoteGenerator, triviaHistoryRepository, triviaQuestionOccurrencesRepository, triviaUtils, twitchChatMessenger, usersRepository)
            self.__triviaScoreCommand: AbsChatCommand = TriviaScoreChatCommand(generalSettingsRepository, shinyTriviaOccurencesRepository, timber, toxicTriviaOccurencesRepository, triviaScoreRepository, triviaUtils, twitchChatMessenger, userIdsRepository, usersRepository)
            self.__unbanTriviaQuestionChatCommand: AbsChatCommand = UnbanTriviaQuestionChatCommand(generalSettingsRepository, timber, triviaBanHelper, triviaEmoteGenerator, triviaHistoryRepository, triviaUtils, twitchUtils, usersRepository)

        if cutenessPresenter is None or cutenessRepository is None or cutenessUtils is None or triviaUtils is None:
            self.__cutenessCommand: AbsChatCommand = StubChatCommand()
            self.__cutenessChampionsCommand: AbsChatCommand = StubChatCommand()
            self.__cutenessHistoryCommand: AbsChatCommand = StubChatCommand()
            self.__giveCutenessCommand: AbsChatCommand = StubChatCommand()
            self.__myCutenessCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__cutenessCommand: AbsChatCommand = CutenessChatCommand(cutenessPresenter, cutenessRepository, timber, twitchChatMessenger, userIdsRepository, usersRepository)
            self.__cutenessChampionsCommand: AbsChatCommand = CutenessChampionsChatCommand(cutenessPresenter, cutenessRepository, timber, twitchChatMessenger, usersRepository)
            self.__cutenessHistoryCommand: AbsChatCommand = CutenessHistoryChatCommand(cutenessRepository, cutenessUtils, timber, twitchChatMessenger, userIdsRepository, usersRepository)
            self.__giveCutenessCommand: AbsChatCommand = GiveCutenessChatCommand(cutenessRepository, timber, triviaUtils, authRepository, twitchChatMessenger, userIdsRepository, usersRepository)
            self.__myCutenessCommand: AbsChatCommand = MyCutenessChatCommand(cutenessRepository, cutenessUtils, timber, twitchChatMessenger, usersRepository)

        if funtoonTokensRepository is None:
            self.__setFuntoonTokenCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__setFuntoonTokenCommand: AbsChatCommand = SetFuntoonTokenChatCommand(administratorProvider, funtoonTokensRepository, timber, twitchUtils, usersRepository)

        if jishoHelper is None:
            self.__jishoCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__jishoCommand: AbsChatCommand = JishoChatCommand(generalSettingsRepository, jishoHelper, timber, twitchChatMessenger, usersRepository)

        if anivCopyMessageTimeoutScoreHelper is None or anivCopyMessageTimeoutScorePresenter is None or anivSettings is None:
            self.__anivTimeoutsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__anivTimeoutsCommand: AbsChatCommand = AnivTimeoutsChatCommand(anivCopyMessageTimeoutScoreHelper, anivCopyMessageTimeoutScorePresenter, anivSettings, timber, twitchChannelEditorsRepository, twitchChatMessenger, userIdsRepository, usersRepository)

        if pokepediaRepository is None:
            self.__pkMonCommand: AbsChatCommand = StubChatCommand()
            self.__pkMoveCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__pkMonCommand: AbsChatCommand = PkMonChatCommand(pokepediaRepository, timber, twitchUtils, usersRepository)
            self.__pkMoveCommand: AbsChatCommand = PkMoveChatCommand(pokepediaRepository, timber, twitchUtils, usersRepository)

        if starWarsQuotesRepository is None:
            self.__swQuoteCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__swQuoteCommand: AbsChatCommand = SwQuoteChatCommand(starWarsQuotesRepository, timber, twitchChatMessenger, usersRepository)

        if translationHelper is None:
            self.__translateCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__translateCommand: AbsChatCommand = TranslateChatCommand(languagesRepository, timber, translationHelper, twitchChatMessenger, usersRepository)

        if ttsChatterRepository is None:
            self.__removeTtsChatterCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__removeTtsChatterCommand: AbsChatCommand = RemoveTtsChatterChatCommand(timber, ttsChatterRepository, twitchChatMessenger, usersRepository)

        if streamAlertsManager is None or ttsJsonMapper is None:
            self.__ttsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__ttsCommand: AbsChatCommand = TtsChatCommand(administratorProvider, streamAlertsManager, timber, ttsJsonMapper, twitchChatMessenger, usersRepository)

        if locationsRepository is None or weatherReportPresenter is None or weatherRepository is None:
            self.__weatherCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__weatherCommand: AbsChatCommand = WeatherChatCommand(locationsRepository, timber, twitchChatMessenger, usersRepository, weatherReportPresenter, weatherRepository)

        if twitchCheerHandler is None:
            self.__testCheerCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__testCheerCommand: AbsChatCommand = TestCheerChatCommand(twitchCheerHandler, timber, twitchChatMessenger, usersRepository)

        if eccoHelper is None:
            self.__eccoCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__eccoCommand: AbsChatCommand = EccoChatCommand(eccoHelper, timber, twitchChatMessenger, usersRepository)

        if timeoutImmuneUserIdsRepository is None:
            self.__vulnerableChattersCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__vulnerableChattersCommand: AbsChatCommand = VulnerableChattersChatCommand(activeChattersRepository, timber, timeoutImmuneUserIdsRepository, twitchChatMessenger, usersRepository)

        if voicemailHelper is None or voicemailsRepository is None or voicemailSettingsRepository is None:
            self.__playVoicemailCommand: AbsChatCommand = StubChatCommand()
            self.__voicemailsCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__playVoicemailCommand: AbsChatCommand = PlayVoicemailChatCommand(compositeTtsManagerProvider, streamAlertsManager, timber, timeZoneRepository, twitchChatMessenger, usersRepository, voicemailHelper, voicemailSettingsRepository)
            self.__voicemailsCommand: AbsChatCommand = VoicemailsChatCommand(timber, timeZoneRepository, twitchChatMessenger, twitchTokensUtils, userIdsRepository, usersRepository, voicemailHelper, voicemailSettingsRepository)

        if wordOfTheDayPresenter is None or wordOfTheDayRepository is None:
            self.__wordCommand: AbsChatCommand = StubChatCommand()
        else:
            self.__wordCommand: AbsChatCommand = WordChatCommand(languagesRepository, timber, twitchChatMessenger, usersRepository, wordOfTheDayPresenter, wordOfTheDayRepository)

        self.__timber.log('CynanBot', f'Finished initialization of {self.__authRepository.getAll().requireTwitchHandle()}')

    async def event_channel_join_failure(self, channel: str):
        self.__timber.log('CynanBot', f'Encountered channel join failure ({channel=})')

        userId = await self.__userIdsRepository.fetchUserId(channel)
        user: UserInterface | None = None
        exception: Exception | None = None

        try:
            user = await self.__usersRepository.getUserAsync(channel)
        except Exception as e:
            exception = e

        if user is None or exception is not None:
            self.__timber.log('CynanBot', f'Failed to join channel, and also failed to retrieve a user for this channel ({channel=}) ({userId=}) ({user=}): {exception}', exception, traceback.format_exc())
            return

        self.__timber.log('CynanBot', f'Failed to join channel ({channel=}) ({userId=}) ({user=}), disabling this user...')

        await self.__usersRepository.setUserEnabled(
            handle = user.handle,
            enabled = False
        )

        self.__timber.log('CynanBot', f'Finished disabling user due to channel join failure ({channel=}) ({userId=}) ({user=})')

    async def event_command_error(self, context: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        else:
            raise error

    async def event_join(self, channel: Channel, user: User):
        # intentionally empty for now
        pass

    async def event_message(self, message: Message):
        if message.echo:
            return

        twitchMessage = self.__twitchConfiguration.getMessage(message)

        if await twitchMessage.isMessageFromExternalSharedChat():
            return

        if self.__chatActionsManager is not None:
            await self.__chatActionsManager.handleMessage(twitchMessage)

        await self.handle_commands(message)

    async def event_mode(self, channel: Channel, user: User, status: str):
        self.__timber.log('CynanBot', f'Received MODE event ({channel=}) ({user=}) ({status=})')

    async def event_part(self, user: User):
        # intentionally empty for now
        pass

    async def event_ready(self):
        await self.waitForReady()

        twitchHandle = await self.__authRepository.getTwitchHandle()
        self.__timber.log('CynanBot', f'{twitchHandle} is ready!')

        self.__twitchChannelJoinHelper.setChannelJoinListener(self)
        self.__twitchChannelJoinHelper.joinChannels()

    async def event_reconnect(self):
        self.__timber.log('CynanBot', f'Received RECONNECT event')
        await self.waitForReady()
        self.__timber.log('CynanBot', f'Finished reconnecting')

    async def __getChannel(self, twitchChannel: str) -> TwitchChannel:
        if not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        await self.waitForReady()

        try:
            channel = self.get_channel(twitchChannel)

            if channel is None:
                self.__timber.log('CynanBot', f'Unable to get twitchChannel: \"{twitchChannel}\"')
                raise RuntimeError(f'Unable to get twitchChannel: \"{twitchChannel}\"')
            else:
                return self.__twitchConfiguration.getChannel(channel)
        except KeyError as e:
            self.__timber.log('CynanBot', f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e, traceback.format_exc())
            raise RuntimeError(f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e, traceback.format_exc())

    async def getTwitchChannel(self, twitchChannel: str) -> TwitchChannel:
        return await self.__getChannel(twitchChannel)

    async def onAddOrRemoveUserEvent(self, event: AddOrRemoveUserData):
        self.__timber.log('CynanBot', f'Received new modify user data event ({event=})')

        await self.waitForReady()

        match event.actionType:
            case AddOrRemoveUserActionType.ADD:
                channels: list[str] = list()
                channels.append(event.userName)
                await self.join_channels(channels)

            case AddOrRemoveUserActionType.REMOVE:
                channels: list[str] = list()
                channels.append(event.userName)
                await self.part_channels(channels)

            case _:
                raise RuntimeError(f'unknown AddOrRemoveUserData type: ({event=})')

    async def onNewChannelJoinEvent(self, event: AbsChannelJoinEvent):
        self.__timber.log('CynanBot', f'Received new channel join event ({event=})')

        await self.waitForReady()

        if isinstance(event, FinishedJoiningChannelsEvent):
            await self.__handleFinishedJoiningChannelsEvent(event)
        elif isinstance(event, JoinChannelsEvent):
            await self.__handleJoinChannelsEvent(event)

    async def __handleFinishedJoiningChannelsEvent(self, event: FinishedJoiningChannelsEvent):
        self.__timber.log('CynanBot', f'Finished joining channels ({event.allChannels=})')

        await self.waitForReady()

        self.__addOrRemoveUserDataHelper.setAddOrRemoveUserEventListener(self)
        self.__timber.start()
        self.__twitchTokensRepository.start()
        self.__sentMessageLogger.start()
        self.__chatLogger.start()
        self.__streamAlertsManager.start()
        self.__twitchChatMessenger.start()
        self.__twitchUtils.start()

        if self.__twitchChannelPointRedemptionHandler is not None:
            self.__twitchChannelPointRedemptionHandler.setTwitchChannelProvider(self)
            self.__twitchChannelPointRedemptionHandler.start()

        if self.__chatterItemEventHandler is not None:
            self.__chatterItemEventHandler.setTwitchConnectionReadinessProvider(self)

        if self.__chatterInventoryItemUseMachine is not None:
            self.__chatterInventoryItemUseMachine.setEventListener(self.__chatterItemEventHandler)
            self.__chatterInventoryItemUseMachine.start()

        if self.__crowdControlMachine is not None:
            self.__crowdControlMachine.setActionHandler(self.__crowdControlActionHandler)
            self.__crowdControlMachine.setMessageListener(self.__crowdControlMessageListener)
            self.__crowdControlMachine.start()

        if self.__timeoutEventHandler is not None:
            self.__timeoutEventHandler.setTwitchConnectionReadinessProvider(self)

        if self.__timeoutActionMachine is not None:
            self.__timeoutActionMachine.setEventListener(self.__timeoutEventHandler)
            self.__timeoutActionMachine.start()

        if self.__twitchTimeoutRemodHelper is not None:
            self.__twitchTimeoutRemodHelper.start()

        if self.__triviaEventHandler is not None:
            self.__triviaEventHandler.setTwitchConnectionReadinessProvider(self)

        if self.__triviaGameMachine is not None:
            self.__triviaGameMachine.setEventListener(self.__triviaEventHandler)
            self.__triviaGameMachine.startMachine()

        if self.__triviaRepository is not None:
            self.__triviaRepository.startSpooler()

        if self.__recurringActionsEventHandler is not None:
            self.__recurringActionsEventHandler.setTwitchConnectionReadinessProvider(self)

        if self.__recurringActionsMachine is not None:
            self.__recurringActionsMachine.setEventListener(self.__recurringActionsEventHandler)
            self.__recurringActionsMachine.startMachine()

        if self.__pixelsDiceMachine is not None:
            self.__pixelsDiceMachine.setEventListener(self.__pixelsDiceEventListener)
            self.__pixelsDiceMachine.start()

        if self.__websocketConnectionServer is not None:
            self.__websocketConnectionServer.start()

        if self.__twitchWebsocketClient is not None:
            self.__twitchWebsocketClient.setDataBundleListener(TwitchWebsocketDataBundleHandler(
                channelPointRedemptionHandler = self.__twitchChannelPointRedemptionHandler,
                chatHandler = self.__twitchChatHandler,
                cheerHandler = self.__twitchCheerHandler,
                followHandler = self.__twitchFollowHandler,
                hypeTrainHandler = self.__twitchHypeTrainHandler,
                pollHandler = self.__twitchPollHandler,
                predictionHandler = self.__twitchPredictionHandler,
                raidHandler = self.__twitchRaidHandler,
                subscriptionHandler = self.__twitchSubscriptionHandler,
                timber = self.__timber,
                userIdsRepository = self.__userIdsRepository,
                usersRepository = self.__usersRepository,
            ))

            self.__twitchWebsocketClient.start()

        self.__twitchIrcReconnectHelper.setTwitchIoBot(self)
        self.__twitchIrcReconnectHelper.start()

    async def __handleJoinChannelsEvent(self, event: JoinChannelsEvent):
        self.__timber.log('CynanBot', f'Joining channels: {event}')
        await self.join_channels(event.channels)

    async def waitForReady(self):
        await self.wait_for_ready()

    @commands.command(name = 'addbannedtriviacontroller')
    async def command_addbannedtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addBannedTriviaControllerCommand.handleChatCommand(context)

    @commands.command(name = 'addcrowdcontrolcheeraction', aliases = [ 'addcrowdcontrolaction' ])
    async def command_addcrowdcontrolaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addCrowdControlCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'addgameshufflecheeraction', aliases = [ 'addgameshuffleaction' ])
    async def command_addgameshufflecheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addGameShuffleCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'addgameshuffleautomator')
    async def command_addgameshuffleautomator(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addGameShuffleAutomatorCommand.handleChatCommand(context)

    @commands.command(name = 'addglobaltriviacontroller')
    async def command_addglobaltriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addGlobalTriviaControllerCommand.handleChatCommand(context)

    @commands.command(name = 'additemusecheeraction', aliases = [ 'additemuseaction' ])
    async def command_additemusecheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addItemUseCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'addrecurringcutenessaction')
    async def command_addrecurringcutenessaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addRecurringCutenessActionCommand.handleChatCommand(context)

    @commands.command(name = 'addrecurringsupertriviaaction', aliases = [ 'addrecurringtriviaaction' ])
    async def command_addrecurringsupertriviaaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addRecurringSuperTriviaActionCommand.handleChatCommand(context)

    @commands.command(name = 'addrecurringweatheraction')
    async def command_addrecurringweatheraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addRecurringWeatherActionCommand.handleChatCommand(context)

    @commands.command(name = 'addrecurringwordofthedayaction', aliases = [ 'addrecurringwordaction', 'addrecurringwotdaction' ])
    async def command_addrecurringwordofthedayaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addRecurringWordOfTheDayActionCommand.handleChatCommand(context)

    @commands.command(name = 'addsoundalertcheeraction', aliases = [ 'addsoundalertaction' ])
    async def command_addsoundalertcheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addSoundAlertCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'addtriviaanswer')
    async def command_addtriviaanswer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addTriviaAnswerCommand.handleChatCommand(context)

    @commands.command(name = 'addtriviacontroller')
    async def command_addtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addTriviaControllerCommand.handleChatCommand(context)

    @commands.command(name = 'adduser')
    async def command_adduser(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addUserCommand.handleChatCommand(context)

    @commands.command(name = 'addvoicemailcheeraction')
    async def command_addvoicemailcheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__addVoicemailCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'anivtimeouts')
    async def command_anivtimeouts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__anivTimeoutsCommand.handleChatCommand(context)

    @commands.command(name = 'answer', aliases = [ 'ANSWER', 'Answer', 'a', 'A' ])
    async def command_answer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__answerCommand.handleChatCommand(context)

    @commands.command(name = 'asplodiestats', aliases = [ 'asplodies', 'asplodiesstats', 'getasplodiestats' ])
    async def command_asplodiestats(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__asplodieStatsCommand.handleChatCommand(context)

    @commands.command(name = 'bantriviaquestion', aliases = [ 'bantrivia' ])
    async def command_bantriviaquestion(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__banTriviaQuestionCommand.handleChatCommand(context)

    @commands.command(name = 'beans')
    async def command_beans(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__beanInstructionsCommand.handleChatCommand(context)

    @commands.command(name = 'beanstats')
    async def command_beanstats(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__beanStatsCommand.handleChatCommand(context)

    @commands.command(name = 'bluesky', aliases = [ 'BlueSky', 'blueSky', 'bsky' ])
    async def command_bluesky(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__blueSkyCommand.handleChatCommand(context)

    @commands.command(name = 'clearcaches')
    async def command_clearcaches(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__clearCachesCommand.handleChatCommand(context)

    @commands.command(name = 'clearsupertriviaqueue', aliases = [ 'cleartriviaqueue' ])
    async def command_clearsupertriviaqueue(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__clearSuperTriviaQueueCommand.handleChatCommand(context)

    @commands.command(name = 'commands')
    async def command_commands(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__commandsCommand.handleChatCommand(context)

    @commands.command(name = 'confirm')
    async def command_confirm(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__confirmCommand.handleChatCommand(context)

    @commands.command(name = 'crowdcontrol')
    async def command_crowdcontrol(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__crowdControlCommand.handleChatCommand(context)

    @commands.command(name = 'cuteness', aliases = [ 'CUTENESS', 'Cuteness' ])
    async def command_cuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessCommand.handleChatCommand(context)

    @commands.command(name = 'cutenesschampions')
    async def command_cutenesschampions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessChampionsCommand.handleChatCommand(context)

    @commands.command(name = 'cutenesshistory')
    async def command_cutenesshistory(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cutenessHistoryCommand.handleChatCommand(context)

    @commands.command(name = 'cynansource')
    async def command_cynansource(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__cynanSourceCommand.handleChatCommand(context)

    @commands.command(name = 'deletecheeraction', aliases = [ 'delcheeraction', 'removecheeraction' ])
    async def command_deletecheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__deleteCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'deletetriviaanswers', aliases = [ 'deltriviaanswers', 'removetriviaanswers' ])
    async def command_deletetriviaanswers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__deleteTriviaAnswersCommand.handleChatCommand(context)

    @commands.command(name = 'disablecheeraction')
    async def command_disablecheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__disableCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'discord', aliases = [ 'Discord' ])
    async def command_discord(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__discordCommand.handleChatCommand(context)

    @commands.command(name = 'ecco', aliases = [ 'Ecco' ])
    async def command_ecco(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__eccoCommand.handleChatCommand(context)

    @commands.command(name = 'enablecheeraction')
    async def command_enablecheeraction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__enableCheerActionCommand.handleChatCommand(context)

    @commands.command(name = 'freegiveitem', aliases = [ 'freeitem', 'freeitemgive', 'freegivechatteritem' ])
    async def command_freegivechatteritem(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__freeGiveChatterItemCommand.handleChatCommand(context)

    @commands.command(name = 'getbannedtriviacontrollers', aliases = [ 'bannedtriviacontrollers' ])
    async def command_getbannedtriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getBannedTriviaControllersCommand.handleChatCommand(context)

    @commands.command(name = 'getpreferredname', aliases = [ 'getchatterpreferredname', 'myname', 'mypreferredname', 'preferredname' ])
    async def command_getchatterpreferredname(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getChatterPreferredNameCommand.handleChatCommand(context)

    @commands.command(name = 'getpreferredtts', aliases = [ 'getchatterpreferredtts', 'mytts', 'mypreferredtts', 'preferredtts' ])
    async def command_getchatterpreferredtts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getChatterPreferredTtsCommand.handleChatCommand(context)

    @commands.command(name = 'getcheeractions', aliases = [ 'cheeractions' ])
    async def command_getcheeractions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getCheerActionsCommand.handleChatCommand(context)

    @commands.command(name = 'getglobaltriviacontrollers', aliases = [ 'globaltriviacontrollers' ])
    async def command_getglobaltriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getGlobalTriviaControllersCommand.handleChatCommand(context)

    @commands.command(name = 'getrecurringactions', aliases = [ 'recurringactions' ])
    async def command_getrecurringactions(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getRecurringActionsCommand.handleChatCommand(context)

    @commands.command(name = 'gettriviaanswers', aliases = [ 'triviaanswers' ])
    async def command_gettriviaanswers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getTriviaAnswersCommand.handleChatCommand(context)

    @commands.command(name = 'gettriviacontrollers', aliases = [ 'triviacontrollers' ])
    async def command_gettriviacontrollers(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__getTriviaControllersCommand.handleChatCommand(context)

    @commands.command(name = 'givecuteness', aliases = [ 'addcuteness' ])
    async def command_givecuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__giveCutenessCommand.handleChatCommand(context)

    @commands.command(name = 'giveitem', aliases = [ 'givechatteritem', 'itemgive' ])
    async def command_givechatteritem(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__giveChatterItemCommand.handleChatCommand(context)

    @commands.command(name = 'inventory', aliases = [ 'inv' ])
    async def command_chatterinventory(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__chatterInventoryCommand.handleChatCommand(context)

    @commands.command(name = 'jisho')
    async def command_jisho(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__jishoCommand.handleChatCommand(context)

    @commands.command(name = 'lorem', aliases = [ 'loremipsum' ])
    async def command_lorem(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__loremIpsumCommand.handleChatCommand(context)

    @commands.command(name = 'mycuteness', aliases = [ 'mycutenesshistory' ])
    async def command_mycuteness(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__myCutenessCommand.handleChatCommand(context)

    @commands.command(name = 'pkmon')
    async def command_pkmon(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pkMonCommand.handleChatCommand(context)

    @commands.command(name = 'playvoicemail')
    async def command_playvoicemail(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__playVoicemailCommand.handleChatCommand(context)

    @commands.command(name = 'pkmove', aliases = [ 'pkmov' ])
    async def command_pkmove(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__pkMoveCommand.handleChatCommand(context)

    @commands.command(name = 'removebannedtriviacontroller')
    async def command_removebannedtriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeBannedTriviaControllerCommand.handleChatCommand(context)

    @commands.command(name = 'removepreferredname', aliases = [ 'deletechatterpreferredname', 'deletemyname', 'removechatterpreferredname', 'removemyname' ])
    async def command_removechatterpreferredname(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeChatterPreferredNameCommand.handleChatCommand(context)

    @commands.command(name = 'removepreferredtts', aliases = [ 'deletechatterpreferredtts', 'deletemytts', 'removechatterpreferredtts', 'removemytts' ])
    async def command_removechatterpreferredtts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeChatterPreferredTtsCommand.handleChatCommand(context)

    @commands.command(name = 'removegameshuffleautomator', aliases = [ 'delgameshuffleautomator', 'deletegameshuffleautomator' ])
    async def command_removegameshuffleautomator(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeGameShuffleAutomatorCommand.handleChatCommand(context)

    @commands.command(name = 'removeglobaltriviacontroller', aliases = [ 'delglobaltriviacontroller', 'deleteglobaltriviacontroller' ])
    async def command_removeglobaltriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeGlobalTriviaControllerChatCommand.handleChatCommand(context)

    @commands.command(name = 'removerecurringcutenessaction', aliases = [ 'delrecurringcutenessaction', 'deleterecurringcutenessaction' ])
    async def command_removerecurringcutenessaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeRecurringCutenessActionCommand.handleChatCommand(context)

    @commands.command(name = 'removerecurringsupertriviaaction', aliases = [ 'deleterecurringsupertriviaaction', 'deleterecurringtriviaaction', 'removerecurringtriviaaction' ])
    async def command_removerecurringsupertriviaaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeRecurringSuperTriviaActionCommand.handleChatCommand(context)

    @commands.command(name = 'removerecurringweatheraction', aliases = [ 'deleterecurringweatheraction' ])
    async def command_removeweatherrecurringaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeRecurringWeatherActionCommand.handleChatCommand(context)

    @commands.command(name = 'removerecurringwordofthedayaction', aliases = [ 'deleterecurringwordaction', 'deleterecurringwordofthedayaction', 'deleterecurringwotdaction', 'removerecurringwordaction', 'removerecurringwotdaction' ])
    async def command_removerecurringwordofthedayaction(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeRecurringWordOfTheDayActionCommand.handleChatCommand(context)

    @commands.command(name = 'removetriviacontroller', aliases = [ 'deltriviacontroller', 'deletetriviacontroller' ])
    async def command_removetriviacontroller(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeTriviaControllerChatCommand.handleChatCommand(context)

    @commands.command(name = 'stopttschatting', aliases = [ 'stopttschat', 'stoptts' ])
    async def command_removettschatter(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__removeTtsChatterCommand.handleChatCommand(context)

    @commands.command(name = 'setpreferredname', aliases = [ 'setname' ])
    async def command_setchatterpreferredtts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setChatterPreferredNameCommand.handleChatCommand(context)

    @commands.command(name = 'setpreferredtts', aliases = [ 'settts' ])
    async def command_setchatterpreferredtts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setChatterPreferredTtsCommand.handleChatCommand(context)

    @commands.command(name = 'setfuntoontoken')
    async def command_setfuntoontoken(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setFuntoonTokenCommand.handleChatCommand(context)

    @commands.command(name = 'settwitchcode')
    async def command_settwitchcode(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__setTwitchCodeCommand.handleChatCommand(context)

    @commands.command(name = 'skiptts', aliases = [ 'skipTts', 'skipTTS', 'SkipTts', 'Skiptts', 'SkipTTS', 'SKIPTTS' ])
    async def command_skiptts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__skipTtsCommand.handleChatCommand(context)

    @commands.command(name = 'superanswer', aliases = [ 'SUPERANSWER', 'SuperAnswer', 'Superanswer', 'sa', 'SA', 'Sa', 'sA', 'sanswer', 'SANSWER', 'Sanswer' ])
    async def command_superanswer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__superAnswerCommand.handleChatCommand(context)

    @commands.command(name = 'supertrivia', aliases = [ 'Supertrivia', 'SuperTrivia', 'supertrivialotr' ])
    async def command_supertrivia(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__superTriviaCommand.handleChatCommand(context)

    @commands.command(name = 'swquote')
    async def command_swquote(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__swQuoteCommand.handleChatCommand(context)

    @commands.command(name = 'testcheer', aliases = [ 'testcheeraction' ])
    async def command_testcheer(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__testCheerCommand.handleChatCommand(context)

    @commands.command(name = 'time')
    async def command_time(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__timeCommand.handleChatCommand(context)

    @commands.command(name = 'translate')
    async def command_translate(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__translateCommand.handleChatCommand(context)

    @commands.command(name = 'triviainfo', aliases = [ 'gettriviainfo' ])
    async def command_triviainfo(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__triviaInfoCommand.handleChatCommand(context)

    @commands.command(name = 'triviascore')
    async def command_triviascore(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__triviaScoreCommand.handleChatCommand(context)

    @commands.command(name = 'tts', aliases = [ 'TTS', 'Tts', 'TTs' ])
    async def command_tts(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__ttsCommand.handleChatCommand(context)

    @commands.command(name = 'twitchuserinfo', aliases = [ 'twitchinfo', 'userinfo' ])
    async def command_twitchuserinfo(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__twitchUserInfoCommand.handleChatCommand(context)

    @commands.command(name = 'unbantriviaquestion', aliases = [ 'unbantrivia' ])
    async def command_unbantriviaquestion(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__unbanTriviaQuestionChatCommand.handleChatCommand(context)

    @commands.command(
        name = 'useitem',
        aliases = [ 'use', 'Use', 'USE', 'usechatteritem', 'use-item', 'use_item' ]
    )
    async def command_usechatteritem(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__useChatterItemCommand.handleChatCommand(context)

    @commands.command(name = 'voicemails', aliases = [ 'voicemail' ])
    async def command_voicemails(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__voicemailsCommand.handleChatCommand(context)

    @commands.command(name = 'vulnerablechatters', aliases = [ 'vulnerablechatter', 'vc', 'vcs', 'VC', 'VCS' ])
    async def command_vulnerablechatters(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__vulnerableChattersCommand.handleChatCommand(context)

    @commands.command(name = 'weather')
    async def command_weather(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__weatherCommand.handleChatCommand(context)

    @commands.command(name = 'word')
    async def command_word(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__wordCommand.handleChatCommand(context)
