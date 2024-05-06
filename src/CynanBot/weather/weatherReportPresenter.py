import locale

import CynanBot.misc.utils as utils
from CynanBot.openWeather.openWeatherAirPollutionIndex import \
    OpenWeatherAirPollutionIndex
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport
from CynanBot.weather.weatherReport import WeatherReport
from CynanBot.weather.weatherReport2 import WeatherReport2
from CynanBot.weather.weatherReportPresenterInterface import \
    WeatherReportPresenterInterface


class WeatherReportPresenter(WeatherReportPresenterInterface):

    async def __getAirQualityString(self, weather: WeatherReport2) -> str | None:
        if weather.airPollution is None:
            return None

        airPollutionIndex = weather.airPollution.airPollutionIndex

        if airPollutionIndex is OpenWeatherAirPollutionIndex.GOOD:
            return None
        elif airPollutionIndex is OpenWeatherAirPollutionIndex.FAIR:
            return None
        elif airPollutionIndex is OpenWeatherAirPollutionIndex.MODERATE:
            return 'air quality is moderate, '
        elif airPollutionIndex is OpenWeatherAirPollutionIndex.POOR:
            return 'air quality is poor, '
        elif airPollutionIndex is OpenWeatherAirPollutionIndex.VERY_POOR:
            return 'air quality is very poor, '
        else:
            raise RuntimeError(f'OpenWeatherAirPollutionIndex is unknown value: \"{airPollutionIndex}\"')

    async def __getConditionsString(self, weather: WeatherReport2) -> str | None:
        weatherDescriptions = weather.report.current.descriptions

        if weatherDescriptions is None or len(weatherDescriptions) == 0:
            return None

        conditions: list[str] = list()

        for weatherDescription in weatherDescriptions:
            conditions.append(weatherDescription.description)

        conditionsJoin = ', '.join(conditions)
        return f'Current conditions: {conditionsJoin}'

    async def __getHumidityString(self, weather: WeatherReport2) -> str:
        return f'humidity is {weather.report.current.humidity}%, '

    async def __getPressureString(self, weather: WeatherReport2) -> str:
        pressureString = locale.format_string("%d", weather.report.current.pressure, grouping = True)
        return f'and pressure is {pressureString} hPa. '

    async def __getTemperatureString(self, weather: WeatherReport2) -> str:
        cTemp = int(round(weather.report.current.feelsLikeTemperature))
        fTemp = int(round(utils.cToF(weather.report.current.feelsLikeTemperature)))
        return f'🌡️ Temperature is {cTemp}°C ({fTemp}°F), '

    async def __getUvIndexString(self, weather: WeatherReport2) -> str | None:
        uvIndex = weather.report.current.uvIndex

        if uvIndex <= 2:
            return None
        elif uvIndex <= 7:
            return f'UV index is moderate to high, '
        else:
            return f'UV index is very high to extreme, '

    async def toString2(self, weather: WeatherReport2) -> str:
        if not isinstance(weather, WeatherReport2):
            raise TypeError(f'weather argument is malformed: \"{weather}\"')

        temperatureStr = await self.__getTemperatureString(weather)
        humidityStr = await self.__getHumidityString(weather)
        airQualityStr = await self.__getAirQualityString(weather)
        uvIndexStr = await self.__getUvIndexString(weather)
        pressureStr = await self.__getPressureString(weather)
        conditionsStr = await self.__getConditionsString(weather)
        return ''

    async def toString(self, weather: WeatherReport) -> str:
        if not isinstance(weather, WeatherReport):
            raise TypeError(f'weather argument is malformed: \"{weather}\"')

        temperatureStr = f'🌡 Temperature is {weather.getTemperatureStr()}°C ({weather.getTemperatureImperialStr()}°F), '
        humidityStr = f'humidity is {weather.humidity}%, '

        airQualityIndexStr = ''
        if weather.airQualityIndex is not None:
            airQualityIndexStr = f'air quality index is {weather.airQualityIndex.toStr()}, '

        uvIndexStr = ''
        if weather.uvIndex is not None and weather.uvIndex.isNoteworthy():
            uvIndexStr = f'UV Index is {weather.uvIndex.toStr()}, '

        pressureStr = f'and pressure is {weather.getPressureStr()} hPa. '

        conditionsStr = ''
        if weather.conditions is not None and len(weather.conditions) >= 1:
            conditionsJoin = ', '.join(weather.conditions)
            conditionsStr = f'Current conditions: {conditionsJoin}. '

        tomorrowsTempsStr = f'Tomorrow has a low of {weather.getTomorrowsLowTemperatureStr()}°C ({weather.getTomorrowsLowTemperatureImperialStr()}°F) and a high of {weather.getTomorrowsHighTemperatureStr()}°C ({weather.getTomorrowsHighTemperatureImperialStr()}°F). '

        tomorrowsConditionsStr = ''
        if weather.tomorrowsConditions is not None and len(weather.tomorrowsConditions) >= 1:
            tomorrowsConditionsJoin = ', '.join(weather.tomorrowsConditions)
            tomorrowsConditionsStr = f'Tomorrow\'s conditions: {tomorrowsConditionsJoin}. '

        alertsStr = ''
        if weather.alerts is not None and len(weather.alerts) >= 1:
            alertsJoin = ' '.join(weather.alerts)
            alertsStr = f'🚨 {alertsJoin}'

        return f'{temperatureStr}{humidityStr}{airQualityIndexStr}{uvIndexStr}{pressureStr}{conditionsStr}{tomorrowsTempsStr}{tomorrowsConditionsStr}{alertsStr}'.strip()
