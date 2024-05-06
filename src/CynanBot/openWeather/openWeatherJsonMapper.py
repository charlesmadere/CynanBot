from datetime import datetime
from typing import Any

import CynanBot.misc.utils as utils
from CynanBot.location.timeZoneRepositoryInterface import \
    TimeZoneRepositoryInterface
from CynanBot.openWeather.openWeatherAirPollutionIndex import \
    OpenWeatherAirPollutionIndex
from CynanBot.openWeather.openWeatherAirPollutionReport import \
    OpenWeatherAirPollutionReport
from CynanBot.openWeather.openWeatherAlert import OpenWeatherAlert
from CynanBot.openWeather.openWeatherDay import OpenWeatherDay
from CynanBot.openWeather.openWeatherFeelsLike import OpenWeatherFeelsLike
from CynanBot.openWeather.openWeatherJsonMapperInterface import \
    OpenWeatherJsonMapperInterface
from CynanBot.openWeather.openWeatherMoment import OpenWeatherMoment
from CynanBot.openWeather.openWeatherMomentDescription import \
    OpenWeatherMomentDescription
from CynanBot.openWeather.openWeatherReport import OpenWeatherReport
from CynanBot.openWeather.openWeatherTemperature import OpenWeatherTemperature
from CynanBot.timber.timberInterface import TimberInterface


