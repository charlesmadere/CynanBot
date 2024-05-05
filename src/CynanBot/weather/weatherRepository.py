import traceback
from datetime import timedelta
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.location.location import Location
from CynanBot.misc.timedDict import TimedDict
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.network.networkHandle import NetworkHandle
from CynanBot.openWeather.exceptions import \
    OpenWeatherApiKeyUnavailableException
from CynanBot.openWeather.openWeatherApiKeyProvider import \
    OpenWeatherApiKeyProvider
from CynanBot.openWeather.openWeatherApiServiceInterface import \
    OpenWeatherApiServiceInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.weather.airQualityIndex import AirQualityIndex
from CynanBot.weather.uvIndex import UvIndex
from CynanBot.weather.weatherReport import WeatherReport
from CynanBot.weather.weatherRepositoryInterface import \
    WeatherRepositoryInterface


class WeatherRepository(WeatherRepositoryInterface):

    def __init__(
        self,
        networkClientProvider: NetworkClientProvider,
        openWeatherApiKeyProvider: OpenWeatherApiKeyProvider,
        openWeatherApiService: OpenWeatherApiServiceInterface,
        timber: TimberInterface,
        maxAlerts: int = 2,
        cacheTimeDelta: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(networkClientProvider, NetworkClientProvider):
            raise TypeError(f'networkClientProvider argument is malformed: \"{networkClientProvider}\"')
        elif not isinstance(openWeatherApiKeyProvider, OpenWeatherApiKeyProvider):
            raise TypeError(f'openWeatherApiKeyProvider argument is malformed: \"{openWeatherApiKeyProvider}\"')
        elif not isinstance(openWeatherApiService, OpenWeatherApiServiceInterface):
            raise TypeError(f'openWeatherApiService argument is malformed: \"{openWeatherApiService}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(maxAlerts):
            raise TypeError(f'maxAlerts argument is malformed: \"{maxAlerts}\"')
        elif maxAlerts < 1 or maxAlerts > 3:
            raise ValueError(f'maxAlerts argument is out of bounds: {maxAlerts}')
        elif not isinstance(cacheTimeDelta, timedelta):
            raise TypeError(f'cacheTimeDelta argument is malformed: \"{cacheTimeDelta}\"')

        self.__networkClientProvider: NetworkClientProvider = networkClientProvider
        self.__openWeatherApiKeyProvider: OpenWeatherApiKeyProvider = openWeatherApiKeyProvider
        self.__openWeatherApiService: OpenWeatherApiServiceInterface = openWeatherApiService
        self.__timber: TimberInterface = timber
        self.__maxAlerts: int = maxAlerts

        self.__cache: TimedDict[WeatherReport] = TimedDict(cacheTimeDelta)
        self.__conditionIcons: dict[str, str] = self.__createConditionIconsDict()

    async def __chooseTomorrowFromForecast(self, jsonResponse: dict[str, Any]) -> dict[str, Any]:
        currentSunrise = jsonResponse['current']['sunrise']
        currentSunset = jsonResponse['current']['sunset']

        for dayJson in jsonResponse['daily']:
            if dayJson['sunrise'] > currentSunrise and dayJson['sunset'] > currentSunset:
                return dayJson

        raise RuntimeError(f'Unable to find viable tomorrow data in JSON response: \"{jsonResponse}\"')

    async def clearCaches(self):
        self.__cache.clear()
        self.__timber.log('WeatherRepository', 'Caches cleared')

    def __createConditionIconsDict(self) -> dict[str, str]:
        # This dictionary is built from the Weather Condition Codes listed here:
        # https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2

        icons: dict[str, str] = dict()
        icons['200'] = '⛈️'
        icons['201'] = icons['200']
        icons['202'] = icons['200']
        icons['210'] = '🌩️'
        icons['211'] = icons['210']
        icons['212'] = icons['211']
        icons['221'] = icons['200']
        icons['230'] = icons['200']
        icons['231'] = icons['200']
        icons['232'] = icons['200']
        icons['300'] = '☔'
        icons['301'] = icons['300']
        icons['310'] = icons['300']
        icons['311'] = icons['300']
        icons['313'] = icons['300']
        icons['500'] = icons['300']
        icons['501'] = '🌧️'
        icons['502'] = icons['501']
        icons['503'] = icons['501']
        icons['504'] = icons['501']
        icons['520'] = icons['501']
        icons['521'] = icons['501']
        icons['522'] = icons['501']
        icons['531'] = icons['501']
        icons['600'] = '❄️'
        icons['601'] = icons['600']
        icons['602'] = '🌨️'
        icons['711'] = '🌫️'
        icons['721'] = icons['711']
        icons['731'] = icons['711']
        icons['741'] = icons['711']
        icons['762'] = '🌋'
        icons['771'] = '🌬'
        icons['781'] = '🌪️'
        icons['801'] = '☁️'
        icons['802'] = icons['801']
        icons['803'] = icons['801']
        icons['804'] = icons['801']

        return icons

    async def __fetchAirQualityIndex(
        self,
        location: Location,
        clientSession: NetworkHandle,
        openWeatherApiKey: str
    ) -> AirQualityIndex | None:
        if not isinstance(location, Location):
            raise TypeError(f'location argument is malformed: \"{location}\"')
        elif not isinstance(clientSession, NetworkHandle):
            raise TypeError(f'clientSession argument is malformed: \"{clientSession}\"')
        elif not utils.isValidStr(openWeatherApiKey):
            raise TypeError(f'openWeatherApiKey argument is malformed: \"{openWeatherApiKey}\"')

        # Retrieve air quality index from: https://openweathermap.org/api/air-pollution
        # Doing this requires an API key, which you can get here: https://openweathermap.org/api

        requestUrl = 'https://api.openweathermap.org/data/2.5/air_pollution?appid={}&lat={}&lon={}'.format(
            openWeatherApiKey, location.getLatitude(), location.getLongitude())

        try:
            response = await clientSession.get(requestUrl)
        except GenericNetworkException as e:
            self.__timber.log('WeatherRepository', f'Encountered network error when fetching air quality index for \"{location.getName()}\" ({location.getLocationId()}): {e}', e, traceback.format_exc())
            return None

        if response.getStatusCode() != 200:
            self.__timber.log('WeatherRepository', f'Encountered non-200 HTTP status code when fetching air quality index for \"{location.getName()}\" ({location.getLocationId()}): {response.getStatusCode()}')
            return None

        jsonResponse = await response.json()
        await response.close()

        if not utils.hasItems(jsonResponse) or not isinstance(jsonResponse, dict):
            self.__timber.log('WeatherRepository', f'Received null/empty JSON response when fetching air quality index for \"{location.getName()}\" ({location.getLocationId()})')
            return None

        airQualityIndex = utils.getIntFromDict(
            d = jsonResponse['list'][0]['main'],
            key = 'aqi',
            fallback = -1
        )

        if airQualityIndex == -1:
            return None
        else:
            return AirQualityIndex.fromInt(airQualityIndex)

    async def fetchWeather(self, location: Location) -> WeatherReport:
        if not isinstance(location, Location):
            raise TypeError(f'location argument is malformed: \"{location}\"')

        weatherReport = self.__cache[location.getLocationId()]
        if weatherReport is not None:
            return weatherReport

        weatherReport = await self.__fetchWeather(location)
        self.__cache[location.getLocationId()] = weatherReport

        return weatherReport

    async def __fetchWeather(self, location: Location) -> WeatherReport:
        if not isinstance(location, Location):
            raise TypeError(f'location argument is malformed: \"{location}\"')

        openWeatherApiKey = await self.__openWeatherApiKeyProvider.getOpenWeatherApiKey()
        if not utils.isValidStr(openWeatherApiKey):
            raise OpenWeatherApiKeyUnavailableException(f'OpenWeather API key unavailable when fetching weather ({location=}) ({openWeatherApiKey=})')

        self.__timber.log('WeatherRepository', f'Fetching weather for \"{location.getName()}\" ({location.getLocationId()})...')
        clientSession = await self.__networkClientProvider.get()

        # Retrieve weather report from https://openweathermap.org/api/one-call-api
        # Doing this requires an API key, which you can get here: https://openweathermap.org/api

        requestUrl = 'https://api.openweathermap.org/data/2.5/onecall?appid={}&lat={}&lon={}&exclude=minutely,hourly&units=metric'.format(
            openWeatherApiKey, location.getLatitude(), location.getLongitude())

        try:
            response = await clientSession.get(requestUrl)
        except GenericNetworkException as e:
            self.__timber.log('WeatherRepository', f'Encountered network error when fetching weather for \"{location.getName()}\" ({location.getLocationId()}): {e}', e, traceback.format_exc())
            raise RuntimeError(f'Encountered network error when fetching weather for \"{location.getName()}\" ({location.getLocationId()})')

        if response.getStatusCode() != 200:
            self.__timber.log('WeatherRepository', f'Encountered non-200 HTTP status code when fetching weather for \"{location.getName()}\" ({location.getLocationId()}): {response.getStatusCode()}')
            raise RuntimeError(f'Encountered network error when fetching weather for \"{location.getName()}\" ({location.getLocationId()})')

        jsonResponse = await response.json()
        await response.close()

        if not isinstance(jsonResponse, dict) or len(jsonResponse) == 0:
            self.__timber.log('WeatherRepository', f'Received null/empty JSON response when fetching weather for \"{location.getName()}\" ({location.getLocationId()}): {jsonResponse}')
            raise RuntimeError(f'WeatherRepository received null/empty JSON response when fetching weather for \"{location.getName()}\" ({location.getLocationId()}): {jsonResponse}')

        currentJson: dict[str, Any] = jsonResponse['current']
        humidity = int(round(utils.getFloatFromDict(currentJson, 'humidity')))
        pressure = int(round(utils.getFloatFromDict(currentJson, 'pressure')))
        temperature = utils.getFloatFromDict(currentJson, 'temp')
        uvIndex = UvIndex.fromFloat(utils.getFloatFromDict(currentJson, 'uvi'))

        conditions: list[str] = list()
        if 'weather' in currentJson and len(currentJson['weather']) >= 1:
            for conditionJson in currentJson['weather']:
                conditions.append(await self.__prettifyCondition(conditionJson))

        alerts: list[str] = list()
        if 'alerts' in jsonResponse and len(jsonResponse['alerts']) >= 1:
            for alertJson in jsonResponse['alerts']:
                event = alertJson.get('event')
                senderName = alertJson.get('sender_name')

                if event is not None and len(event) >= 1:
                    if senderName is None or len(senderName) == 0:
                        alerts.append(f'Alert: {event}.')
                    else:
                        alerts.append(f'Alert from {senderName}: {event}.')

                    if len(alerts) >= self.__maxAlerts:
                        break

        tomorrowsJson = await self.__chooseTomorrowFromForecast(jsonResponse)
        tomorrowsHighTemperature = utils.getFloatFromDict(tomorrowsJson['temp'], 'max')
        tomorrowsLowTemperature = utils.getFloatFromDict(tomorrowsJson['temp'], 'min')

        tomorrowsConditions: list[str] = list()
        if 'weather' in tomorrowsJson and len(tomorrowsJson['weather']) >= 1:
            for conditionJson in tomorrowsJson['weather']:
                tomorrowsConditions.append(conditionJson['description'])

        airQualityIndex = await self.__fetchAirQualityIndex(
            location = location,
            clientSession = clientSession,
            openWeatherApiKey = openWeatherApiKey
        )

        return WeatherReport(
            airQualityIndex = airQualityIndex,
            temperature = temperature,
            tomorrowsHighTemperature = tomorrowsHighTemperature,
            tomorrowsLowTemperature = tomorrowsLowTemperature,
            humidity = humidity,
            pressure = pressure,
            alerts = alerts,
            conditions = conditions,
            tomorrowsConditions = tomorrowsConditions,
            locationId = location.getLocationId(),
            uvIndex = uvIndex
        )

    async def isAvailable(self) -> bool:
        openWeatherApiKey = await self.__openWeatherApiKeyProvider.getOpenWeatherApiKey()
        return utils.isValidStr(openWeatherApiKey)

    async def __prettifyCondition(self, conditionJson: dict[Any, Any]) -> str:
        conditionIcon = ''
        if 'id' in conditionJson:
            conditionId = utils.getStrFromDict(conditionJson, 'id')

            if conditionId in self.__conditionIcons:
                icon = self.__conditionIcons[conditionId]
                conditionIcon = f'{icon} '

        conditionDescription = utils.getStrFromDict(conditionJson, 'description')
        return f'{conditionIcon}{conditionDescription}'.strip()
