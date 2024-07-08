import asyncio
from asyncio import AbstractEventLoop
from typing import Any

from location.locationsRepository import LocationsRepository
from location.locationsRepositoryInterface import LocationsRepositoryInterface
from location.timeZoneRepository import TimeZoneRepository
from location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from network.aioHttpClientProvider import AioHttpClientProvider
from network.networkClientProvider import NetworkClientProvider
from openWeather.openWeatherApiKeyProvider import OpenWeatherApiKeyProvider
from openWeather.openWeatherApiService import OpenWeatherApiService
from openWeather.openWeatherApiServiceInterface import OpenWeatherApiServiceInterface
from openWeather.openWeatherJsonMapper import OpenWeatherJsonMapper
from openWeather.openWeatherJsonMapperInterface import OpenWeatherJsonMapperInterface
from storage.jsonStaticReader import JsonStaticReader
from timber.timberInterface import TimberInterface
from timber.timberStub import TimberStub
from weather.weatherReportPresenter import WeatherReportPresenter
from weather.weatherReportPresenterInterface import WeatherReportPresenterInterface
from weather.weatherRepository import WeatherRepository
from weather.weatherRepositoryInterface import WeatherRepositoryInterface


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
