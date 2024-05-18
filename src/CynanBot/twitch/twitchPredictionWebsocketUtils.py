from typing import Any

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
    ) -> dict[str, Any] | None:
        if not isinstance(event, TwitchWebsocketEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

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
        outcomes: list[TwitchOutcome]
    ) -> list[dict[str, int]]:
        if not isinstance(outcomes, list) or len(outcomes) == 0:
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')

        colors: list[dict[str, int]] = list()

        if len(outcomes) <= 2:
            for outcome in outcomes:
                colors.append(await self.outcomeColorToEventData(outcome.color))
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
    ) -> dict[str, int]:
        if not isinstance(color, TwitchOutcomeColor):
            raise TypeError(f'color argument is malformed: \"{color}\"')

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
        outcomes: list[TwitchOutcome]
    ) -> list[dict[str, Any]]:
        if not isinstance(outcomes, list) or len(outcomes) == 0:
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')

        sortedOutcomes = sorted(outcomes, key = lambda outcome: outcome.title.lower())
        colors = await self.websocketOutcomesToColorsArray(outcomes)

        events: list[dict[str, Any]] = list()

        for index, outcome in enumerate(sortedOutcomes):
            events.append({
                'channelPoints': outcome.channelPoints,
                'color': colors[index],
                'outcomeId': outcome.outcomeId,
                'title': outcome.title,
                'users': outcome.users
            })

        return events

    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType
    ) -> str:
        if not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        match subscriptionType:
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_BEGIN:
                return 'prediction_begin'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_END:
                return 'prediction_end'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_LOCK:
                return 'prediction_lock'
            case TwitchWebsocketSubscriptionType.CHANNEL_PREDICTION_PROGRESS:
                return 'prediction_progress'
            case _:
                raise ValueError(f'Can\'t convert the given WebsocketSubscriptionType (\"{subscriptionType}\") into a string!')
