import traceback
from datetime import timedelta
from typing import Final

from .absChatCommand import AbsChatCommand
from ..location.exceptions import NoSuchLocationException
from ..location.locationsRepositoryInterface import LocationsRepositoryInterface
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..openWeather.exceptions import OpenWeatherApiKeyUnavailableException
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface
from ..weather.weatherReportPresenterInterface import WeatherReportPresenterInterface
from ..weather.weatherRepositoryInterface import WeatherRepositoryInterface


class WeatherChatCommand(AbsChatCommand):

    def __init__(
        self,
        locationsRepository: LocationsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
        weatherReportPresenter: WeatherReportPresenterInterface,
        weatherRepository: WeatherRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(locationsRepository, LocationsRepositoryInterface):
            raise TypeError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(weatherReportPresenter, WeatherReportPresenterInterface):
            raise TypeError(f'weatherReportPresenter argument is malformed: \"{weatherReportPresenter}\"')
        elif not isinstance(weatherRepository, WeatherRepositoryInterface):
            raise TypeError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__locationsRepository: Final[LocationsRepositoryInterface] = locationsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__weatherReportPresenter: WeatherReportPresenterInterface = weatherReportPresenter
        self.__weatherRepository: WeatherRepositoryInterface = weatherRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isWeatherEnabled:
            return
        elif not ctx.isAuthorMod and not ctx.isAuthorVip and not self.__lastMessageTimes.isReadyAndUpdate(user.handle):
            return

        locationId = user.locationId
        if not utils.isValidStr(locationId):
            self.__timber.log('WeatherCommand', f'No location ID found when fetching weather for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            return

        try:
            location = await self.__locationsRepository.getLocation(locationId)
        except NoSuchLocationException as e:
            self.__timber.log('WeatherCommand', f'Unable to get location when fetching weather for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({locationId=})', e, traceback.format_exc())
            return

        try:
            weatherReport = await self.__weatherRepository.fetchWeather(
                location = location,
            )

            weatherReportString = await self.__weatherReportPresenter.toString(
                weather = weatherReport,
            )

            self.__twitchChatMessenger.send(
                text = weatherReportString,
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        except OpenWeatherApiKeyUnavailableException as e:
            self.__timber.log('WeatherCommand', f'OpenWeather API key unavailable when fetching weather for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({locationId=})', e, traceback.format_exc())
        except Exception as e:
            self.__timber.log('WeatherCommand', f'Error fetching weather for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({locationId=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = '⚠ Error fetching weather',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('WeatherCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
