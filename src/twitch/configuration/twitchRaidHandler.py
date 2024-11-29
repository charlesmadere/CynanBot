from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchRaidHandler import AbsTwitchRaidHandler
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...chatLogger.chatLoggerInterface import ChatLoggerInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...tts.ttsEvent import TtsEvent
from ...tts.ttsRaidInfo import TtsRaidInfo
from ...users.userInterface import UserInterface


class TwitchRaidHandler(AbsTwitchRaidHandler):

    def __init__(
        self,
        chatLogger: ChatLoggerInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface
    ):
        if not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def onNewRaid(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that has no event (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        fromUserId = event.fromBroadcasterUserId
        fromUserLogin = event.fromBroadcasterUserLogin
        fromUserName = event.fromBroadcasterUserName
        toUserId = event.toBroadcasterUserId
        toUserLogin = event.toBroadcasterUserLogin
        toUserName = event.toBroadcasterUserName
        viewers = event.viewers

        if not utils.isValidStr(fromUserId) or not utils.isValidStr(fromUserLogin) or not utils.isValidStr(fromUserName) or not utils.isValidStr(toUserId) or not utils.isValidStr(toUserLogin) or not utils.isValidStr(toUserName) or not utils.isValidInt(viewers):
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({fromUserId=}) ({fromUserLogin=}) ({fromUserName=}) ({toUserId=}) ({toUserLogin=}) ({toUserName=}) ({viewers=})')
            return

        self.__timber.log('TwitchRaidHandler', f'\"{user.getHandle()}\" received raid of {viewers} from \"{fromUserLogin}\"')

        if user.isChatLoggingEnabled:
            self.__chatLogger.logRaid(
                raidSize = viewers,
                fromWho = fromUserName,
                twitchChannel = user.getHandle(),
                twitchChannelId = toUserId
            )

        await self.__processTtsEvent(
            viewers = viewers,
            broadcasterUserId = toUserId,
            userId = fromUserId,
            fromUserName = fromUserName,
            user = user
        )

    async def __processTtsEvent(
        self,
        viewers: int,
        broadcasterUserId: str,
        userId: str,
        fromUserName: str,
        user: UserInterface
    ):
        if not utils.isValidInt(viewers):
            raise TypeError(f'viewers argument is malformed: \"{viewers}\"')
        elif viewers < 0 or viewers > utils.getIntMaxSafeSize():
            raise ValueError(f'viewers argument is out of bounds: {viewers}')
        elif not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(fromUserName):
            raise TypeError(f'fromUserName argument is malformed: \"{fromUserName}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        if not user.isTtsEnabled:
            return
        elif viewers < 1:
            return

        raidInfo = TtsRaidInfo(viewers = viewers)

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.RAID,
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                message = f'Hello everyone from {fromUserName}\'s stream, welcome in. Thanks for the raid!',
                twitchChannel = user.getHandle(),
                twitchChannelId = broadcasterUserId,
                userId = userId,
                userName = fromUserName,
                donation = None,
                provider = user.defaultTtsProvider,
                raidInfo = raidInfo
            )
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
