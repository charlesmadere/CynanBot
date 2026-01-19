from typing import Any, Collection, Final

from frozenlist import FrozenList

from .api.models.twitchOutcome import TwitchOutcome
from .api.models.twitchOutcomeColor import TwitchOutcomeColor
from .api.models.twitchWebsocketSubscriptionType import TwitchWebsocketSubscriptionType
from .twitchPredictionWebsocketUtilsInterface import TwitchPredictionWebsocketUtilsInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class TwitchPredictionWebsocketUtils(TwitchPredictionWebsocketUtilsInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: Final[TimberInterface] = timber

    async def __determineIndexBasedColorDictionary(
        self,
        colors: FrozenList[dict[str, int]],
        index: int,
    ) -> dict[str, int]:
        if not isinstance(colors, FrozenList):
            raise TypeError(f'colors argument is malformed: \"{colors}\"')
        elif not utils.isValidInt(index):
            raise TypeError(f'index argument is malformed: \"{index}\"')
        elif index < 0 or index > utils.getIntMaxSafeSize():
            raise ValueError(f'index argument is out of bounds: {index}')

        match index:
            case 0:
                return await self.outcomeColorToEventData(TwitchOutcomeColor.BLUE)

            case 1:
                return await self.outcomeColorToEventData(TwitchOutcomeColor.PINK)

            case 2:
                # orange
                return {
                    'red': 255,
                    'green': 127,
                    'blue': 0,
                }

            case 3:
                # green
                return {
                    'red': 127,
                    'green': 255,
                    'blue': 0,
                }

            case 4:
                # cyan
                return {
                    'red': 0,
                    'green': 255,
                    'blue': 255,
                }

            case 5:
                # light-ish blue
                return {
                    'red': 0,
                    'green': 127,
                    'blue': 255,
                }

            case 6:
                # magenta
                return {
                    'red': 255,
                    'green': 0,
                    'blue': 255,
                }

            case 7:
                # red
                return {
                    'red': 255,
                    'green': 0,
                    'blue': 0,
                }

            case 8:
                # yellow
                return {
                    'red': 255,
                    'green': 255,
                    'blue': 0,
                }

            case 9:
                # purple
                return {
                    'red': 127,
                    'green': 0,
                    'blue': 255,
                }

            case 10:
                # silver
                return {
                    'red': 192,
                    'green': 192,
                    'blue': 192,
                }

            case 11:
                # dark slate
                return {
                    'red': 47,
                    'green': 79,
                    'blue': 79,
                }

            case _:
                raise RuntimeError(f'Encountered unexpected TwitchOutcome color index ({index=}) ({colors=})')

    async def outcomeColorToEventData(
        self,
        color: TwitchOutcomeColor,
    ) -> dict[str, int]:
        if not isinstance(color, TwitchOutcomeColor):
            raise TypeError(f'color argument is malformed: \"{color}\"')

        match color:
            case TwitchOutcomeColor.BLUE:
                return {
                    'red': 54,
                    'green': 162,
                    'blue': 235,
                }

            case TwitchOutcomeColor.PINK:
                return {
                    'red': 255,
                    'green': 99,
                    'blue': 132,
                }

            case _:
                raise RuntimeError(f'Unknown TwitchOutcomeColor: \"{color}\"')

    async def __outcomesToColorsArray(
        self,
        outcomes: FrozenList[TwitchOutcome],
    ) -> FrozenList[dict[str, int]]:
        if not isinstance(outcomes, FrozenList) or len(outcomes) == 0:
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')

        colors: FrozenList[dict[str, int]] = FrozenList()

        if len(outcomes) <= 2:
            for outcome in outcomes:
                colors.append(await self.outcomeColorToEventData(outcome.color))
        else:
            for index, _ in enumerate(outcomes):
                colors.append(await self.__determineIndexBasedColorDictionary(
                    colors = colors,
                    index = index,
                ))

        colors.freeze()
        return colors

    async def outcomesToEventDataArray(
        self,
        outcomes: Collection[TwitchOutcome],
    ) -> list[dict[str, Any]]:
        if not isinstance(outcomes, Collection):
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')

        sortedOutcomes: list[TwitchOutcome] = list(outcomes)
        sortedOutcomes.sort(key = lambda twitchOutcome: twitchOutcome.title.casefold())
        frozenSortedOutcomes: FrozenList[TwitchOutcome] = FrozenList(sortedOutcomes)
        frozenSortedOutcomes.freeze()

        colors = await self.__outcomesToColorsArray(frozenSortedOutcomes)
        events: list[dict[str, Any]] = list()

        for index, outcome in enumerate(frozenSortedOutcomes):
            events.append({
                'channelPoints': outcome.channelPoints,
                'color': colors[index],
                'outcomeId': outcome.outcomeId,
                'title': outcome.title,
                'users': outcome.users,
            })

        return events

    async def websocketEventToEventDataDictionary(
        self,
        outcomes: FrozenList[TwitchOutcome],
        eventId: str,
        title: str,
        subscriptionType: TwitchWebsocketSubscriptionType,
    ) -> dict[str, Any] | None:
        if not isinstance(outcomes, FrozenList):
            raise TypeError(f'outcomes argument is malformed: \"{outcomes}\"')
        elif not utils.isValidStr(eventId):
            raise TypeError(f'eventId argument is malformed: \"{eventId}\"')
        elif not utils.isValidStr(title):
            raise TypeError(f'title argument is malformed: \"{title}\"')
        elif not isinstance(subscriptionType, TwitchWebsocketSubscriptionType):
            raise TypeError(f'subscriptionType argument is malformed: \"{subscriptionType}\"')

        if len(outcomes) == 0:
            return None

        outcomesArray = await self.outcomesToEventDataArray(outcomes)
        predictionTypeString = await self.websocketSubscriptionTypeToString(subscriptionType)

        return {
            'eventId': eventId,
            'outcomes': outcomesArray,
            'predictionType': predictionTypeString,
            'title': title,
        }

    async def websocketSubscriptionTypeToString(
        self,
        subscriptionType: TwitchWebsocketSubscriptionType,
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
                raise ValueError(f'Can\'t convert the given TwitchWebsocketSubscriptionType (\"{subscriptionType}\") into a string!')
