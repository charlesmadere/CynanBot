import traceback

import CynanBot.misc.utils as utils
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.openWeather.exceptions import \
    OpenWeatherApiKeyUnavailableException
from CynanBot.openWeather.openWeatherAirQualityReport import \
    OpenWeatherAirQualityReport
from CynanBot.openWeather.openWeatherApiKeyProvider import \
    OpenWeatherApiKeyProvider
from CynanBot.openWeather.openWeatherApiServiceInterface import \
    OpenWeatherApiServiceInterface
from CynanBot.openWeather.openWeatherJsonMapperInterface import \
    OpenWeatherJsonMapperInterface
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport
from CynanBot.timber.timberInterface import TimberInterface


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

    async def fetchAirQuality(
        self,
        latitude: float,
        longitude: float
    ) -> OpenWeatherAirQualityReport:
        if not utils.isValidNum(latitude):
            raise TypeError(f'latitude argument is malformed: \"{latitude}\"')
        elif not utils.isValidNum(longitude):
            raise TypeError(f'longitude argument is malformed: \"{longitude}\"')

        self.__timber.log('OpenWeatherApiService', f'Fetching air quality index from OpenWeather... ({latitude=}) ({longitude=})')
        clientSession = await self.__networkClientProvider.get()

        openWeatherApiKey = await self.__openWeatherApiKeyProvider.getOpenWeatherApiKey()
        if not utils.isValidStr(openWeatherApiKey):
            raise OpenWeatherApiKeyUnavailableException(f'No OpenWeatherApiService API key is available: \"{openWeatherApiKey}\"')

        try:
            response = await clientSession.get(
                url = f''
            )
        except GenericNetworkException as e:
            self.__timber.log('OpenWeatherApiService', f'Encountererd network error when fetching weather ({latitude=}) ({longitude=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'OpenWeatherApiService encountered network error when fetching weather ({latitude=}) ({longitude=}): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('OpenWeatherApiService', f'Encountered non-200 HTTP status code when fetching weather ({latitude=}) ({longitude=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'OpenWeatherApiService encountered non-200 HTTP status code when fetching weather ({latitude=}) ({longitude=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        airQualityReport = await self.__openWeatherJsonMapper.parseAirQualityReport(jsonResponse)

        if airQualityReport is None:
            self.__timber.log('OpenWeatherApiService', f'Failed to parse JSON response into OpenWeatherAirQualityReport instance ({latitude=}) ({longitude=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({airQualityReport=})')
            raise GenericNetworkException(f'OpenWeatherApiService failed to parse JSON response into OpenWeatherAirQualityReport instance ({latitude=}) ({longitude=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({airQualityReport=})')

        return airQualityReport

    async def fetchWeatherReport(
        self,
        latitude: float,
        longitude: float
    ) -> OpenWeatherReport:
        if not utils.isValidNum(latitude):
            raise TypeError(f'latitude argument is malformed: \"{latitude}\"')
        elif not utils.isValidNum(longitude):
            raise TypeError(f'longitude argument is malformed: \"{longitude}\"')

        self.__timber.log('OpenWeatherApiService', f'Fetching weather report from OpenWeather... ({latitude=}) ({longitude=})')
        clientSession = await self.__networkClientProvider.get()

        openWeatherApiKey = await self.__openWeatherApiKeyProvider.getOpenWeatherApiKey()
        if not utils.isValidStr(openWeatherApiKey):
            raise OpenWeatherApiKeyUnavailableException(f'No OpenWeatherApiService API key is available: \"{openWeatherApiKey}\"')

        try:
            response = await clientSession.get(
                url = f'https://api.openweathermap.org/data/3.0/onecall?appid={openWeatherApiKey}&lang=en&lat={latitude}&lon={longitude}&exclude=minutely,hourly&units=metric'
            )
        except GenericNetworkException as e:
            self.__timber.log('OpenWeatherApiService', f'Encountererd network error when fetching weather ({latitude=}) ({longitude=}): {e}', e, traceback.format_exc())
            raise GenericNetworkException(f'OpenWeatherApiService encountered network error when fetching weather ({latitude=}) ({longitude=}): {e}')

        responseStatusCode = response.getStatusCode()
        jsonResponse = await response.json()
        await response.close()

        if responseStatusCode != 200:
            self.__timber.log('OpenWeatherApiService', f'Encountered non-200 HTTP status code when fetching weather ({latitude=}) ({longitude=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')
            raise GenericNetworkException(f'OpenWeatherApiService encountered non-200 HTTP status code when fetching weather ({latitude=}) ({longitude=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=})')

        weatherReport = await self.__openWeatherJsonMapper.parseWeatherReport(jsonResponse)

        if weatherReport is None:
            self.__timber.log('OpenWeatherApiService', f'Failed to parse JSON response into OpenWeatherReport instance ({latitude=}) ({longitude=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({weatherReport=})')
            raise GenericNetworkException(f'OpenWeatherApiService failed to parse JSON response into OpenWeatherReport instance ({latitude=}) ({longitude=}) ({responseStatusCode=}) ({response=}) ({jsonResponse=}) ({weatherReport=})')

        return weatherReport
