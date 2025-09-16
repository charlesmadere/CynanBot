from typing import Final

from ..absTwitchPredictionHandler import AbsTwitchPredictionHandler
from ..activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..api.models.twitchPredictionStatus import TwitchPredictionStatus
from ..api.models.twitchWebsocketDataBundle import TwitchWebsocketDataBundle
from ..api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from ..chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundAlert import SoundAlert
from ...streamAlertsManager.streamAlert import StreamAlert
from ...streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ...timber.timberInterface import TimberInterface
from ...tts.models.ttsEvent import TtsEvent
from ...tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ...users.userInterface import UserInterface
from ...websocketConnection.websocketConnectionServerInterface import WebsocketConnectionServerInterface
from ...websocketConnection.websocketEventType import WebsocketEventType


class TwitchPredictionHandler(AbsTwitchPredictionHandler):

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchPredictionWebsocketUtils: TwitchPredictionWebsocketUtilsInterface | None,
        websocketConnectionServer: WebsocketConnectionServerInterface,
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise TypeError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchPredictionWebsocketUtils: Final[TwitchPredictionWebsocketUtilsInterface | None] = twitchPredictionWebsocketUtils
        self.__websocketConnectionServer: Final[WebsocketConnectionServerInterface] = websocketConnectionServer

    async def __notifyChatOfPredictionResults(self, predictionData: AbsTwitchPredictionHandler.PredictionData):
        outcomes = predictionData.outcomes
        winningOutcomeId = predictionData.winningOutcomeId
        user = predictionData.user

        if not user.isNotifyOfPredictionResultsEnabled:
            return
        elif not utils.isValidStr(winningOutcomeId):
            return
        elif predictionData.predictionStatus is not TwitchPredictionStatus.RESOLVED:
            return
        elif predictionData.subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END:
            return

        winningOutcome = [ outcome for outcome in outcomes if outcome.outcomeId == winningOutcomeId ][0]
        topPredictors = winningOutcome.topPredictors

        outcomeString = f'🗳️ The winning outcome is \"{winningOutcome.title}\"!'

        if topPredictors is not None and len(topPredictors) >= 1:
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
                predictorPluralization = 'The top predictor was'
            else:
                predictorPluralization = 'Top predictors:'

            outcomeString = outcomeString + f' {predictorPluralization} {topPredictorsString}!'

        self.__twitchChatMessenger.send(
            text = outcomeString,
            twitchChannelId = predictionData.twitchChannelId,
        )

    async def __notifyChatOfPredictionStart(self, predictionData: AbsTwitchPredictionHandler.PredictionData):
        user = predictionData.user

        if not user.isNotifyOfPredictionStartEnabled:
            return
        elif predictionData.subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return

        # intentionally empty for now
        pass

    async def __notifyWebsocketOfPredictionEvent(self, predictionData: AbsTwitchPredictionHandler.PredictionData):
        if self.__twitchPredictionWebsocketUtils is None:
            return
        elif not predictionData.user.isChannelPredictionChartEnabled:
            return

        eventData = await self.__twitchPredictionWebsocketUtils.websocketEventToEventDataDictionary(
            outcomes = predictionData.outcomes,
            eventId = predictionData.eventId,
            title = predictionData.title,
            subscriptionType = predictionData.subscriptionType,
        )

        if eventData is None or len(eventData) == 0:
            return

        self.__websocketConnectionServer.submitEvent(
            twitchChannel = predictionData.user.handle,
            twitchChannelId = predictionData.twitchChannelId,
            eventType = WebsocketEventType.CHANNEL_PREDICTION,
            eventData = eventData,
        )

    async def onNewPrediction(self, predictionData: AbsTwitchPredictionHandler.PredictionData):
        if not isinstance(predictionData, AbsTwitchPredictionHandler.PredictionData):
            raise TypeError(f'predictionData argument is malformed: \"{predictionData}\"')

        await self.__processActiveChatters(predictionData)
        await self.__notifyWebsocketOfPredictionEvent(predictionData)

        if predictionData.user.isTtsEnabled:
            await self.__processTtsEvent(predictionData)

        if predictionData.user.isNotifyOfPredictionStartEnabled:
            await self.__notifyChatOfPredictionStart(predictionData)

        if predictionData.user.isNotifyOfPredictionResultsEnabled:
            await self.__notifyChatOfPredictionResults(predictionData)

    async def onNewPredictionDataBundle(
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
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that is missing event data ({user=}) ({dataBundle=})')
            return

        outcomes = event.outcomes
        eventId = event.eventId
        title = event.title
        subscriptionType = dataBundle.metadata.subscriptionType

        if outcomes is None or len(outcomes) == 0 or not utils.isValidStr(eventId) or not utils.isValidStr(title) or subscriptionType is None:
            self.__timber.log('TwitchPredictionHandler', f'Received a data bundle that is missing crucial data: ({user=}) ({dataBundle=}) ({outcomes=}) ({eventId=}) ({title=}) ({subscriptionType=})')
            return

        predictionData = AbsTwitchPredictionHandler.PredictionData(
            outcomes = outcomes,
            eventId = eventId,
            title = title,
            twitchChannelId = twitchChannelId,
            winningOutcomeId = event.winningOutcomeId,
            user = user,
            predictionStatus = event.predictionStatus,
            subscriptionType = subscriptionType,
        )

        await self.onNewPrediction(
            predictionData = predictionData,
        )

    async def __processActiveChatters(self, predictionData: AbsTwitchPredictionHandler.PredictionData):
        if predictionData.subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
            return

        userIdsToUserNames: dict[str, str] = dict()

        for outcome in predictionData.outcomes:
            topPredictors = outcome.topPredictors

            if topPredictors is not None and len(topPredictors) >= 1:
                for topPredictor in topPredictors:
                    userIdsToUserNames[topPredictor.userId] = topPredictor.userLogin

        for userId, userName in userIdsToUserNames.items():
            await self.__activeChattersRepository.add(
                chatterUserId = userId,
                chatterUserName = userName,
                twitchChannelId = predictionData.twitchChannelId,
            )

    async def __processTtsEvent(self, predictionData: AbsTwitchPredictionHandler.PredictionData):
        user = predictionData.user

        if not user.isTtsEnabled:
            return
        elif not user.isNotifyOfPredictionStartEnabled:
            return
        elif predictionData.subscriptionType is not TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.PREDICTION,
            twitchChannel = user.handle,
            twitchChannelId = predictionData.twitchChannelId,
            ttsEvent = TtsEvent(
                message = f'A new prediction has begun! \"{predictionData.title}\"',
                twitchChannel = user.handle,
                twitchChannelId = predictionData.twitchChannelId,
                userId = predictionData.twitchChannelId,
                userName = user.handle,
                donation = None,
                provider = user.defaultTtsProvider,
                providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
                raidInfo = None,
            ),
        ))
