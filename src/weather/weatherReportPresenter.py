import locale
from datetime import datetime
from typing import Final

from .weatherReport import WeatherReport
from .weatherReportPresenterInterface import WeatherReportPresenterInterface
from ..misc import utils as utils
from ..openWeather.models.openWeatherAirPollutionIndex import OpenWeatherAirPollutionIndex
from ..openWeather.models.openWeatherDay import OpenWeatherDay


class WeatherReportPresenter(WeatherReportPresenterInterface):

    def __init__(
        self,
        maxAlerts: int = 1,
        maxConditions: int = 2,
        maxTomorrowsConditions: int = 1,
    ):
        if not utils.isValidInt(maxAlerts):
            raise TypeError(f'maxAlerts argument is malformed: \"{maxAlerts}\"')
        elif maxAlerts < 1 or maxAlerts > utils.getIntMaxSafeSize():
            raise ValueError(f'maxAlerts argument is out of bounds: {maxAlerts}')
        elif not utils.isValidInt(maxConditions):
            raise TypeError(f'maxConditions argument is malformed: \"{maxConditions}\"')
        elif maxConditions < 1 or maxConditions > utils.getIntMaxSafeSize():
            raise ValueError(f'maxConditions argument is out of bounds: {maxConditions}')
        elif not utils.isValidInt(maxTomorrowsConditions):
            raise TypeError(f'maxTomorrowsConditions argument is malformed: \"{maxTomorrowsConditions}\"')
        elif maxTomorrowsConditions < 1 or maxTomorrowsConditions > utils.getIntMaxSafeSize():
            raise ValueError(f'maxTomorrowsConditions argument is out of bounds: {maxTomorrowsConditions}')

        self.__maxAlerts: Final[int] = maxAlerts
        self.__maxConditions: Final[int] = maxConditions
        self.__maxTomorrowsConditions: Final[int] = maxTomorrowsConditions

    async def __getAirQualityString(self, weather: WeatherReport) -> str:
        if weather.airPollution is None:
            return ''

        airPollutionIndex = weather.airPollution.airPollutionIndex

        match airPollutionIndex:
            case OpenWeatherAirPollutionIndex.GOOD: return ''
            case OpenWeatherAirPollutionIndex.FAIR: return ''
            case OpenWeatherAirPollutionIndex.MODERATE: return 'air quality is moderate, '
            case OpenWeatherAirPollutionIndex.POOR: return 'air quality is poor, '
            case OpenWeatherAirPollutionIndex.VERY_POOR: return 'air quality is very poor, '
            case _:
                raise RuntimeError(f'OpenWeatherAirPollutionIndex is unknown value: \"{airPollutionIndex}\"')

    async def __getAlertsString(self, weather: WeatherReport) -> str:
        alerts = weather.report.alerts

        if alerts is None or len(alerts) == 0:
            return ''

        alertStrings: list[str] = list()

        for alert in alerts:
            alertStrings.append(alert.event)

            if len(alertStrings) >= self.__maxAlerts:
                break

        alertsJoin = ' '.join(alertStrings)
        return f'🚨 {alertsJoin}'

    async def __getConditionsString(self, weather: WeatherReport) -> str:
        weatherDescriptions = weather.report.current.descriptions

        if weatherDescriptions is None or len(weatherDescriptions) == 0:
            return ''

        conditionStrings: list[str] = list()

        for weatherDescription in weatherDescriptions:
            conditionStrings.append(weatherDescription.description)

            if len(conditionStrings) >= self.__maxConditions:
                break

        conditionsJoin = ', '.join(conditionStrings)
        return f'Current conditions: {conditionsJoin}. '

    async def __getHumidityString(self, weather: WeatherReport) -> str:
        return f'humidity is {weather.report.current.humidity}%, '

    async def __getPressureString(self, weather: WeatherReport) -> str:
        pressureString = locale.format_string("%d", weather.report.current.pressure, grouping = True)
        return f'and pressure is {pressureString} hPa. '

    async def __getTemperatureString(self, weather: WeatherReport) -> str:
        cTemp = int(round(weather.report.current.feelsLikeTemperature))
        fTemp = int(round(utils.cToF(weather.report.current.feelsLikeTemperature)))
        return f'🌡️ Temperature is {cTemp}°C ({fTemp}°F), '

    async def __getTomorrowsConditionsString(self, weather: WeatherReport) -> str:
        tomorrow = await self.__getTomorrowsWeather(weather)

        if tomorrow is None or tomorrow.descriptions is None or len(tomorrow.descriptions) == 0:
            return ''

        conditionStrings: list[str] = list()

        for tomorrowsDescription in tomorrow.descriptions:
            conditionStrings.append(tomorrowsDescription.description)

            if len(conditionStrings) >= self.__maxTomorrowsConditions:
                break

        conditionsJoin = ', '.join(conditionStrings)
        return f'Tomorrow\'s conditions: {conditionsJoin}. '

    async def __getTomorrowsTempsString(self, weather: WeatherReport) -> str:
        tomorrow = await self.__getTomorrowsWeather(weather)

        if tomorrow is None:
            return ''

        cMax = int(round(tomorrow.temperature.maximum))
        fMax = int(round(utils.cToF(tomorrow.temperature.maximum)))
        cMin = int(round(tomorrow.temperature.minimum))
        fMin = int(round(utils.cToF(tomorrow.temperature.minimum)))
        return f'Tomorrow has a low of {cMin}°C ({fMin}°F) and a high of {cMax}°C ({fMax}°F). '

    async def __getTomorrowsWeather(self, weather: WeatherReport) -> OpenWeatherDay | None:
        now = datetime.now(weather.report.timeZone)

        for day in weather.report.days:
            if day.dateTime.day > now.day or day.dateTime.month > now.month or day.dateTime.year > now.year:
                return day

        return None

    async def __getUvIndexString(self, weather: WeatherReport) -> str:
        uvIndex = weather.report.current.uvIndex

        if uvIndex <= 2:
            return ''
        elif uvIndex <= 7:
            return f'UV index is moderate to high, '
        else:
            return f'UV index is very high to extreme, '

    async def toString(self, weather: WeatherReport) -> str:
        if not isinstance(weather, WeatherReport):
            raise TypeError(f'weather argument is malformed: \"{weather}\"')

        temperatureStr = await self.__getTemperatureString(weather)
        humidityStr = await self.__getHumidityString(weather)
        airQualityStr = await self.__getAirQualityString(weather)
        uvIndexStr = await self.__getUvIndexString(weather)
        pressureStr = await self.__getPressureString(weather)
        conditionsStr = await self.__getConditionsString(weather)
        tomorrowsTempsStr = await self.__getTomorrowsTempsString(weather)
        tomorrowsConditionsStr = await self.__getTomorrowsConditionsString(weather)
        alertsStr = await self.__getAlertsString(weather)

        combinedStr = f'{temperatureStr}{humidityStr}{airQualityStr}{uvIndexStr}{pressureStr}{conditionsStr}{tomorrowsTempsStr}{tomorrowsConditionsStr}{alertsStr}'
        return utils.cleanStr(combinedStr)
