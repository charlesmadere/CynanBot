import traceback
from datetime import timedelta

from .weatherReport import WeatherReport
from .weatherRepositoryInterface import WeatherRepositoryInterface
from ..location.location import Location
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..network.exceptions import GenericNetworkException
from ..openWeather.apiService.openWeatherApiKeyProvider import OpenWeatherApiKeyProvider
from ..openWeather.apiService.openWeatherApiServiceInterface import OpenWeatherApiServiceInterface
from ..openWeather.exceptions import OpenWeatherApiKeyUnavailableException
from ..openWeather.models.openWeatherAirPollutionReport import OpenWeatherAirPollutionReport
from ..timber.timberInterface import TimberInterface


class WeatherRepository(WeatherRepositoryInterface):

    def __init__(
        self,
        openWeatherApiKeyProvider: OpenWeatherApiKeyProvider,
        openWeatherApiService: OpenWeatherApiServiceInterface,
        timber: TimberInterface,
        cacheTimeDelta: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(openWeatherApiKeyProvider, OpenWeatherApiKeyProvider):
            raise TypeError(f'openWeatherApiKeyProvider argument is malformed: \"{openWeatherApiKeyProvider}\"')
        elif not isinstance(openWeatherApiService, OpenWeatherApiServiceInterface):
            raise TypeError(f'openWeatherApiService argument is malformed: \"{openWeatherApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__openWeatherApiKeyProvider: OpenWeatherApiKeyProvider = openWeatherApiKeyProvider
        self.__openWeatherApiService: OpenWeatherApiServiceInterface = openWeatherApiService
        self.__timber: TimberInterface = timber

        self.__cache: TimedDict[WeatherReport] = TimedDict(cacheTimeDelta)

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('WeatherRepository', 'Caches cleared')

    async def fetchWeather(self, location: Location) -> WeatherReport:
        if not isinstance(location, Location):
            raise TypeError(f'location argument is malformed: \"{location}\"')

        weatherReport = self.__cache[location.locationId]
        if weatherReport is not None:
            return weatherReport

        weatherReport = await self.__fetchWeather(location)
        self.__cache[location.locationId] = weatherReport

        return weatherReport

    async def __fetchWeather(self, location: Location) -> WeatherReport:
        if not isinstance(location, Location):
            raise TypeError(f'location argument is malformed: \"{location}\"')

        openWeatherApiKey = await self.__openWeatherApiKeyProvider.getOpenWeatherApiKey()
        if not utils.isValidStr(openWeatherApiKey):
            raise OpenWeatherApiKeyUnavailableException(f'OpenWeather API key unavailable when fetching weather ({location=}) ({openWeatherApiKey=})')

        self.__timber.log('WeatherRepository', f'Fetching weather... ({location=})')
        airPollutionReport: OpenWeatherAirPollutionReport | None = None

        try:
            airPollutionReport = await self.__openWeatherApiService.fetchAirPollutionReport(location)
        except GenericNetworkException as e:
            self.__timber.log('WeatherRepository', f'Encountered network error when fetching air pollution ({location=}): {e}', e, traceback.format_exc())

        try:
            weatherReport = await self.__openWeatherApiService.fetchWeatherReport(location)
        except GenericNetworkException as e:
            self.__timber.log('WeatherRepository', f'Encountered network error when fetching weather ({location=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'WeatherRepository encountered network error when fetching weather ({location=}): {e}')

        return WeatherReport(
            location = location,
            airPollution = airPollutionReport,
            report = weatherReport
        )

    async def isAvailable(self) -> bool:
        openWeatherApiKey = await self.__openWeatherApiKeyProvider.getOpenWeatherApiKey()
        return utils.isValidStr(openWeatherApiKey)
