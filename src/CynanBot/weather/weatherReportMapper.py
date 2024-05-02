from CynanBot.openWeather.openWeatherReport import OpenWeatherReport
from CynanBot.weather.weatherReport import WeatherReport
from CynanBot.weather.weatherReportMapperInterface import WeatherReportMapperInterface


class WeatherReportMapper(WeatherReportMapperInterface):

    async def fromOpenWeatherReport(
        self,
        report: OpenWeatherReport
    ) -> WeatherReport:
        if not isinstance(report, OpenWeatherReport):
            raise TypeError(f'report argument is malformed: \"{report}\"')

        # TODO
        pass

        raise RuntimeError()
