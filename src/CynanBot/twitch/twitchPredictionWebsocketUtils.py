from typing import Any, Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.twitch.api.twitchOutcome import TwitchOutcome
from CynanBot.twitch.api.twitchOutcomeColor import TwitchOutcomeColor
from CynanBot.twitch.api.websocket.twitchWebsocketEvent import \
    TwitchWebsocketEvent
from CynanBot.twitch.api.websocket.twitchWebsocketSubscriptionType import \
    TwitchWebsocketSubscriptionType
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface


class TwitchPredictionWebsocketUtils(TwitchPredictionWebsocketUtilsInterface):

    async def websocketEventToEventDataDictionary(
        self,
        event: TwitchWebsocketEvent,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> Optional[Dict[str, Any]]:
        assert isinstance(event, TwitchWebsocketEvent), f"malformed {event=}"
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"

        eventId = event.getEventId()
        if not utils.isValidStr(eventId):
            return None

        title = event.getTitle()
        if not utils.isValidStr(title):
            return None

        outcomes = event.getOutcomes()
        if outcomes is None or len(outcomes) == 0:
            return None

        outcomesArray = await self.outcomesToEventDataArray(outcomes)
        predictionTypeString = await self.websocketSubscriptionTypeToString(subscriptionType)

        return {
            'eventId': eventId,
            'outcomes': outcomesArray,
            'predictionType': predictionTypeString,
            'title': title
        }

    async def websocketOutcomesToColorsArray(
        self,
        outcomes: List[TwitchOutcome]
    ) -> List[Dict[str, int]]:
        if not isinstance(outcomes, List) or len(outcomes) == 0:
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')

        colors: List[Dict[str, int]] = list()

        if len(outcomes) <= 2:
            for outcome in outcomes:
                colors.append(await self.outcomeColorToEventData(outcome.getColor()))
        else:
            for index, outcome in enumerate(outcomes):
                if index == 0:
                    colors.append(await self.outcomeColorToEventData(TwitchOutcomeColor.BLUE))
                elif index == 1:
                    colors.append(await self.outcomeColorToEventData(TwitchOutcomeColor.PINK))
                elif index == 2:
                    # orange
                    colors.append({
                        'red': 255,
                        'green': 127,
                        'blue': 0
                    })
                elif index == 3:
                    # green
                    colors.append({
                        'red': 127,
                        'green': 255,
                        'blue': 0
                    })
                elif index == 4:
                    # cyan
                    colors.append({
                        'red': 0,
                        'green': 255,
                        'blue': 255
                    })
                elif index == 5:
                    # light-ish blue
                    colors.append({
                        'red': 0,
                        'green': 127,
                        'blue': 255
                    })
                elif index == 6:
                    # magenta
                    colors.append({
                        'red': 255,
                        'green': 0,
                        'blue': 255
                    })
                elif index == 7:
                    # red
                    colors.append({
                        'red': 255,
                        'green': 0,
                        'blue': 0
                    })
                elif index == 8:
                    # yellow
                    colors.append({
                        'red': 255,
                        'green': 255,
                        'blue': 0
                    })
                elif index == 9:
                    # purple
                    colors.append({
                        'red': 127,
                        'green': 0,
                        'blue': 255
                    })
                elif index == 10:
                    # silver
                    colors.append({
                        'red': 192,
                        'green': 192,
                        'blue': 192
                    })
                elif index == 11:
                    # dark slate
                    colors.append({
                        'red': 47,
                        'green': 79,
                        'blue': 79
                    })

        return colors

    async def outcomeColorToEventData(
        self,
        color: TwitchOutcomeColor
    ) -> Dict[str, int]:
        assert isinstance(color, TwitchOutcomeColor), f"malformed {color=}"

        if color is TwitchOutcomeColor.BLUE:
            return {
                'red': 54,
                'green': 162,
                'blue': 235
            }
        elif color is TwitchOutcomeColor.PINK:
            return {
                'red': 255,
                'green': 99,
                'blue': 132
            }
        else:
            raise RuntimeError(f'Unknown WebsocketOutcomeColor: \"{color}\"')

    async def outcomesToEventDataArray(
        self,
        outcomes: List[TwitchOutcome]
    ) -> List[Dict[str, Any]]:
        if not isinstance(outcomes, List) or len(outcomes) == 0:
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')

        sortedOutcomes = sorted(outcomes, key = lambda outcome: outcome.getTitle().lower())
        colors = await self.websocketOutcomesToColorsArray(outcomes)

        events: List[Dict[str, Any]] = list()

        for index, outcome in enumerate(sortedOutcomes):
            events.append({
                'channelPoints': outcome.getChannelPoints(),
                'color': colors[index],
                'outcomeId': outcome.getOutcomeId(),
                'title': outcome.getTitle(),
                'users': outcome.getUsers()
            })

        return events

    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> str:
        assert isinstance(subscriptionType, TwitchWebsocketSubscriptionType), f"malformed {subscriptionType=}"

        if subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
            return 'prediction_begin'
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END:
            return 'prediction_end'
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
            return 'prediction_lock'
        elif subscriptionType is TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
            return 'prediction_progress'
        else:
            raise ValueError(f'Can\'t convert the given WebsocketSubscriptionType (\"{subscriptionType}\") into a string!')
