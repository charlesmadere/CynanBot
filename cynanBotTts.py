import traceback
from asyncio import AbstractEventLoop
from typing import Any, Dict, List, Optional

from twitchio import Channel, Message
from twitchio.ext import commands
from twitchio.ext.commands import Context
from twitchio.ext.commands.errors import CommandNotFound

import CynanBotCommon.utils as utils
from authRepository import AuthRepository
from commands import AbsCommand, ClearCachesCommand, TtsCommand
from CynanBotCommon.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.lruCache import LruCache
from CynanBotCommon.timber.timberInterface import TimberInterface
from CynanBotCommon.trivia.bannedWords.bannedWordsRepositoryInterface import \
    BannedWordsRepositoryInterface
from CynanBotCommon.twitch.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBotCommon.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBotCommon.twitch.websocket.twitchWebsocketClientInterface import \
    TwitchWebsocketClientInterface
from CynanBotCommon.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBotCommon.users.userInterface import UserInterface
from CynanBotCommon.users.usersRepositoryInterface import \
    UsersRepositoryInterface
from generalSettingsRepository import GeneralSettingsRepository
from twitch.absChannelJoinEvent import AbsChannelJoinEvent
from twitch.channelJoinEventType import ChannelJoinEventType
from twitch.channelJoinHelper import ChannelJoinHelper
from twitch.channelJoinListener import ChannelJoinListener
from twitch.finishedJoiningChannelsEvent import FinishedJoiningChannelsEvent
from twitch.joinChannelsEvent import JoinChannelsEvent
from twitch.twitchChannel import TwitchChannel
from twitch.twitchChannelProvider import TwitchChannelProvider
from twitch.twitchConfiguration import TwitchConfiguration
from twitch.twitchUtils import TwitchUtils
from twitch.twitchWebsocketDataBundleHandler import \
    TwitchWebsocketDataBundleHandler
from users.modifyUserActionType import ModifyUserActionType
from users.modifyUserData import ModifyUserData
from users.modifyUserDataHelper import ModifyUserDataHelper
from users.modifyUserEventListener import ModifyUserEventListener


