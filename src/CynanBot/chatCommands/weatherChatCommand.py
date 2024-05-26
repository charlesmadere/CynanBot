import traceback
from datetime import timedelta

import CynanBot.misc.utils as utils
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.location.locationsRepositoryInterface import \
    LocationsRepositoryInterface
from CynanBot.misc.timedDict import TimedDict
from CynanBot.openWeather.exceptions import \
    OpenWeatherApiKeyUnavailableException
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface
from CynanBot.weather.weatherReportPresenterInterface import \
    WeatherReportPresenterInterface
from CynanBot.weather.weatherRepositoryInterface import \
    WeatherRepositoryInterface


class WeatherChatCommand(AbsChatCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        locationsRepository: LocationsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        weatherReportPresenter: WeatherReportPresenterInterface,
        weatherRepository: WeatherRepositoryInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(locationsRepository, LocationsRepositoryInterface):
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

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__locationsRepository: LocationsRepositoryInterface = locationsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__weatherReportPresenter: WeatherReportPresenterInterface = weatherReportPresenter
        self.__weatherRepository: WeatherRepositoryInterface = weatherRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isWeatherEnabled() or not user.isWeatherEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        locationId = user.getLocationId()

        if not utils.isValidStr(locationId):
            await self.__twitchUtils.safeSend(ctx, f'⚠ Weather for {user.getHandle()} is enabled, but no location ID is available')
            return

        location = await self.__locationsRepository.getLocation(locationId)

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

        self.__timber.log('WeatherCommand', f'Handled !weather command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
