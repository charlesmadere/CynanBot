from frozenlist import FrozenList

from ..absTwitchPredictionHandler import AbsTwitchPredictionHandler
from ..api.twitchOutcome import TwitchOutcome
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.websocket.twitchWebsocketEvent import TwitchWebsocketEvent
from ..api.websocket.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..configuration.twitchChannelProvider import TwitchChannelProvider
from ..twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface
from ...misc import utils as utils
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...tts.ttsEvent import TtsEvent
from ...users.userInterface import UserInterface
from ...websocketConnection.websocketConnectionServerInterface import WebsocketConnectionServerInterface


class TwitchPredictionHandler(AbsTwitchPredictionHandler):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchPredictionWebsocketUtils: TwitchPredictionWebsocketUtilsInterface | None,
        websocketConnectionServer: WebsocketConnectionServerInterface | None,
        websocketEventType: str = 'channelPrediction',
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise TypeError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')
        elif not utils.isValidStr(websocketEventType):
            raise TypeError(f'websocketEventType argument is malformed: \"{websocketEventType}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__twitchPredictionWebsocketUtils: TwitchPredictionWebsocketUtilsInterface | None = twitchPredictionWebsocketUtils
        self.__websocketConnectionServer: WebsocketConnectionServerInterface | None = websocketConnectionServer
        self.__websocketEventType: str = websocketEventType

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def onNewPrediction(
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

        payload = dataBundle.requirePayload()
        event = payload.event

        if event is None:
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that has no event (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        broadcasterUserId = event.broadcasterUserId
        title = event.title
        outcomes = event.outcomes

        if not utils.isValidStr(broadcasterUserId) or not utils.isValidStr(title) or outcomes is None or len(outcomes) == 0:
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({broadcasterUserId=}) ({title=}) ({outcomes=})')
            return

        subscriptionType = payload.requireSubscription().subscriptionType
        self.__timber.log('TwitchPredictionHandler', f'\"{user.getHandle()}\" received prediction event ({title=}) ({outcomes=}) ({subscriptionType=})')

        await self.__processTtsEvent(
            broadcasterUserId = broadcasterUserId,
            title = title,
            userId = userId,
            user = user,
            subscriptionType = subscriptionType
        )

        await self.__processWebsocketEvent(
            outcomes = outcomes,
            title = title,
            user = user,
            event = event,
            subscriptionType = subscriptionType
        )

    async def __processTtsEvent(
        self,
        broadcasterUserId: str,
        title: str,
        userId: str,
        user: UserInterface,
        subscriptionType: TwitchWebsocketSubscriptionType
    ):
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        if subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return
        elif not user.isTtsEnabled():
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                message = f'A new prediction has begun! \"{title}\"',
                twitchChannel = user.getHandle(),
                twitchChannelId = broadcasterUserId,
                userId = userId,
                userName = user.getHandle(),
                donation = None,
                provider = user.defaultTtsProvider,
                raidInfo = None
            )
        ))

    async def __processWebsocketEvent(
        self,
        outcomes: FrozenList[TwitchOutcome],
        title: str,
        user: UserInterface,
        event: TwitchWebsocketEvent,
        subscriptionType: TwitchWebsocketSubscriptionType
    ):
        if not isinstance(outcomes, FrozenList):
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')
        elif not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(event, TwitchWebsocketEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        twitchPredictionWebsocketUtils = self.__twitchPredictionWebsocketUtils
        websocketConnectionServer = self.__websocketConnectionServer

        if twitchPredictionWebsocketUtils is None or websocketConnectionServer is None:
            return
        elif not user.isChannelPredictionChartEnabled():
            return

        eventData = await twitchPredictionWebsocketUtils.websocketEventToEventDataDictionary(
            event = event,
            subscriptionType = subscriptionType
        )

        if eventData is None or len(eventData) == 0:
            return

        await websocketConnectionServer.sendEvent(
            twitchChannel = user.getHandle(),
            eventType = self.__websocketEventType,
            eventData = eventData
        )

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
