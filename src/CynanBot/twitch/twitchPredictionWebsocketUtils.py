from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.websocket.websocketEvent import WebsocketEvent
from CynanBot.twitch.websocket.websocketOutcome import WebsocketOutcome
from CynanBot.twitch.websocket.websocketSubscriptionType import \
    WebsocketSubscriptionType


class TwitchPredictionWebsocketUtils(TwitchPredictionWebsocketUtilsInterface):

    async def websocketEventToEventDataDictionary(
        self,
        event: WebsocketEvent,
        subscriptionType: WebsocketSubscriptionType
    ) -> Optional[Dict[str, Any]]:
        if not isinstance(event, WebsocketEvent):
            raise ValueError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(subscriptionType, WebsocketSubscriptionType):
            raise ValueError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        eventId = event.getEventId()
        if not utils.isValidStr(eventId):
            return None

        title = event.getTitle()
        if not utils.isValidStr(title):
            return None

        outcomes = event.getOutcomes()
        if outcomes is None or len(outcomes) == 0:
            return None

        outcomesArray = await self.websocketOutcomesToEventDataArray(outcomes)
        predictionTypeString = await self.websocketSubscriptionTypeToString(subscriptionType)

        return {
            'eventId': eventId,
            'outcomes': outcomesArray,
            'predictionType': predictionTypeString,
            'title': title
        }

    async def websocketOutcomesToEventDataArray(
        self,
        outcomes: List[WebsocketOutcome]
    ) -> List[Dict[str, Any]]:
        if not isinstance(outcomes, List) or len(outcomes) == 0:
            raise ValueError(f'outcomes argument is malformed: \"{outcomes}\"')

        sortedOutcomes = sorted(outcomes, key = lambda outcome: outcome.getTitle().lower())
        events: List[Dict[str, Any]] = list()

        for outcome in sortedOutcomes:
            events.append({
                'channelPoints': outcome.getChannelPoints(),
                'outcomeId': outcome.getOutcomeId(),
                'title': outcome.getTitle(),
                'users': outcome.getUsers()
            })

        return events

    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: WebsocketSubscriptionType
    ) -> str:
        if not isinstance(subscriptionType, WebsocketSubscriptionType):
            raise ValueError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        if subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return 'prediction_begin'
        elif subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_END:
            return 'prediction_end'
        elif subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
            return 'prediction_lock'
        elif subscriptionType is WebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return 'prediction_progress'
        else:
            raise ValueError(f'Can\'t convert the given WebsocketSubscriptionType (\"{subscriptionType}\") into a string!')
