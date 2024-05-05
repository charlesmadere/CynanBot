from CynanBot.weather.weatherReport import WeatherReport
from CynanBot.weather.weatherReportPresenterInterface import \
    WeatherReportPresenterInterface


class WeatherReportPresenter(WeatherReportPresenterInterface):

    async def present(self, weather: WeatherReport) -> str:
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
