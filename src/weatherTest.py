import asyncio
from asyncio import AbstractEventLoop
from typing import Any

from CynanBot.location.locationsRepository import LocationsRepository
from CynanBot.location.locationsRepositoryInterface import \
    LocationsRepositoryInterface
from CynanBot.location.timeZoneRepository import TimeZoneRepository
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.network.aioHttpClientProvider import AioHttpClientProvider
from CynanBot.network.networkClientProvider import NetworkClientProvider
from CynanBot.openWeather.openWeatherApiKeyProvider import \
    OpenWeatherApiKeyProvider
from CynanBot.openWeather.openWeatherApiService import OpenWeatherApiService
from CynanBot.openWeather.openWeatherApiServiceInterface import \
    OpenWeatherApiServiceInterface
from CynanBot.openWeather.openWeatherJsonMapper import OpenWeatherJsonMapper
from CynanBot.openWeather.openWeatherJsonMapperInterface import \
    OpenWeatherJsonMapperInterface
from CynanBot.storage.jsonStaticReader import JsonStaticReader
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.timber.timberStub import TimberStub
from CynanBot.weather.weatherReportPresenter import WeatherReportPresenter
from CynanBot.weather.weatherReportPresenterInterface import \
    WeatherReportPresenterInterface
from CynanBot.weather.weatherRepository import WeatherRepository
from CynanBot.weather.weatherRepositoryInterface import \
    WeatherRepositoryInterface


class OpenWeatherApiKeyProviderStub(OpenWeatherApiKeyProvider):

    async def getOpenWeatherApiKey(self) -> str | None:
        return None

eventLoop: AbstractEventLoop = asyncio.get_event_loop()

timber: TimberInterface = TimberStub()

timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

locationsJson: dict[str, dict[str, Any]] = {
    "2128295": {
        "lat": 43.064171,
        "lon": 141.346939,
        "name": "Sapporo",
        "timeZone": "Japan"
    },
    "2643743": {
        "lat": 51.50853,
        "lon": -0.12574,
        "name": "London",
        "timeZone": "Europe/London"
    }
}

locationsRepository: LocationsRepositoryInterface = LocationsRepository(
    locationsJsonReader = JsonStaticReader(locationsJson),
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
    timber = timber
)

openWeatherJsonMapper: OpenWeatherJsonMapperInterface = OpenWeatherJsonMapper(
    timber = timber,
    timeZoneRepository = timeZoneRepository
)

openWeatherApiKeyProvider: OpenWeatherApiKeyProvider = OpenWeatherApiKeyProviderStub()

openWeatherApiService: OpenWeatherApiServiceInterface = OpenWeatherApiService(
    networkClientProvider = networkClientProvider,
    openWeatherApiKeyProvider = openWeatherApiKeyProvider,
    openWeatherJsonMapper = openWeatherJsonMapper,
    timber = timber
)

weatherReportPresenter: WeatherReportPresenterInterface = WeatherReportPresenter()

weatherRepository: WeatherRepositoryInterface = WeatherRepository(
    openWeatherApiKeyProvider = openWeatherApiKeyProvider,
    openWeatherApiService = openWeatherApiService,
    timber = timber
)

londonLocationId = '2643743'
sapporoLocationId = '2128295'

async def main():
    location = await locationsRepository.getLocation(sapporoLocationId)

    air = await openWeatherApiService.fetchAirPollutionReport(location)
    weatherReport = await openWeatherApiService.fetchWeatherReport(location)

    print(air)
    print(weatherReport)

    pass

eventLoop.run_until_complete(main())
