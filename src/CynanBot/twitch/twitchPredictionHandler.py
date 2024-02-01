from typing import List, Optional
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
import CynanBot.misc.utils as utils
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsManagerInterface import TtsManagerInterface
from CynanBot.twitch.absTwitchPredictionHandler import \
    AbsTwitchPredictionHandler
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.websocket.websocketDataBundle import WebsocketDataBundle
from CynanBot.twitch.websocket.websocketEvent import WebsocketEvent
from CynanBot.twitch.websocket.websocketOutcome import WebsocketOutcome
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from CynanBot.users.userInterface import UserInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class TwitchPredictionHandler(AbsTwitchPredictionHandler):

    def __init__(
        self,
        streamAlertsManager: Optional[StreamAlertsManagerInterface],
        timber: TimberInterface,
        twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface],
        websocketConnectionServer: Optional[WebsocketConnectionServerInterface],
        websocketEventType: str = 'channelPrediction',
    ):
        if streamAlertsManager is not None and not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise TypeError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')
        elif not utils.isValidStr(websocketEventType):
            raise TypeError(f'websocketEventType argument is malformed: \"{websocketEventType}\"')

        self.__streamAlertsManager: Optional[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface] = twitchPredictionWebsocketUtils
        self.__websocketConnectionServer: Optional[WebsocketConnectionServerInterface] = websocketConnectionServer
        self.__websocketEventType: str = websocketEventType

    async def onNewPrediction(
        self,
        userId: str,
        user: UserInterface,
        dataBundle: WebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(dataBundle, WebsocketDataBundle):
            raise TypeError(f'dataBundle argument is malformed: \"{dataBundle}\"')

        payload = dataBundle.requirePayload()
        event = payload.getEvent()

        if event is None:
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that has no event: (channel=\"{user.getHandle()}\") ({dataBundle=})')
            return

        title = event.getTitle()
        outcomes = event.getOutcomes()

        if not utils.isValidStr(title) or not isinstance(outcomes, List):
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.getHandle()}\") ({dataBundle=}) ({title=}) ({outcomes=})')
            return

        subscriptionType = payload.requireSubscription().getSubscriptionType()
        self.__timber.log('TwitchPredictionHandler', f'\"{user.getHandle()}\" received prediction event ({title=}) ({outcomes=}) ({subscriptionType=})')

        await self.__processTtsEvent(
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
        title: str,
        userId: str,
        user: UserInterface,
        subscriptionType: WebsocketSubscriptionType
    ):
        if not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(subscriptionType, WebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        if subscriptionType is not WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return
        elif self.__streamAlertsManager is None:
            return
        elif not user.isTtsEnabled():
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.getHandle(),
            ttsEvent = TtsEvent(
                message = f'A new prediction has begun! \"{title}\"',
                twitchChannel = user.getHandle(),
                userId = userId,
                userName = user.getHandle(),
                donation = None,
                raidInfo = None
            )
        ))

    async def __processWebsocketEvent(
        self,
        outcomes: List[WebsocketOutcome],
        title: str,
        user: UserInterface,
        event: WebsocketEvent,
        subscriptionType: WebsocketSubscriptionType
    ):
        if not isinstance(outcomes, List):
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')
        elif not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(event, WebsocketEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(subscriptionType, WebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        if self.__twitchPredictionWebsocketUtils is None or self.__websocketConnectionServer is None:
            return
        elif not user.isChannelPredictionChartEnabled():
            return

        eventData = await self.__twitchPredictionWebsocketUtils.websocketEventToEventDataDictionary(
            event = event,
            subscriptionType = subscriptionType
        )

        if eventData is None or len(eventData) == 0:
            return

        await self.__websocketConnectionServer.sendEvent(
            twitchChannel = user.getHandle(),
            eventType = self.__websocketEventType,
            eventData = eventData
        )