class OpenWeatherJsonMapper(OpenWeatherJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository

    async def parseAirPollutionIndex(
        self,
        index: int | None
    ) -> OpenWeatherAirPollutionIndex | None:
        if not utils.isValidInt(index):
            return None

        if index <= 1:
            return OpenWeatherAirPollutionIndex.GOOD
        elif index <= 2:
            return OpenWeatherAirPollutionIndex.FAIR
        elif index <= 3:
            return OpenWeatherAirPollutionIndex.MODERATE
        elif index <= 4:
            return OpenWeatherAirPollutionIndex.POOR
        else:
            return OpenWeatherAirPollutionIndex.VERY_POOR

    async def parseAirPollutionReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherAirPollutionReport | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        coordJson: dict[str, Any] | None = jsonContents.get('coord')
        if not isinstance(coordJson, dict) or len(coordJson) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"coord\" field in JSON data: ({jsonContents=})')
            return None

        latitude = utils.getFloatFromDict(coordJson, 'lat')
        longitude = utils.getFloatFromDict(coordJson, 'lon')

        listArray: list[dict[str, Any] | None] | None = jsonContents.get('list')
        if not isinstance(listArray, list) or len(listArray) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"list\" field in JSON data: ({jsonContents=})')
            return None

        listEntryJson = listArray[0]
        if not isinstance(listEntryJson, dict) or len(listEntryJson) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid entry in \"list\" JSON data: ({jsonContents=})')
            return None

        dateTime = datetime.fromtimestamp(utils.getIntFromDict(listEntryJson, 'dt'))

        mainJson: dict[str, Any] | None = listEntryJson.get('main')
        if not isinstance(mainJson, dict) or len(mainJson) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"main\" field in JSON data: ({jsonContents=})')
            return None

        airPollutionIndex = await self.parseAirPollutionIndex(mainJson.get('aqi'))
        if airPollutionIndex is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid OpenWeatherAirPollutionIndex in \"main\" JSON data: ({jsonContents=})')
            return None

        return OpenWeatherAirPollutionReport(
            dateTime = dateTime,
            latitude = latitude,
            longitude = longitude,
            airPollutionIndex = airPollutionIndex
        )

    async def parseAlert(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherAlert | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        end = utils.getIntFromDict(jsonContents, 'end')
        start = utils.getIntFromDict(jsonContents, 'start')
        description = utils.getStrFromDict(jsonContents, 'description')
        event = utils.getStrFromDict(jsonContents, 'event')
        senderName = utils.getStrFromDict(jsonContents, 'sender_name')

        return OpenWeatherAlert(
            end = end,
            start = start,
            description = description,
            event = event,
            senderName = senderName
        )

    async def parseDay(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherDay | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        dateTime = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'dt'))
        moonrise = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'moonrise'))
        moonset = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'moonset'))
        sunrise = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'sunrise'))
        sunset = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'sunset'))
        dewPoint = utils.getFloatFromDict(jsonContents, 'dew_point')
        moonPhase = utils.getFloatFromDict(jsonContents, 'moon_phase')
        uvIndex = utils.getFloatFromDict(jsonContents, 'uvi')
        windSpeed = utils.getFloatFromDict(jsonContents, 'wind_speed')
        humidity = utils.getIntFromDict(jsonContents, 'humidity')
        pressure = utils.getIntFromDict(jsonContents, 'pressure')
        summary = utils.getStrFromDict(jsonContents, 'summary')

        feelsLike = await self.parseFeelsLike(jsonContents.get('feels_like'))
        if feelsLike is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"feels_like\" field in JSON data: ({jsonContents=})')
            return None

        weatherArray: list[dict[str, Any] | None] | None = jsonContents.get('weather')
        if not isinstance(weatherArray, list) or len(weatherArray) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"weather\" field in JSON data: ({jsonContents=})')
            return None

        weatherEntryJson = weatherArray[0]
        if not isinstance(weatherEntryJson, dict) or len(weatherEntryJson) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid entry in \"weather\" JSON data: ({jsonContents=})')
            return None

        description = await self.parseMomentDescription(weatherEntryJson)
        if description is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value for \"weather\" data: ({jsonContents=})')
            return None

        temperature = await self.parseTemperature(jsonContents.get('temp'))
        if temperature is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"temp\" field in JSON data: ({jsonContents=})')
            return None

        return OpenWeatherDay(
            dateTime = dateTime,
            moonrise = moonrise,
            moonset = moonset,
            sunrise = sunrise,
            sunset = sunset,
            dewPoint = dewPoint,
            moonPhase = moonPhase,
            uvIndex = uvIndex,
            windSpeed = windSpeed,
            humidity = humidity,
            pressure = pressure,
            feelsLike = feelsLike,
            description = description,
            temperature = temperature,
            summary = summary
        )

    async def parseFeelsLike(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherFeelsLike | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        day = utils.getFloatFromDict(jsonContents, 'day')
        evening = utils.getFloatFromDict(jsonContents, 'eve')
        morning = utils.getFloatFromDict(jsonContents, 'morn')
        night = utils.getFloatFromDict(jsonContents, 'night')

        return OpenWeatherFeelsLike(
            day = day,
            evening = evening,
            morning = morning,
            night = night
        )

    async def parseMoment(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMoment | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        dateTime = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'dt'))
        sunrise = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'sunrise'))
        sunset = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'sunset'))
        dewPoint = utils.getFloatFromDict(jsonContents, 'dew_point')
        feelsLikeTemperature = utils.getFloatFromDict(jsonContents, 'feels_like')
        temperature = utils.getFloatFromDict(jsonContents, 'temp')
        uvIndex = utils.getFloatFromDict(jsonContents, 'uvi')
        windSpeed = utils.getFloatFromDict(jsonContents, 'wind_speed')
        humidity = utils.getIntFromDict(jsonContents, 'humidity')
        pressure = utils.getIntFromDict(jsonContents, 'pressure')

        weatherArray: list[dict[str, Any] | None] | None = jsonContents.get('weather')
        if not isinstance(weatherArray, list) or len(weatherArray) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"weather\" field in JSON data: ({jsonContents=})')
            return None

        weatherEntryJson = weatherArray[0]
        if not isinstance(weatherEntryJson, dict) or len(weatherEntryJson) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid entry in \"weather\" JSON data: ({jsonContents=})')
            return None

        description = await self.parseMomentDescription(weatherEntryJson)
        if description is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value for \"weather\" data: ({jsonContents=})')
            return None

        return OpenWeatherMoment(
            dateTime = dateTime,
            sunrise = sunrise,
            sunset = sunset,
            dewPoint = dewPoint,
            feelsLikeTemperature = feelsLikeTemperature,
            temperature = temperature,
            uvIndex = uvIndex,
            windSpeed = windSpeed,
            humidity = humidity,
            pressure = pressure,
            description = description
        )

    async def parseMomentDescription(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMomentDescription | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        description = utils.getStrFromDict(jsonContents, 'description')
        descriptionId = utils.getStrFromDict(jsonContents, 'id')
        icon = utils.getStrFromDict(jsonContents, 'icon')
        main = utils.getStrFromDict(jsonContents, 'main')

        return OpenWeatherMomentDescription(
            description = description,
            descriptionId = descriptionId,
            icon = icon,
            main = main
        )

    async def parseTemperature(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherTemperature | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        day = utils.getFloatFromDict(jsonContents, 'day')
        evening = utils.getFloatFromDict(jsonContents, 'eve')
        maximum = utils.getFloatFromDict(jsonContents, 'max')
        minimum = utils.getFloatFromDict(jsonContents, 'min')
        morning = utils.getFloatFromDict(jsonContents, 'morn')
        night = utils.getFloatFromDict(jsonContents, 'night')

        return OpenWeatherTemperature(
            day = day,
            evening = evening,
            maximum = maximum,
            minimum = minimum,
            morning = morning,
            night = night
        )

    async def parseWeatherReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherReport | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        latitude = utils.getFloatFromDict(jsonContents, 'lat')
        longitude = utils.getFloatFromDict(jsonContents, 'lon')

        alertsArray: list[dict[str, Any] | None] | None = jsonContents.get('alerts')
        alerts: list[OpenWeatherAlert] | None = None

        if isinstance(alertsArray, list) and len(alertsArray) >= 1:
            alerts = list()

            for index, alertEntryJson in enumerate(alertsArray):
                alert = await self.parseAlert(alertEntryJson)

                if alert is None:
                    self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value at index {index} for \"alerts\" data: ({jsonContents=})')
                else:
                    alerts.append(alert)

        current = await self.parseMoment(jsonContents.get('current'))
        if current is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value for \"current\" data: ({jsonContents=})')
            return None

        timeZoneStr = utils.getStrFromDict(jsonContents, 'timezone')
        timeZone = self.__timeZoneRepository.getTimeZone(timeZoneStr)

        dailyArray: list[dict[str, Any]] | None = jsonContents.get('daily')
        days: list[OpenWeatherDay] | None = None

        if isinstance(dailyArray, list) and len(dailyArray) >= 1:
            days = list()

            for index, dailyEntryJson in enumerate(dailyArray):
                day = await self.parseDay(dailyEntryJson)

                if day is None:
                    self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value for \"daily\" data: ({jsonContents=})')
                else:
                    days.append(day)

        if days is None or len(days) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse any \"daily\" data: ({jsonContents=})')
            return None

        return OpenWeatherReport(
            latitude = latitude,
            longitude = longitude,
            alerts = alerts,
            days = days,
            current = current,
            timeZone = timeZone
        )
