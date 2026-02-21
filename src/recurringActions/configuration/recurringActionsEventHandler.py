from typing import Final

from .absRecurringActionsEventHandler import AbsRecurringActionsEventHandler
from ..events.cutenessRecurringEvent import CutenessRecurringEvent
from ..events.superTriviaRecurringEvent import SuperTriviaRecurringEvent
from ..events.weatherRecurringEvent import WeatherRecurringEvent
from ..events.wordOfTheDayRecurringEvent import WordOfTheDayRecurringEvent
from ...cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from ...language.wordOfTheDay.wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from ...recurringActions.events.recurringEvent import RecurringEvent
from ...timber.timberInterface import TimberInterface
from ...twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider
from ...weather.weatherReportPresenterInterface import WeatherReportPresenterInterface


class RecurringActionsEventHandler(AbsRecurringActionsEventHandler):

    def __init__(
        self,
        cutenessPresenter: CutenessPresenterInterface | None,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        weatherReportPresenter: WeatherReportPresenterInterface | None,
        wordOfTheDayPresenter: WordOfTheDayPresenterInterface | None,
    ):
        if cutenessPresenter is not None and not isinstance(cutenessPresenter, CutenessPresenterInterface):
            raise TypeError(f'cutenessPresenter argument is malformed: \"{cutenessPresenter}\"')
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif weatherReportPresenter is not None and not isinstance(weatherReportPresenter, WeatherReportPresenterInterface):
            raise TypeError(f'weatherReportPresenter argument is malformed: \"{weatherReportPresenter}\"')
        elif wordOfTheDayPresenter is not None and not isinstance(wordOfTheDayPresenter, WordOfTheDayPresenterInterface):
            raise TypeError(f'wordOfTheDayPresenter argument is malformed: \"{wordOfTheDayPresenter}\"')

        self.__cutenessPresenter: Final[CutenessPresenterInterface | None] = cutenessPresenter
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__weatherReportPresenter: Final[WeatherReportPresenterInterface | None] = weatherReportPresenter
        self.__wordOfTheDayPresenter: Final[WordOfTheDayPresenterInterface | None] = wordOfTheDayPresenter

        self.__twitchConnectionReadinessProvider: TwitchConnectionReadinessProvider | None = None

    async def onNewRecurringActionEvent(self, event: RecurringEvent):
        if not isinstance(event, RecurringEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        self.__timber.log('RecurringActionsEventHandler', f'Received new recurring action event ({event=})')

        twitchConnectionReadinessProvider = self.__twitchConnectionReadinessProvider

        if twitchConnectionReadinessProvider is None:
            self.__timber.log('RecurringActionsEventHandler', f'Received new recurring action event, but it won\'t be handled, as the twitchConnectionReadinessProvider instances have not been set ({event=}) ({twitchConnectionReadinessProvider=})')
            return

        await twitchConnectionReadinessProvider.waitForReady()

        if isinstance(event, CutenessRecurringEvent):
            await self.__handleCutenessRecurringActionEvent(
                event = event,
            )

        elif isinstance(event, SuperTriviaRecurringEvent):
            await self.__handleSuperTriviaRecurringActionEvent(
                event = event,
            )

        elif isinstance(event, WeatherRecurringEvent):
            await self.__handleWeatherRecurringActionEvent(
                event = event,
            )

        elif isinstance(event, WordOfTheDayRecurringEvent):
            await self.__handleWordOfTheDayRecurringActionEvent(
                event = event,
            )

        else:
            self.__timber.log('RecurringActionsEventHandler', f'Received unhandled recurring action event ({event=})')

    async def __handleCutenessRecurringActionEvent(
        self,
        event: CutenessRecurringEvent,
    ):
        if self.__cutenessPresenter is None:
            return

        leaderboardString = await self.__cutenessPresenter.printLeaderboard(event.leaderboard)

        self.__twitchChatMessenger.send(
            text = leaderboardString,
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleSuperTriviaRecurringActionEvent(
        self,
        event: SuperTriviaRecurringEvent,
    ):
        self.__twitchChatMessenger.send(
            text = 'Super trivia starting soon!',
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleWeatherRecurringActionEvent(
        self,
        event: WeatherRecurringEvent,
    ):
        if self.__weatherReportPresenter is None:
            return

        weatherReportString = await self.__weatherReportPresenter.toString(event.weatherReport)

        self.__twitchChatMessenger.send(
            text = weatherReportString,
            twitchChannelId = event.twitchChannelId,
        )

    async def __handleWordOfTheDayRecurringActionEvent(
        self,
        event: WordOfTheDayRecurringEvent,
    ):
        if self.__wordOfTheDayPresenter is None:
            return

        wordOfTheDayString = await self.__wordOfTheDayPresenter.toString(
            includeRomaji = False,
            wordOfTheDay = event.wordOfTheDayResponse,
        )

        self.__twitchChatMessenger.send(
            text = wordOfTheDayString,
            twitchChannelId = event.twitchChannelId,
        )

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
