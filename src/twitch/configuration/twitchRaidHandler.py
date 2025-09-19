from typing import Final

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
        timber: TimberInterface,
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

    async def __buildRaidMessage(self, raidData: AbsTwitchRaidHandler.RaidData) -> str:
        # Not sure if I'll keep this method, but I wanted to try out some things that may work a
        # bit better with Google MultiSpeaker TTS. And so, some of this is hardcoded a bit more
        # than I would really want if I ever make this a more long term feature.

        viewers = raidData.viewers
        fromUserName = raidData.raidUserName

        if raidData.user.defaultTtsProvider is TtsProvider.GOOGLE:
            if viewers >= 100:
                return f'Hey everyone coming in from {fromUserName}\'s stream! Welcome in!! Wow, that\'s a ton of chatters. Thanks so much for the raid!'

            elif viewers >= 75:
                return f'Hey y\'all from {fromUserName}\'s stream! Thanks for the raid of {viewers}. Sup everyone! And welcome in!'

            elif viewers >= 25:
                return f'Hey everyone from {fromUserName}\'s stream! Thanks for bringing over {viewers} chatters. Welcome in!'

            elif viewers >= 10:
                return f'Hey everybody from {fromUserName}\'s stream! Thanks for coming in with {viewers} chatters. Welcome!'

        return f'Hello everyone from {fromUserName}\'s stream, welcome in. Thanks for the raid!'

    async def onNewRaid(self, raidData: AbsTwitchRaidHandler.RaidData):
        if not isinstance(raidData, AbsTwitchRaidHandler.RaidData):
            raise TypeError(f'raidData argument is malformed: \"{raidData}\"')

        if raidData.user.isChatLoggingEnabled:
            self.__chatLogger.logRaid(
                viewers = raidData.viewers,
                raidUserId = raidData.raidUserId,
                raidUserLogin = raidData.raidUserLogin,
                twitchChannel = raidData.user.handle,
                twitchChannelId = raidData.twitchChannelId,
            )

        minimumRaidViewersForNotification = raidData.user.minimumRaidViewersForNotification

        if minimumRaidViewersForNotification is not None and raidData.viewers < minimumRaidViewersForNotification:
            self.__timber.log('TwitchRaidHandler', f'Received raid that has too few viewers to be considered for notification ({minimumRaidViewersForNotification=}) ({raidData=})')
            return

        if raidData.user.isTtsEnabled:
            await self.__processTtsEvent(raidData)

    async def onNewRaidDataBundle(
        self,
        twitchChannelId: str,
        user: UserInterface,
        dataBundle: TwitchWebsocketDataBundle,
    ):
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, TwitchWebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        event = dataBundle.requirePayload().event

        if event is None:
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that has no event ({user=}) ({twitchChannelId=}) ({dataBundle=})')
            return

        viewers = event.viewers
        fromUserId = event.fromBroadcasterUserId
        fromUserLogin = event.fromBroadcasterUserLogin
        fromUserName = event.fromBroadcasterUserName

        if not utils.isValidInt(viewers) or viewers < 1 or not utils.isValidStr(fromUserId) or not utils.isValidStr(fromUserLogin) or not utils.isValidStr(fromUserName):
            self.__timber.log('TwitchRaidHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({twitchChannelId=}) ({dataBundle=}) ({viewers=}) ({fromUserId=}) ({fromUserLogin=}) ({fromUserName=})')
            return

        raidData = AbsTwitchRaidHandler.RaidData(
            viewers = viewers,
            raidUserId = fromUserId,
            raidUserLogin = fromUserLogin,
            raidUserName = fromUserName,
            twitchChannelId = twitchChannelId,
            user = user,
        )

        await self.onNewRaid(
            raidData = raidData,
        )

    async def __processTtsEvent(self, raidData: AbsTwitchRaidHandler.RaidData):
        user = raidData.user

        if not user.isTtsEnabled:
            return
        elif raidData.viewers < 1:
            return
        elif not user.isNotifyOfRaidEnabled:
            return

        raidMessage = await self.__buildRaidMessage(raidData)
        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.RAID,
            twitchChannel = user.handle,
            twitchChannelId = raidData.twitchChannelId,
            ttsEvent = TtsEvent(
                message = raidMessage,
                twitchChannel = user.handle,
                twitchChannelId = raidData.twitchChannelId,
                userId = raidData.raidUserId,
                userName = raidData.raidUserName,
                donation = None,
                provider = user.defaultTtsProvider,
                providerOverridableStatus = providerOverridableStatus,
                raidInfo = TtsRaidInfo(
                    viewers = raidData.viewers,
                ),
            ),
        ))