class CynanBotTts(commands.Bot, ChannelJoinListener, ModifyUserEventListener, TwitchChannelProvider):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        administratorProvider: AdministratorProviderInterface,
        authRepository: AuthRepository,
        backgroundTaskHelper: BackgroundTaskHelper,
        bannedWordsRepository: Optional[BannedWordsRepositoryInterface],
        channelJoinHelper: ChannelJoinHelper,
        generalSettingsRepository: GeneralSettingsRepository,
        modifyUserDataHelper: ModifyUserDataHelper,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchConfiguration: TwitchConfiguration,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtils,
        twitchWebsocketClient: Optional[TwitchWebsocketClientInterface],
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        super().__init__(
            client_secret = authRepository.getAll().requireTwitchClientSecret(),
            initial_channels = list(),
            loop = eventLoop,
            nick = authRepository.getAll().requireNick(),
            prefix = '!',
            retain_cache = True,
            token = authRepository.getAll().requireTwitchIrcAuthToken(),
            heartbeat = 15
        )

        if not isinstance(eventLoop, AbstractEventLoop):
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif not isinstance(administratorProvider, AdministratorProviderInterface):
            raise ValueError(f'administratorProviderInterface argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(authRepository, AuthRepository):
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif bannedWordsRepository is not None and not isinstance(bannedWordsRepository, BannedWordsRepositoryInterface):
            raise ValueError(f'bannedWordsRepository argument is malformed: \"{bannedWordsRepository}\"')
        elif not isinstance(channelJoinHelper, ChannelJoinHelper):
            raise ValueError(f'channelJoinHelper argument is malformed: \"{channelJoinHelper}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(modifyUserDataHelper, ModifyUserDataHelper):
            raise ValueError(f'modifyUserDataHelper argument is malformed: \"{modifyUserDataHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise ValueError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchConfiguration, TwitchConfiguration):
            raise ValueError(f'twitchConfiguration argument is malformed: \"{twitchConfiguration}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif twitchWebsocketClient is not None and not isinstance(twitchWebsocketClient, TwitchWebsocketClientInterface):
            raise ValueError(f'twitchWebsocketClient argument is malformed: \"{twitchWebsocketClient}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__authRepository: AuthRepository = authRepository
        self.__channelJoinHelper: ChannelJoinHelper = channelJoinHelper
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__modifyUserDataHelper: ModifyUserDataHelper = modifyUserDataHelper
        self.__timber: TimberInterface = timber
        self.__twitchConfiguration: TwitchConfiguration = twitchConfiguration
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__twitchWebsocketClient: Optional[TwitchWebsocketClientInterface] = twitchWebsocketClient
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository

        self.__channelPointsLruCache: LruCache = LruCache(64)

        #######################################
        ## Initialization of command objects ##
        #######################################

        self.__ttsCommand: AbsCommand = TtsCommand(timber, twitchUtils, usersRepository)

        self.__timber.log('CynanBotTts', f'Finished initialization of {self.__authRepository.getAll().requireNick()}')

    async def event_channel_join_failure(self, channel: str):
        userId = await self.__userIdsRepository.fetchUserId(channel)
        user: Optional[UserInterface] = None

        try:
            user = await self.__usersRepository.getUserAsync(channel)
        except:
            pass

        self.__timber.log('CynanBotTts', f'Failed to join channel \"{channel}\" (userId=\"{userId}\") (user=\"{user}\"), disabling this user...')

        await self.__usersRepository.setUserEnabled(
            handle = user.getHandle(),
            enabled = False
        )

        self.__timber.log('CynanBotTts', f'Finished disabling user \"{user}\" due to channel join failure')

    async def event_pubsub_error(self, tags: Dict):
        self.__timber.log('CynanBotTts', f'Received PubSub error: {tags}')

    async def event_pubsub_nonce(self, tags: Dict):
        self.__timber.log('CynanBotTts', f'Received PubSub nonce: {tags}')

    async def event_ready(self):
        await self.wait_for_ready()

        twitchHandle = await self.__authRepository.getTwitchHandle()
        self.__timber.log('CynanBotTts', f'{twitchHandle} is ready!')

        self.__channelJoinHelper.setChannelJoinListener(self)
        self.__channelJoinHelper.joinChannels()
        self.__modifyUserDataHelper.setModifyUserEventListener(self)

    async def event_reconnect(self):
        self.__timber.log('CynanBotTts', f'Received new reconnect event')
        await self.wait_for_ready()

    async def __getChannel(self, twitchChannel: str) -> TwitchChannel:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        await self.wait_for_ready()

        try:
            channel = self.get_channel(twitchChannel)

            if channel is None:
                self.__timber.log('CynanBotTts', f'Unable to get twitchChannel: \"{twitchChannel}\"')
                raise RuntimeError(f'Unable to get twitchChannel: \"{twitchChannel}\"')
            else:
                return self.__twitchConfiguration.getChannel(channel)
        except KeyError as e:
            self.__timber.log('CynanBotTts', f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e, traceback.format_exc())
            raise RuntimeError(f'Encountered KeyError when trying to get twitchChannel \"{twitchChannel}\": {e}', e, traceback.format_exc())

    async def getTwitchChannel(self, twitchChannel: str) -> TwitchChannel:
        return await self.__getChannel(twitchChannel)

    async def onModifyUserEvent(self, event: ModifyUserData):
        self.__timber.log('CynanBotTts', f'Received new modify user data event: {event.toStr()}')

        await self.wait_for_ready()

        if event.getActionType() is ModifyUserActionType.ADD:
            channels: List[str] = list()
            channels.append(event.getUserName())
            await self.join_channels(channels)
        elif event.getActionType() is ModifyUserActionType.REMOVE:
            channels: List[str] = list()
            channels.append(event.getUserName())
            await self.part_channels(channels)
        else:
            raise RuntimeError(f'unknown ModifyUserActionType: \"{event.getActionType()}\"')

    async def onNewChannelJoinEvent(self, event: AbsChannelJoinEvent):
        eventType = event.getEventType()
        self.__timber.log('CynanBotTts', f'Received new channel join event: \"{eventType}\"')

        await self.wait_for_ready()

        if eventType is ChannelJoinEventType.FINISHED:
            await self.__handleFinishedJoiningChannelsEvent(event)
        elif eventType is ChannelJoinEventType.JOIN:
            await self.__handleJoinChannelsEvent(event)

    async def __handleFinishedJoiningChannelsEvent(self, event: FinishedJoiningChannelsEvent):
        self.__timber.log('CynanBotTts', f'Finished joining channels: {event.getAllChannels()}')

        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if generalSettings.isEventSubEnabled() and self.__twitchWebsocketClient is not None:
            # TODO
            self.__twitchWebsocketClient.setDataBundleListener(TwitchWebsocketDataBundleHandler(
                timber = self.__timber,
                channelPointRedemptionHandler = None,
                cheerHandler = None,
                subscriptionHandler = None,
                userIdsRepository = self.__userIdsRepository,
                usersRepository = self.__usersRepository
            ))

            self.__twitchWebsocketClient.start()

    async def __handleJoinChannelsEvent(self, event: JoinChannelsEvent):
        self.__timber.log('CynanBotTts', f'Joining channels: {event.getChannels()}')
        await self.join_channels(event.getChannels())

    @commands.command(name = 'tts')
    async def command_translate(self, ctx: Context):
        context = self.__twitchConfiguration.getContext(ctx)
        await self.__ttsCommand.handleCommand(context)
