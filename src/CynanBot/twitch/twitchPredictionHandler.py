from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.streamAlertsManager.streamAlert import StreamAlert
from CynanBot.streamAlertsManager.streamAlertsManagerInterface import \
    StreamAlertsManagerInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsProvider import TtsProvider
from CynanBot.twitch.absTwitchPredictionHandler import \
    AbsTwitchPredictionHandler
from CynanBot.twitch.api.twitchOutcome import TwitchOutcome
from CynanBot.twitch.api.websocket.twitchWebsocketDataBundle import \
    TwitchWebsocketDataBundle
from CynanBot.twitch.api.websocket.twitchWebsocketEvent import \
    TwitchWebsocketEvent
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
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
        assert streamAlertsManager is None or isinstance(streamAlertsManager, StreamAlertsManagerInterface), f"malformed {streamAlertsManager=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert twitchPredictionWebsocketUtils is None or isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface), f"malformed {twitchPredictionWebsocketUtils=}"
        assert websocketConnectionServer is None or isinstance(websocketConnectionServer, WebsocketConnectionServerInterface), f"malformed {websocketConnectionServer=}"
        if not utils.isValidStr(websocketEventType):
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
        dataBundle: TwitchWebsocketDataBundle
    ):
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(dataBundle, TwitchWebsocketDataBundle), f"malformed {dataBundle=}"

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
        subscriptionType: TwitchWebsocketSubscriptionType
    ):
        if not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        if not utils.isValidStr(userId):
            raise TypeError(f'userId argument is malformed: \"{userId}\"')
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"

        if subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
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
                provider = TtsProvider.DEC_TALK,
                raidInfo = None
            )
        ))

    async def __processWebsocketEvent(
        self,
        outcomes: List[TwitchOutcome],
        title: str,
        user: UserInterface,
        event: TwitchWebsocketEvent,
        subscriptionType: TwitchWebsocketSubscriptionType
    ):
        assert isinstance(outcomes, List), f"malformed {outcomes=}"
        if not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(event, TwitchWebsocketEvent), f"malformed {event=}"
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"

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
