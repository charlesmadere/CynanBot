import asyncio
from asyncio import AbstractEventLoop
from typing import Any

from src.location.locationsRepository import LocationsRepository
from src.location.locationsRepositoryInterface import LocationsRepositoryInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.network.aioHttp.aioHttpClientProvider import AioHttpClientProvider
from src.network.aioHttp.aioHttpCookieJarProvider import AioHttpCookieJarProvider
from src.network.networkClientProvider import NetworkClientProvider
from src.openWeather.apiService.openWeatherApiKeyProvider import OpenWeatherApiKeyProvider
from src.openWeather.apiService.openWeatherApiService import OpenWeatherApiService
from src.openWeather.apiService.openWeatherApiServiceInterface import OpenWeatherApiServiceInterface
from src.openWeather.jsonMapper.openWeatherJsonMapper import OpenWeatherJsonMapper
from src.openWeather.jsonMapper.openWeatherJsonMapperInterface import OpenWeatherJsonMapperInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.weather.weatherReportPresenter import WeatherReportPresenter
from src.weather.weatherReportPresenterInterface import WeatherReportPresenterInterface
from src.weather.weatherRepository import WeatherRepository
from src.weather.weatherRepositoryInterface import WeatherRepositoryInterface


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

aioHttpCookieJarProvider = AioHttpCookieJarProvider(
    eventLoop = eventLoop
)

networkClientProvider: NetworkClientProvider = AioHttpClientProvider(
    eventLoop = eventLoop,
    cookieJarProvider = aioHttpCookieJarProvider,
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
