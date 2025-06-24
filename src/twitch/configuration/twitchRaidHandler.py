from typing import Final

from .twitchChannelProvider import TwitchChannelProvider
from ..absTwitchRaidHandler import AbsTwitchRaidHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ...chatLogger.chatLoggerInterface import ChatLoggerInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProvider import TtsProvider
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ...tts.models.ttsRaidInfo import TtsRaidInfo
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

        self.__chatLogger: Final[ChatLoggerInterface] = chatLogger
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __buildRaidMessage(
        self,
        viewers: int,
        fromUserName: str,
        user: UserInterface
    ) -> str:
        # Not sure if I'll keep this method, but I wanted to try out some things that may work a
        # bit better with Google MultiSpeaker TTS. And so, some of this is hardcoded a bit more
        # than I would really want if I ever make this a more longterm feature.

        if user.defaultTtsProvider is TtsProvider.GOOGLE:
            if viewers >= 100:
                return f'Hey everyone coming in from {fromUserName}\'s stream! Welcome in!! Wow, that\'s a ton of chatters. Thanks so much for the raid!'

            elif viewers >= 75:
                return f'Hey y\'all from {fromUserName}\'s stream! Thanks for the raid of {viewers}. Sup everyone! And welcome in!'

            elif viewers >= 25:
                return f'Hey everyone from {fromUserName}\'s stream! Thanks for bringing over {viewers} chatters. Welcome in!'

            elif viewers >= 10:
                return f'Hey everybody from {fromUserName}\'s stream! Thanks for coming in with {viewers} chatters. Welcome!'

        return f'Hello everyone from {fromUserName}\'s stream, welcome in. Thanks for the raid!'

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
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that has no event ({user=}) ({dataBundle=})')
            return

        fromUserId = event.fromBroadcasterUserId
        fromUserLogin = event.fromBroadcasterUserLogin
        fromUserName = event.fromBroadcasterUserName
        toUserId = event.toBroadcasterUserId
        toUserLogin = event.toBroadcasterUserLogin
        toUserName = event.toBroadcasterUserName
        viewers = event.viewers

        if not utils.isValidStr(fromUserId) or not utils.isValidStr(fromUserLogin) or not utils.isValidStr(fromUserName) or not utils.isValidStr(toUserId) or not utils.isValidStr(toUserLogin) or not utils.isValidStr(toUserName) or not utils.isValidInt(viewers):
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({dataBundle=}) ({fromUserId=}) ({fromUserLogin=}) ({fromUserName=}) ({toUserId=}) ({toUserLogin=}) ({toUserName=}) ({viewers=})')
            return

        if user.isChatLoggingEnabled:
            self.__chatLogger.logRaid(
                raidSize = viewers,
                fromWho = fromUserName,
                twitchChannel = user.handle,
                twitchChannelId = toUserId
            )

        if user.isTtsEnabled:
            await self.__processTtsEvent(
                viewers = viewers,
                broadcasterUserId = toUserId,
                fromUserId = fromUserId,
                fromUserName = fromUserName,
                user = user
            )

    async def __processTtsEvent(
        self,
        viewers: int,
        broadcasterUserId: str,
        fromUserId: str,
        fromUserName: str,
        user: UserInterface
    ):
        if not user.isTtsEnabled:
            return
        elif viewers < 1:
            return

        raidMessage = await self.__buildRaidMessage(
            viewers = viewers,
            fromUserName = fromUserName,
            user = user
        )

        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.RAID,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                message = raidMessage,
                twitchChannel = user.handle,
                twitchChannelId = broadcasterUserId,
                userId = fromUserId,
                userName = fromUserName,
                donation = None,
                provider = user.defaultTtsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = TtsRaidInfo(
                    viewers = viewers
                )
            )
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
