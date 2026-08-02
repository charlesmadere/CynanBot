from typing import Final

from ..absTwitchHypeTrainHandler import AbsTwitchHypeTrainHandler
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..localModels.mapper.twitchLocalModelsMapperInterface import TwitchLocalModelsMapperInterface
from ..localModels.twitchHypeTrainState import TwitchHypeTrainState
from ...misc import utils as utils
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...trollmoji.trollmojiHelperInterface import TrollmojiHelperInterface
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ...users.userInterface import UserInterface


class TwitchHypeTrainHandler(AbsTwitchHypeTrainHandler):

    class HypeTrainState:

        def __init__(
            self,
            hypeTrainId: str,
            twitchChannelId: str,
        ):
            self.__hypeTrainId: Final[str] = hypeTrainId
            self.__twitchChannelId: Final[str] = twitchChannelId

            self.__level: int = 1

        @property
        def hypeTrainId(self) -> str:
            return self.__hypeTrainId

        @property
        def level(self) -> int:
            return self.__level

        def setLevel(self, level: int):
            self.__level = level

        @property
        def twitchChannelId(self) -> str:
            return self.__twitchChannelId


    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        trollmojiHelper: TrollmojiHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchLocalModelsMapper: TwitchLocalModelsMapperInterface,
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(trollmojiHelper, TrollmojiHelperInterface):
            raise TypeError(f'trollmojiHelper argument is malformed: \"{trollmojiHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchLocalModelsMapper, TwitchLocalModelsMapperInterface):
            raise TypeError(f'twitchLocalModelsMapper argument is malformed: \"{twitchLocalModelsMapper}\"')

        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__trollmojiHelper: Final[TrollmojiHelperInterface] = trollmojiHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchLocalModelsMapper: Final[TwitchLocalModelsMapperInterface] = twitchLocalModelsMapper

        self.__hypeTrains: Final[dict[str, TwitchHypeTrainHandler.HypeTrainState | None]] = dict()

    async def __notifyOfHypeTrainProgress(
        self,
        hypeTrainData: AbsTwitchHypeTrainHandler.HypeTrainData,
        hypeTrainState: HypeTrainState,
    ):
        user = hypeTrainData.user

        if not user.isNotifyOfHypeTrainProgressEnabled or not user.isTtsEnabled:
            return
        elif hypeTrainData.hypeTrainState is not TwitchHypeTrainState.PROGRESS:
            return
        elif hypeTrainState.level >= hypeTrainData.level:
            return

        hypeTrainState.setLevel(hypeTrainData.level)

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.HYPE_TRAIN,
            twitchChannel = user.handle,
            twitchChannelId = hypeTrainData.twitchChannelId,
            ttsEvent = TtsEvent(
                message = f'Hype train upgraded to level {hypeTrainData.level}!',
                twitchChannel = user.handle,
                twitchChannelId = hypeTrainData.twitchChannelId,
                userId = hypeTrainData.twitchChannelId,
                userName = user.handle,
                donation = None,
                provider = user.defaultTtsProvider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))

    async def __notifyOfHypeTrainStart(
        self,
        hypeTrainData: AbsTwitchHypeTrainHandler.HypeTrainData,
        hypeTrainState: HypeTrainState,
    ):
        user = hypeTrainData.user

        if not user.isNotifyOfHypeTrainStartEnabled:
            return
        elif hypeTrainData.hypeTrainState is not TwitchHypeTrainState.BEGIN:
            return

        if user.isTtsEnabled:
            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = SoundAlert.HYPE_TRAIN,
                twitchChannel = user.handle,
                twitchChannelId = hypeTrainData.twitchChannelId,
                ttsEvent = TtsEvent(
                    message = f'A hype train has begun!',
                    twitchChannel = user.handle,
                    twitchChannelId = hypeTrainData.twitchChannelId,
                    userId = hypeTrainData.twitchChannelId,
                    userName = user.handle,
                    donation = None,
                    provider = user.defaultTtsProvider,
                    providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                    raidInfo = None,
                ),
            ))

        self.__twitchChatMessenger.send(
            text = f'{hypeTrainData.hypeEmoji} A hype train has begun! {hypeTrainData.hypeEmoji}',
            twitchChannelId = hypeTrainData.twitchChannelId,
        )

    async def onNewHypeTrain(self, hypeTrainData: AbsTwitchHypeTrainHandler.HypeTrainData):
        if not isinstance(hypeTrainData, AbsTwitchHypeTrainHandler.HypeTrainData):
            raise TypeError(f'hypeTrainData argument is malformed: \"{hypeTrainData}\"')

        hypeTrainState = self.__hypeTrains.get(hypeTrainData.twitchChannelId, None)

        if hypeTrainState is None or hypeTrainState.hypeTrainId != hypeTrainData.hypeTrainId:
            hypeTrainState = TwitchHypeTrainHandler.HypeTrainState(
                hypeTrainId = hypeTrainData.hypeTrainId,
                twitchChannelId = hypeTrainData.twitchChannelId,
            )

            self.__hypeTrains[hypeTrainData.twitchChannelId] = hypeTrainState

        if hypeTrainData.user.isNotifyOfHypeTrainStartEnabled:
            await self.__notifyOfHypeTrainStart(
                hypeTrainData = hypeTrainData,
                hypeTrainState = hypeTrainState,
            )

        if hypeTrainData.user.isNotifyOfHypeTrainProgressEnabled:
            await self.__notifyOfHypeTrainProgress(
                hypeTrainData = hypeTrainData,
                hypeTrainState = hypeTrainState,
            )

    async def onNewHypeTrainDataBundle(
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
            self.__timber.log('TwitchHypeTrainHandler', f'Received a data bundle that is missing event data ({user=}) ({dataBundle=})')
            return

        isSharedTrain = event.isSharedTrain
        level = event.level
        total = event.total
        hypeEmoji = await self.__trollmojiHelper.getHypeEmoteOrBackup()
        hypeTrainId = event.eventId
        hypeTrainState = await self.__twitchLocalModelsMapper.mapHypeTrainState(dataBundle.metadata.subscriptionType)
        hypeTrainType = await self.__twitchLocalModelsMapper.mapHypeTrainType(event.hypeTrainType)

        if isSharedTrain is None or level is None or total is None or not utils.isValidStr(hypeTrainId) or hypeTrainState is None or hypeTrainType is None:
            self.__timber.log('TwitchHypeTrainHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({dataBundle=}) ({isSharedTrain=}) ({level=}) ({total=}) ({hypeTrainId=}) ({hypeTrainState=}) ({hypeTrainType=})')
            return

        hypeTrainData = AbsTwitchHypeTrainHandler.HypeTrainData(
            isSharedTrain = isSharedTrain,
            level = level,
            total = total,
            hypeEmoji = hypeEmoji,
            hypeTrainId = hypeTrainId,
            twitchChannelId = twitchChannelId,
            hypeTrainState = hypeTrainState,
            hypeTrainType = hypeTrainType,
            user = user,
        )

        await self.onNewHypeTrain(
            hypeTrainData = hypeTrainData,
        )
