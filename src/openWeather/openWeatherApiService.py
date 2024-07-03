import traceback

from .exceptions import OpenWeatherApiKeyUnavailableException
from .openWeatherAirPollutionReport import OpenWeatherAirPollutionReport
from .openWeatherApiKeyProvider import OpenWeatherApiKeyProvider
from .openWeatherApiServiceInterface import OpenWeatherApiServiceInterface
from .openWeatherJsonMapperInterface import OpenWeatherJsonMapperInterface
from .openWeatherReport import OpenWeatherReport
from ..location.location import Location
from ..misc import utils as utils
from ..network.exceptions import GenericNetworkException
from ..network.networkClientProvider import NetworkClientProvider
from ..timber.timberInterface import TimberInterface


class OpenWeatherApiService(OpenWeatherApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        openWeatherApiKeyProvider: OpenWeatherApiKeyProvider,
        openWeatherJsonMapper: OpenWeatherJsonMapperInterface,
        timber: TimberInterface
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(openWeatherApiKeyProvider, OpenWeatherApiKeyProvider):
            raise TypeError(f'openWeatherApiKeyProvider argument is malformed: \"{openWeatherApiKeyProvider}\"')
        elif not isinstance(openWeatherJsonMapper, OpenWeatherJsonMapperInterface):
            raise TypeError(f'openWeatherJsonMapper argument is malformed: \"{openWeatherJsonMapper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__openWeatherApiKeyProvider: OpenWeatherApiKeyProvider = openWeatherApiKeyProvider
        self.__openWeatherJsonMapper: OpenWeatherJsonMapperInterface = openWeatherJsonMapper
        self.__timber: TimberInterface = timber

    async def fetchAirPollutionReport(self, location: Location) -> OpenWeatherAirPollutionReport:
        if not isinstance(location, Location):
            raise TypeError(f'location argument is malformed: \"{location}\"')

        self.__timber.log('OpenWeatherApiService', f'Fetching air quality index from OpenWeather... ({location=})')
        clientSession = await self.__networkClientProvider.get()

        openWeatherApiKey = await self.__openWeatherApiKeyProvider.getOpenWeatherApiKey()
        if not utils.isValidStr(openWeatherApiKey):
            raise OpenWeatherApiKeyUnavailableException(f'No OpenWeatherApiService API key is available: \"{openWeatherApiKey}\"')

        try:
            response = await clientSession.get(
                url = f'http://api.openweathermap.org/data/2.5/air_pollution?appid={openWeatherApiKey}&lat={location.latitude}&lon={location.longitude}'
            )
        except GenericNetworkException as e:
            self.__timber.log('OpenWeatherApiService', f'Encountererd network error when fetching weather ({location=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'OpenWeatherApiService encountered network error when fetching weather ({location=}): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('OpenWeatherApiService', f'Encountered non-200 HTTP status code when fetching weather ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'OpenWeatherApiService encountered non-200 HTTP status code when fetching weather ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        airPollutionReport = await self.__openWeatherJsonMapper.parseAirPollutionReport(
            jsonContents = jsonResponse,
            timeZone = location.timeZone
        )

        if airPollutionReport is None:
            self.__timber.log('OpenWeatherApiService', f'Failed to parse JSON response into OpenWeatherAirPollutionReport instance ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({airPollutionReport=})')
            raise GenericNetworkException(f'OpenWeatherApiService failed to parse JSON response into OpenWeatherAirPollutionReport instance ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({airPollutionReport=})')

        return airPollutionReport

    async def fetchWeatherReport(self, location: Location) -> OpenWeatherReport:
        if not isinstance(location, Location):
            raise TypeError(f'location argument is malformed: \"{location}\"')

        self.__timber.log('OpenWeatherApiService', f'Fetching weather report from OpenWeather... ({location=})')
        clientSession = await self.__networkClientProvider.get()

        openWeatherApiKey = await self.__openWeatherApiKeyProvider.getOpenWeatherApiKey()
        if not utils.isValidStr(openWeatherApiKey):
            raise OpenWeatherApiKeyUnavailableException(f'No OpenWeatherApiService API key is available: \"{openWeatherApiKey}\"')

        try:
            response = await clientSession.get(
                url = f'https://api.openweathermap.org/data/3.0/onecall?appid={openWeatherApiKey}&lang=en&lat={location.latitude}&lon={location.longitude}&exclude=minutely,hourly&units=metric'
            )
        except GenericNetworkException as e:
            self.__timber.log('OpenWeatherApiService', f'Encountererd network error when fetching weather ({location=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'OpenWeatherApiService encountered network error when fetching weather ({location=}): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('OpenWeatherApiService', f'Encountered non-200 HTTP status code when fetching weather ({location=})) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'OpenWeatherApiService encountered non-200 HTTP status code when fetching weather ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        weatherReport = await self.__openWeatherJsonMapper.parseWeatherReport(jsonResponse)

        if weatherReport is None:
            self.__timber.log('OpenWeatherApiService', f'Failed to parse JSON response into OpenWeatherReport instance ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({weatherReport=})')
            raise GenericNetworkException(f'OpenWeatherApiService failed to parse JSON response into OpenWeatherReport instance ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({weatherReport=})')

        return weatherReport
