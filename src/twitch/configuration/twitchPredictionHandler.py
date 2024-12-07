from frozenlist import FrozenList

from ..absTwitchPredictionHandler import AbsTwitchPredictionHandler
from ..api.twitchOutcome import TwitchOutcome
from ..api.twitchPredictionStatus import TwitchPredictionStatus
from ..api.websocket.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.websocket.twitchWebsocketEvent import TwitchWebsocketEvent
from ..api.websocket.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..configuration.twitchChannelProvider import TwitchChannelProvider
from ..twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface
from ..twitchUtilsInterface import TwitchUtilsInterface
from ...misc import utils as utils
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...tts.ttsEvent import TtsEvent
from ...users.userInterface import UserInterface
from ...websocketConnection.websocketConnectionServerInterface import WebsocketConnectionServerInterface
from ...websocketConnection.websocketEventType import WebsocketEventType


class TwitchPredictionHandler(AbsTwitchPredictionHandler):

    def __init__(
        self,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        twitchPredictionWebsocketUtils: TwitchPredictionWebsocketUtilsInterface | None,
        websocketConnectionServer: WebsocketConnectionServerInterface
    ):
        if not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise TypeError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')

        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__twitchPredictionWebsocketUtils: TwitchPredictionWebsocketUtilsInterface | None = twitchPredictionWebsocketUtils
        self.__websocketConnectionServer: WebsocketConnectionServerInterface = websocketConnectionServer

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def __notifyChatOfPredictionResults(
        self,
        outcomes: FrozenList[TwitchOutcome],
        winningOutcomeId: str | None,
        predictionStatus: TwitchPredictionStatus | None,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface,
    ):
        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            return
        elif not utils.isValidStr(winningOutcomeId):
            return
        elif predictionStatus is not TwitchPredictionStatus.RESOLVED:
            return
        elif subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END:
            return
        elif not user.isNotifyOfPredictionResultsEnabled:
            return

        winningOutcome = [ outcome for outcome in outcomes if outcome.outcomeId == winningOutcomeId ][0]
        topPredictors = winningOutcome.topPredictors

        outcomeString = f'🗳️ The winning outcome is \"{winningOutcome.title}\"'

        if topPredictors is not None and len(topPredictors) > 0:
            topPredictorsString = ''
            for index, topPredictor in enumerate(topPredictors):
                predictorString = f'{topPredictor.userName} ({topPredictor.channelPointsWonStr})'
                if index == 0:
                    topPredictorsString = predictorString
                elif index + 1 == len(topPredictors):
                    topPredictorsString = f'{topPredictorsString}, and {predictorString}'
                else:
                    topPredictorsString = f'{topPredictorsString}, {predictorString}'

            predictorPluralization: str
            if len(topPredictors) == 1:
                predictorPluralization = 'top predictor was'
            else:
                predictorPluralization = 'top predictors were'

            outcomeString = outcomeString + f', {predictorPluralization} {topPredictorsString}!'

        twitchChannel = await twitchChannelProvider.getTwitchChannel(user.handle)
        await self.__twitchUtils.safeSend(twitchChannel, outcomeString)

    async def __notifyWebsocketOfPredictionEvent(
        self,
        broadcasterUserId: str,
        event: TwitchWebsocketEvent,
        subscriptionType: TwitchWebsocketSubscriptionType,
        user: UserInterface
    ):
        twitchPredictionWebsocketUtils = self.__twitchPredictionWebsocketUtils

        if twitchPredictionWebsocketUtils is None:
            return
        elif not user.isChannelPredictionChartEnabled:
            return

        eventData = await twitchPredictionWebsocketUtils.websocketEventToEventDataDictionary(
            event = event,
            subscriptionType = subscriptionType
        )

        if eventData is None or len(eventData) == 0:
            return

        self.__websocketConnectionServer.submitEvent(
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            eventType = WebsocketEventType.CHANNEL_PREDICTION,
            eventData = eventData
        )

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
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that has no event (channel=\"{user.handle}\") ({dataBundle=})')
            return

        broadcasterUserId = event.broadcasterUserId
        title = event.title
        outcomes = event.outcomes
        winningOutcomeId = event.winningOutcomeId

        if not utils.isValidStr(broadcasterUserId) or not utils.isValidStr(title) or outcomes is None or len(outcomes) == 0:
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that is missing crucial data: (channel=\"{user.handle}\") ({dataBundle=}) ({broadcasterUserId=}) ({title=}) ({outcomes=})')
            return

        subscriptionType = payload.requireSubscription().subscriptionType
        self.__timber.log('TwitchPredictionHandler', f'\"{user.handle}\" received prediction event ({title=}) ({outcomes=}) ({subscriptionType=})')

        await self.__processTtsEvent(
            broadcasterUserId = broadcasterUserId,
            title = title,
            userId = userId,
            user = user,
            subscriptionType = subscriptionType
        )

        await self.__notifyWebsocketOfPredictionEvent(
            broadcasterUserId = broadcasterUserId,
            event = event,
            subscriptionType = subscriptionType,
            user = user
        )

        await self.__notifyChatOfPredictionResults(
            outcomes = outcomes,
            winningOutcomeId = winningOutcomeId,
            predictionStatus = event.predictionStatus,
            subscriptionType = subscriptionType,
            user = user
        )

    async def __processTtsEvent(
        self,
        broadcasterUserId: str,
        title: str,
        userId: str,
        user: UserInterface,
        subscriptionType: TwitchWebsocketSubscriptionType
    ):
        if not user.isTtsEnabled:
            return
        elif subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = None,
            twitchChannel = user.handle,
            twitchChannelId = broadcasterUserId,
            ttsEvent = TtsEvent(
                message = f'A new prediction has begun! \"{title}\"',
                twitchChannel = user.handle,
                twitchChannelId = broadcasterUserId,
                userId = userId,
                userName = user.handle,
                donation = None,
                provider = user.defaultTtsProvider,
                raidInfo = None
            )
        ))

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
