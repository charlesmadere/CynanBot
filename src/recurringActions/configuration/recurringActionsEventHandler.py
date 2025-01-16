from .absRecurringActionsEventHandler import AbsRecurringActionsEventHandler
from ..events.cutenessRecurringEvent import CutenessRecurringEvent
from ..events.superTriviaRecurringEvent import SuperTriviaRecurringEvent
from ..events.weatherRecurringEvent import WeatherRecurringEvent
from ..events.wordOfTheDayRecurringEvent import WordOfTheDayRecurringEvent
from ...cuteness.cutenessPresenterInterface import CutenessPresenterInterface
from ...language.wordOfTheDay.wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from ...recurringActions.events.recurringEvent import RecurringEvent
from ...timber.timberInterface import TimberInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...twitch.configuration.twitchConnectionReadinessProvider import TwitchConnectionReadinessProvider
from ...twitch.twitchUtilsInterface import TwitchUtilsInterface
from ...weather.weatherReportPresenterInterface import WeatherReportPresenterInterface


class RecurringActionsEventHandler(AbsRecurringActionsEventHandler):

    def __init__(
        self,
        cutenessPresenter: CutenessPresenterInterface | None,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        weatherReportPresenter: WeatherReportPresenterInterface | None,
        wordOfTheDayPresenter: WordOfTheDayPresenterInterface | None
    ):
        if cutenessPresenter is not None and not isinstance(cutenessPresenter, CutenessPresenterInterface):
            raise TypeError(f'cutenessPresenter argument is malformed: \"{cutenessPresenter}\"')
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif weatherReportPresenter is not None and not isinstance(weatherReportPresenter, WeatherReportPresenterInterface):
            raise TypeError(f'weatherReportPresenter argument is malformed: \"{weatherReportPresenter}\"')
        elif wordOfTheDayPresenter is not None and not isinstance(wordOfTheDayPresenter, WordOfTheDayPresenterInterface):
            raise TypeError(f'wordOfTheDayPresenter argument is malformed: \"{wordOfTheDayPresenter}\"')

        self.__cutenessPresenter: CutenessPresenterInterface | None = cutenessPresenter
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__weatherReportPresenter: WeatherReportPresenterInterface | None = weatherReportPresenter
        self.__wordOfTheDayPresenter: WordOfTheDayPresenterInterface | None = wordOfTheDayPresenter

        self.__twitchChannelProvider: TwitchChannelProvider | None = None
        self.__twitchConnectionReadinessProvider: TwitchConnectionReadinessProvider | None = None

    async def onNewRecurringActionEvent(self, event: RecurringEvent):
        if not isinstance(event, RecurringEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        self.__timber.log('RecurringActionsEventHandler', f'Received new recurring action event ({event=})')

        twitchChannelProvider = self.__twitchChannelProvider
        twitchConnectionReadinessProvider = self.__twitchConnectionReadinessProvider

        if twitchChannelProvider is None or twitchConnectionReadinessProvider is None:
            self.__timber.log('RecurringActionsEventHandler', f'Received new recurring action event, but it won\'t be handled, as the twitchChannelProvider and/or twitchConnectionReadinessProvider instances have not been set ({event=}) ({twitchChannelProvider=}) ({twitchConnectionReadinessProvider=})')
            return

        await twitchConnectionReadinessProvider.waitForReady()

        if isinstance(event, CutenessRecurringEvent):
            await self.__handleCutenessRecurringActionEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, SuperTriviaRecurringEvent):
            await self.__handleSuperTriviaRecurringActionEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, WeatherRecurringEvent):
            await self.__handleWeatherRecurringActionEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        elif isinstance(event, WordOfTheDayRecurringEvent):
            await self.__handleWordOfTheDayRecurringActionEvent(
                event = event,
                twitchChannelProvider = twitchChannelProvider
            )

        else:
            self.__timber.log('RecurringActionsEventHandler', f'Received unhandled recurring action event ({event=})')

    async def __handleCutenessRecurringActionEvent(
        self,
        event: CutenessRecurringEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        cutenessPresenter = self.__cutenessPresenter

        if cutenessPresenter is None:
            return

        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        leaderboardString = await cutenessPresenter.printLeaderboard(event.leaderboard)
        await self.__twitchUtils.safeSend(twitchChannel, leaderboardString)

    async def __handleSuperTriviaRecurringActionEvent(
        self,
        event: SuperTriviaRecurringEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        await self.__twitchUtils.safeSend(twitchChannel, 'Super trivia starting soon!')

    async def __handleWeatherRecurringActionEvent(
        self,
        event: WeatherRecurringEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        weatherReportPresenter = self.__weatherReportPresenter

        if weatherReportPresenter is None:
            return

        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)
        weatherReportString = await weatherReportPresenter.toString(event.weatherReport)
        await self.__twitchUtils.safeSend(twitchChannel, weatherReportString)

    async def __handleWordOfTheDayRecurringActionEvent(
        self,
        event: WordOfTheDayRecurringEvent,
        twitchChannelProvider: TwitchChannelProvider
    ):
        wordOfTheDayPresenter = self.__wordOfTheDayPresenter

        if wordOfTheDayPresenter is None:
            return

        twitchChannel = await twitchChannelProvider.getTwitchChannel(event.twitchChannel)

        wordOfTheDayString = await wordOfTheDayPresenter.toString(
            includeRomaji = False,
            wordOfTheDay = event.wordOfTheDayResponse
        )

        await self.__twitchUtils.safeSend(twitchChannel, wordOfTheDayString)

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider

    def setTwitchConnectionReadinessProvider(self, provider: TwitchConnectionReadinessProvider | None):
        if provider is not None and not isinstance(provider, TwitchConnectionReadinessProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchConnectionReadinessProvider = provider
