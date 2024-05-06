import locale
from dataclasses import dataclass

import CynanBot.misc.utils as utils
from CynanBot.weather.airQualityIndex import AirQualityIndex
from CynanBot.weather.uvIndex import UvIndex


@dataclass(frozen = True)
class WeatherReport():
    airQualityIndex: AirQualityIndex | None
    temperature: float
    tomorrowsHighTemperature: float
    tomorrowsLowTemperature: float
    humidity: int
    pressure: int
    alerts: list[str] | None
    conditions: list[str] | None
    tomorrowsConditions: list[str] | None
    locationId: str
    uvIndex: UvIndex | None

    def getPressureStr(self) -> str:
        return locale.format_string("%d", self.pressure, grouping = True)

    def getTemperatureInt(self):
        return int(round(self.temperature))

    def getTemperatureStr(self):
        return locale.format_string("%d", self.temperature, grouping = True)

    def getTemperatureImperialInt(self):
        return int(round(utils.cToF(self.temperature)))

    def getTemperatureImperialStr(self):
        return locale.format_string("%d", self.getTemperatureImperialInt(), grouping = True)

    def getTomorrowsLowTemperatureInt(self) -> int:
        return int(round(self.tomorrowsLowTemperature))

    def getTomorrowsLowTemperatureStr(self) -> str:
        return locale.format_string("%d", self.getTomorrowsLowTemperatureInt(), grouping = True)

    def getTomorrowsLowTemperatureImperial(self) -> int:
        return int(round(utils.cToF(self.tomorrowsLowTemperature)))

    def getTomorrowsLowTemperatureImperialStr(self) -> str:
        return locale.format_string("%d", self.getTomorrowsLowTemperatureImperial(), grouping = True)

    def getTomorrowsHighTemperatureInt(self) -> int:
        return int(round(self.tomorrowsHighTemperature))

    def getTomorrowsHighTemperatureStr(self) -> str:
        return locale.format_string("%d", self.getTomorrowsHighTemperatureInt(), grouping = True)

    def getTomorrowsHighTemperatureImperial(self) -> int:
        return int(round(utils.cToF(self.tomorrowsHighTemperature)))

    def getTomorrowsHighTemperatureImperialStr(self) -> str:
        return locale.format_string("%d", self.getTomorrowsHighTemperatureImperial(), grouping = True)
