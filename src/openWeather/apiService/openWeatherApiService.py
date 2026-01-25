import traceback
import urllib.parse
from typing import Final

from .openWeatherApiKeyProvider import OpenWeatherApiKeyProvider
from .openWeatherApiServiceInterface import OpenWeatherApiServiceInterface
from ..exceptions import OpenWeatherApiKeyUnavailableException
from ..jsonMapper.openWeatherJsonMapperInterface import OpenWeatherJsonMapperInterface
from ..models.openWeatherAirPollutionReport import OpenWeatherAirPollutionReport
from ..models.openWeatherReport import OpenWeatherReport
from ...location.location import Location
from ...misc import utils as utils
from ...network.exceptions import GenericNetworkException
from ...network.networkClientProvider import NetworkClientProvider
from ...timber.timberInterface import TimberInterface


class OpenWeatherApiService(OpenWeatherApiServiceInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        openWeatherApiKeyProvider: OpenWeatherApiKeyProvider,
        openWeatherJsonMapper: OpenWeatherJsonMapperInterface,
        timber: TimberInterface,
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(openWeatherApiKeyProvider, OpenWeatherApiKeyProvider):
            raise TypeError(f'openWeatherApiKeyProvider argument is malformed: \"{openWeatherApiKeyProvider}\"')
        elif not isinstance(openWeatherJsonMapper, OpenWeatherJsonMapperInterface):
            raise TypeError(f'openWeatherJsonMapper argument is malformed: \"{openWeatherJsonMapper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__networkClientProvider: Final[NetworkClientProvider] = networkClientProvider
        self.__openWeatherApiKeyProvider: Final[OpenWeatherApiKeyProvider] = openWeatherApiKeyProvider
        self.__openWeatherJsonMapper: Final[OpenWeatherJsonMapperInterface] = openWeatherJsonMapper
        self.__timber: Final[TimberInterface] = timber

    async def fetchAirPollutionReport(self, location: Location) -> OpenWeatherAirPollutionReport:
        if not isinstance(location, Location):
            raise TypeError(f'location argument is malformed: \"{location}\"')

        self.__timber.log('OpenWeatherApiService', f'Fetching air pollution report from OpenWeather... ({location=})')
        clientSession = await self.__networkClientProvider.get()
        openWeatherApiKey = await self.__requireOpenWeatherApiKey()

        queryString = urllib.parse.urlencode({
            'appid': openWeatherApiKey,
            'lat': location.latitude,
            'lon': location.longitude,
        })

        try:
            response = await clientSession.get(
                url = f'http://api.openweathermap.org/data/2.5/air_pollution?{queryString}'
            )
        except GenericNetworkException as e:
            self.__timber.log('OpenWeatherApiService', f'Encountered network error when fetching weather ({location=})', e, traceback.format_exc())
            raise GenericNetworkException(f'OpenWeatherApiService encountered network error when fetching weather ({location=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('OpenWeatherApiService', f'Encountered non-200 HTTP status code when fetching weather ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(
                message = f'OpenWeatherApiService encountered non-200 HTTP status code when fetching weather ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})',
                statusCode = responseStatusCode,
            )

        airPollutionReport = await self.__openWeatherJsonMapper.parseAirPollutionReport(
            jsonContents = jsonResponse,
            timeZone = location.timeZone,
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
        openWeatherApiKey = await self.__requireOpenWeatherApiKey()

        queryString = urllib.parse.urlencode({
            'appid': openWeatherApiKey,
            'exclude': 'minutely,hourly',
            'lang': 'en',
            'lat': location.latitude,
            'lon': location.longitude,
            'units': 'metric',
        })

        try:
            response = await clientSession.get(
                url = f'https://api.openweathermap.org/data/3.0/onecall?{queryString}'
            )
        except GenericNetworkException as e:
            self.__timber.log('OpenWeatherApiService', f'Encountered network error when fetching weather ({location=})', e, traceback.format_exc())
            raise GenericNetworkException(f'OpenWeatherApiService encountered network error when fetching weather ({location=}): {e}')

        responseStatusCode = response.statusCode
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('OpenWeatherApiService', f'Encountered non-200 HTTP status code when fetching weather ({location=})) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(
                message = f'OpenWeatherApiService encountered non-200 HTTP status code when fetching weather ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})',
                statusCode = responseStatusCode,
            )

        weatherReport = await self.__openWeatherJsonMapper.parseWeatherReport(jsonResponse)

        if weatherReport is None:
            self.__timber.log('OpenWeatherApiService', f'Failed to parse JSON response into OpenWeatherReport instance ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({weatherReport=})')
            raise GenericNetworkException(f'OpenWeatherApiService failed to parse JSON response into OpenWeatherReport instance ({location=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({weatherReport=})')

        return weatherReport

    async def __requireOpenWeatherApiKey(self) -> str:
        openWeatherApiKey = await self.__openWeatherApiKeyProvider.getOpenWeatherApiKey()

        if not utils.isValidStr(openWeatherApiKey):
            raise OpenWeatherApiKeyUnavailableException(f'No OpenWeatherApiService API key is available: \"{openWeatherApiKey}\"')

        return openWeatherApiKey
