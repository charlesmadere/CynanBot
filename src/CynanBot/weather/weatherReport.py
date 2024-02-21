import locale
from typing import List, Optional

import CynanBot.misc.utils as utils
from CynanBot.weather.airQualityIndex import AirQualityIndex
from CynanBot.weather.uvIndex import UvIndex


class WeatherReport():

    def __init__(
        self,
        airQualityIndex: Optional[AirQualityIndex],
        temperature: float,
        tomorrowsHighTemperature: float,
        tomorrowsLowTemperature: float,
        humidity: int,
        pressure: int,
        alerts: List[str],
        conditions: List[str],
        tomorrowsConditions: List[str],
        locationId: str,
        uvIndex: UvIndex
    ):
        assert airQualityIndex is None or isinstance(airQualityIndex, AirQualityIndex), f"malformed {airQualityIndex=}"
        if not utils.isValidNum(temperature):
            raise ValueError(f'temperature argument is malformed: \"{temperature}\"')
        if temperature < utils.getIntMinSafeSize() or temperature > utils.getIntMaxSafeSize():
            raise ValueError(f'temperature argument is out of bounds: {temperature}')
        if not utils.isValidNum(tomorrowsHighTemperature):
            raise ValueError(f'tomorrowsHighTemperature argument is malformed: \"{tomorrowsHighTemperature}\"')
        if tomorrowsHighTemperature < utils.getIntMinSafeSize() or tomorrowsHighTemperature > utils.getIntMaxSafeSize():
            raise ValueError(f'tomorrowsHighTemperature argument is out of bounds: {tomorrowsHighTemperature}')
        if not utils.isValidNum(tomorrowsLowTemperature):
            raise ValueError(f'tomorrowsLowTemperature argument is malformed: \"{tomorrowsLowTemperature}\"')
        if tomorrowsLowTemperature < utils.getIntMinSafeSize() or tomorrowsLowTemperature > utils.getIntMaxSafeSize():
            raise ValueError(f'tomorrowsLowTemperature argument is out of bounds: {tomorrowsLowTemperature}')
        if not utils.isValidInt(humidity):
            raise ValueError(f'humidity argument is malformed: \"{humidity}\"')
        if not utils.isValidInt(pressure):
            raise ValueError(f'pressure argument is malformed: \"{pressure}\"')
        if not utils.isValidStr(locationId):
            raise ValueError(f'locationId argument is malformed: \"{locationId}\"')
        assert isinstance(uvIndex, UvIndex), f"malformed {uvIndex=}"

        self.__airQualityIndex: Optional[AirQualityIndex] = airQualityIndex
        self.__temperature: float = temperature
        self.__tomorrowsHighTemperature: float = tomorrowsHighTemperature
        self.__tomorrowsLowTemperature: float = tomorrowsLowTemperature
        self.__humidity: int = humidity
        self.__pressure: int = pressure
        self.__alerts: List[str] = alerts
        self.__conditions: List[str] = conditions
        self.__tomorrowsConditions: List[str] = tomorrowsConditions
        self.__locationId: str = locationId
        self.__uvIndex: UvIndex = uvIndex

    def getAirQualityIndex(self) -> Optional[AirQualityIndex]:
        return self.__airQualityIndex

    def getAlerts(self) -> List[str]:
        return self.__alerts

    def getConditions(self) -> List[str]:
        return self.__conditions

    def getHumidity(self) -> int:
        return self.__humidity

    def getLocationId(self) -> str:
        return self.__locationId

    def getPressure(self) -> int:
        return self.__pressure

    def getPressureStr(self) -> str:
        return locale.format_string("%d", self.getPressure(), grouping = True)

    def getTemperature(self):
        return int(round(self.__temperature))

    def getTemperatureStr(self):
        return locale.format_string("%d", self.getTemperature(), grouping = True)

    def getTemperatureImperial(self):
        return int(round(utils.cToF(self.__temperature)))

    def getTemperatureImperialStr(self):
        return locale.format_string("%d", self.getTemperatureImperial(), grouping = True)

    def getTomorrowsConditions(self) -> List[str]:
        return self.__tomorrowsConditions

    def getTomorrowsLowTemperature(self) -> int:
        return int(round(self.__tomorrowsLowTemperature))

    def getTomorrowsLowTemperatureStr(self) -> str:
        return locale.format_string("%d", self.getTomorrowsLowTemperature(), grouping = True)

    def getTomorrowsLowTemperatureImperial(self) -> int:
        return int(round(utils.cToF(self.__tomorrowsLowTemperature)))

    def getTomorrowsLowTemperatureImperialStr(self) -> str:
        return locale.format_string("%d", self.getTomorrowsLowTemperatureImperial(), grouping = True)

    def getTomorrowsHighTemperature(self) -> int:
        return int(round(self.__tomorrowsHighTemperature))

    def getTomorrowsHighTemperatureStr(self) -> str:
        return locale.format_string("%d", self.getTomorrowsHighTemperature(), grouping = True)

    def getTomorrowsHighTemperatureImperial(self) -> int:
        return int(round(utils.cToF(self.__tomorrowsHighTemperature)))

    def getTomorrowsHighTemperatureImperialStr(self) -> str:
        return locale.format_string("%d", self.getTomorrowsHighTemperatureImperial(), grouping = True)

    def getUvIndex(self) -> UvIndex:
        return self.__uvIndex

    def hasAirQualityIndex(self) -> bool:
        return self.__airQualityIndex is not None

    def hasAlerts(self) -> bool:
        return utils.hasItems(self.__alerts)

    def hasConditions(self) -> bool:
        return utils.hasItems(self.__conditions)

    def hasTomorrowsConditions(self) -> bool:
        return utils.hasItems(self.__tomorrowsConditions)

    def hasUvIndex(self) -> bool:
        return self.__uvIndex is not None

    def toStr(self, delimiter: str = ', ') -> str:
        assert isinstance(delimiter, str), f"malformed {delimiter=}"

        temperature = f'🌡 Temperature is {self.getTemperatureStr()}°C ({self.getTemperatureImperialStr()}°F), '
        humidity = f'humidity is {self.getHumidity()}%, '

        airQuality = ''
        if self.hasAirQualityIndex():
            airQuality = f'air quality index is {self.__airQualityIndex.toStr()}, '

        uvIndex = ''
        if self.hasUvIndex() and self.__uvIndex.isNoteworthy():
            uvIndex = f'UV Index is {self.__uvIndex.toStr()}, '

        pressure = f'and pressure is {self.getPressureStr()} hPa. '

        conditions = ''
        if self.hasConditions():
            conditionsJoin = delimiter.join(self.__conditions)
            conditions = f'Current conditions: {conditionsJoin}. '

        tomorrowsTemps = f'Tomorrow has a low of {self.getTomorrowsLowTemperatureStr()}°C ({self.getTomorrowsLowTemperatureImperialStr()}°F) and a high of {self.getTomorrowsHighTemperatureStr()}°C ({self.getTomorrowsHighTemperatureImperialStr()}°F). '

        tomorrowsConditions = ''
        if self.hasTomorrowsConditions():
            tomorrowsConditionsJoin = delimiter.join(self.__tomorrowsConditions)
            tomorrowsConditions = f'Tomorrow\'s conditions: {tomorrowsConditionsJoin}. '

        alerts = ''
        if self.hasAlerts():
            alertsJoin = ' '.join(self.__alerts)
            alerts = f'🚨 {alertsJoin}'

        return f'{temperature}{humidity}{airQuality}{uvIndex}{pressure}{conditions}{tomorrowsTemps}{tomorrowsConditions}{alerts}'
