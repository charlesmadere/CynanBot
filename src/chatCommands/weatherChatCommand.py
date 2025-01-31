import traceback
from datetime import timedelta

from .absChatCommand import AbsChatCommand
from ..location.exceptions import NoSuchLocationException
from ..location.locationsRepositoryInterface import LocationsRepositoryInterface
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..openWeather.exceptions import OpenWeatherApiKeyUnavailableException
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface
from ..weather.weatherReportPresenterInterface import WeatherReportPresenterInterface
from ..weather.weatherRepositoryInterface import WeatherRepositoryInterface


class WeatherChatCommand(AbsChatCommand):

    def __init__(
        self,
        locationsRepository: LocationsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        weatherReportPresenter: WeatherReportPresenterInterface,
        weatherRepository: WeatherRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(locationsRepository, LocationsRepositoryInterface):
            raise TypeError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(weatherReportPresenter, WeatherReportPresenterInterface):
            raise TypeError(f'weatherReportPresenter argument is malformed: \"{weatherReportPresenter}\"')
        elif not isinstance(weatherRepository, WeatherRepositoryInterface):
            raise TypeError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__locationsRepository: LocationsRepositoryInterface = locationsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
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
            await self.__twitchUtils.safeSend(ctx, f'⚠ Weather for {user.handle} is enabled, but no location ID is available')
            return

        try:
            location = await self.__locationsRepository.getLocation(locationId)
        except NoSuchLocationException as e:
            self.__timber.log('WeatherCommand', f'Unable to get location ID when fetching weather for {ctx.getAuthorName()}:{ctx.getAuthorId()} ({locationId=}): {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error fetching your user account\'s location ID')
            return

        try:
            weatherReport = await self.__weatherRepository.fetchWeather(location)
            weatherReportString = await self.__weatherReportPresenter.toString(weatherReport)
            await self.__twitchUtils.safeSend(ctx, weatherReportString)
        except OpenWeatherApiKeyUnavailableException as e:
            self.__timber.log('WeatherCommand', f'Unable to fetch weather for \"{locationId}\" as no OpenWeather API key is available: {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, '⚠ Error fetching weather')
        except (RuntimeError, ValueError) as e:
            self.__timber.log('WeatherCommand', f'Error fetching weather for \"{locationId}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, '⚠ Error fetching weather')

        self.__timber.log('WeatherCommand', f'Handled !weather command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
