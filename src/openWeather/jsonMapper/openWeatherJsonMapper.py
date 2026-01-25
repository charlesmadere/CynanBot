from datetime import datetime, tzinfo
from typing import Any, Final

from frozendict import frozendict
from frozenlist import FrozenList

from .openWeatherJsonMapperInterface import OpenWeatherJsonMapperInterface
from ..models.openWeatherAirPollutionIndex import OpenWeatherAirPollutionIndex
from ..models.openWeatherAirPollutionReport import OpenWeatherAirPollutionReport
from ..models.openWeatherAlert import OpenWeatherAlert
from ..models.openWeatherDay import OpenWeatherDay
from ..models.openWeatherFeelsLike import OpenWeatherFeelsLike
from ..models.openWeatherMoment import OpenWeatherMoment
from ..models.openWeatherMomentDescription import OpenWeatherMomentDescription
from ..models.openWeatherReport import OpenWeatherReport
from ..models.openWeatherTemperature import OpenWeatherTemperature
from ...location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface


class OpenWeatherJsonMapper(OpenWeatherJsonMapperInterface):

    def __init__(
        self,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__descriptionIdToEmoji: Final[frozendict[str, str | None]] = self.__createDescriptionIdToEmojiDictionary()

    def __createDescriptionIdToEmojiDictionary(self) -> frozendict[str, str | None]:
        dictionary: dict[str, str | None] = dict()
        dictionary['200'] = '⛈️'
        dictionary['201'] = dictionary['200']
        dictionary['202'] = dictionary['200']
        dictionary['210'] = '🌩️'
        dictionary['211'] = dictionary['210']
        dictionary['212'] = dictionary['211']
        dictionary['221'] = dictionary['200']
        dictionary['230'] = dictionary['200']
        dictionary['231'] = dictionary['200']
        dictionary['232'] = dictionary['200']
        dictionary['300'] = '☔'
        dictionary['301'] = dictionary['300']
        dictionary['310'] = dictionary['300']
        dictionary['311'] = dictionary['300']
        dictionary['313'] = dictionary['300']
        dictionary['500'] = dictionary['300']
        dictionary['501'] = '🌧️'
        dictionary['502'] = dictionary['501']
        dictionary['503'] = dictionary['501']
        dictionary['504'] = dictionary['501']
        dictionary['520'] = dictionary['501']
        dictionary['521'] = dictionary['501']
        dictionary['522'] = dictionary['501']
        dictionary['531'] = dictionary['501']
        dictionary['600'] = '❄️'
        dictionary['601'] = dictionary['600']
        dictionary['602'] = '🌨️'
        dictionary['711'] = '🌫️'
        dictionary['721'] = dictionary['711']
        dictionary['731'] = dictionary['711']
        dictionary['741'] = dictionary['711']
        dictionary['762'] = '🌋'
        dictionary['771'] = '🌬️🍃'
        dictionary['781'] = '🌪️'
        dictionary['801'] = '☁️'
        dictionary['802'] = dictionary['801']
        dictionary['803'] = dictionary['801']
        dictionary['804'] = dictionary['801']

        return frozendict(dictionary)

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
        jsonContents: dict[str, Any] | Any | None,
        timeZone: tzinfo
    ) -> OpenWeatherAirPollutionReport | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

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

        dateTime = datetime.fromtimestamp(utils.getIntFromDict(listEntryJson, 'dt'), timeZone)

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
            airPollutionIndex = airPollutionIndex,
            timeZone = timeZone,
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
            senderName = senderName,
        )

    async def parseDay(
        self,
        jsonContents: dict[str, Any] | Any | None,
        timeZone: tzinfo
    ) -> OpenWeatherDay | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        dateTime = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'dt'), timeZone)
        moonrise = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'moonrise'), timeZone)
        moonset = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'moonset'), timeZone)
        sunrise = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'sunrise'), timeZone)
        sunset = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'sunset'), timeZone)
        dewPoint = utils.getFloatFromDict(jsonContents, 'dew_point')
        moonPhase = utils.getFloatFromDict(jsonContents, 'moon_phase')
        uvIndex = utils.getFloatFromDict(jsonContents, 'uvi')
        windSpeed = utils.getFloatFromDict(jsonContents, 'wind_speed')
        humidity = utils.getIntFromDict(jsonContents, 'humidity')
        pressure = utils.getIntFromDict(jsonContents, 'pressure')
        summary = utils.getStrFromDict(jsonContents, 'summary')

        descriptionsArray: list[dict[str, Any] | None] | None = jsonContents.get('weather')
        descriptions: FrozenList[OpenWeatherMomentDescription] | None = None

        if isinstance(descriptionsArray, list) and len(descriptionsArray) >= 1:
            descriptions = FrozenList()

            for index, descriptionEntryJson in enumerate(descriptionsArray):
                description = await self.parseMomentDescription(descriptionEntryJson)

                if description is None:
                    self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value at index {index} for \"weather\" field in JSON data: ({jsonContents=})')
                else:
                    descriptions.append(description)

            descriptions.freeze()

        feelsLike = await self.parseFeelsLike(jsonContents.get('feels_like'))
        if feelsLike is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Encountered missing/invalid \"feels_like\" field in JSON data: ({jsonContents=})')
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
            descriptions = descriptions,
            humidity = humidity,
            pressure = pressure,
            feelsLike = feelsLike,
            temperature = temperature,
            summary = summary,
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
            night = night,
        )

    async def parseMoment(
        self,
        jsonContents: dict[str, Any] | Any | None,
        timeZone: tzinfo
    ) -> OpenWeatherMoment | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None
        elif not isinstance(timeZone, tzinfo):
            raise TypeError(f'timeZone argument is malformed: \"{timeZone}\"')

        dateTime = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'dt'), timeZone)
        sunrise = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'sunrise'), timeZone)
        sunset = datetime.fromtimestamp(utils.getIntFromDict(jsonContents, 'sunset'), timeZone)
        dewPoint = utils.getFloatFromDict(jsonContents, 'dew_point')
        feelsLikeTemperature = utils.getFloatFromDict(jsonContents, 'feels_like')
        temperature = utils.getFloatFromDict(jsonContents, 'temp')
        uvIndex = utils.getFloatFromDict(jsonContents, 'uvi')
        windSpeed = utils.getFloatFromDict(jsonContents, 'wind_speed')
        humidity = utils.getIntFromDict(jsonContents, 'humidity')
        pressure = utils.getIntFromDict(jsonContents, 'pressure')

        descriptionsArray: list[dict[str, Any] | None] | Any | None = jsonContents.get('weather')
        descriptions: FrozenList[OpenWeatherMomentDescription] | None = None

        if isinstance(descriptionsArray, list) and len(descriptionsArray) >= 1:
            descriptions = FrozenList()

            for index, descriptionEntryJson in enumerate(descriptionsArray):
                description = await self.parseMomentDescription(descriptionEntryJson)

                if description is None:
                    self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value at index {index} for \"weather\" data: ({jsonContents=})')
                else:
                    descriptions.append(description)

            if len(descriptions) >= 1:
                descriptions.freeze()
            else:
                descriptions = None

        return OpenWeatherMoment(
            dateTime = dateTime,
            sunrise = sunrise,
            sunset = sunset,
            dewPoint = dewPoint,
            feelsLikeTemperature = feelsLikeTemperature,
            temperature = temperature,
            uvIndex = uvIndex,
            windSpeed = windSpeed,
            descriptions = descriptions,
            humidity = humidity,
            pressure = pressure,
        )

    async def parseMomentDescription(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherMomentDescription | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        description = utils.getStrFromDict(jsonContents, 'description')
        descriptionId = utils.getStrFromDict(jsonContents, 'id')
        emoji = self.__descriptionIdToEmoji.get(descriptionId, None)
        icon = utils.getStrFromDict(jsonContents, 'icon')
        main = utils.getStrFromDict(jsonContents, 'main')

        return OpenWeatherMomentDescription(
            description = description,
            descriptionId = descriptionId,
            emoji = emoji,
            icon = icon,
            main = main,
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
            night = night,
        )

    async def parseWeatherReport(
        self,
        jsonContents: dict[str, Any] | Any | None
    ) -> OpenWeatherReport | None:
        if not isinstance(jsonContents, dict) or len(jsonContents) == 0:
            return None

        latitude = utils.getFloatFromDict(jsonContents, 'lat')
        longitude = utils.getFloatFromDict(jsonContents, 'lon')

        alertsArray: list[dict[str, Any] | None] | Any | None = jsonContents.get('alerts')
        alerts: FrozenList[OpenWeatherAlert] = FrozenList()

        if isinstance(alertsArray, list) and len(alertsArray) >= 1:
            for index, alertEntryJson in enumerate(alertsArray):
                alert = await self.parseAlert(alertEntryJson)

                if alert is None:
                    self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value at index {index} for \"alerts\" data: ({jsonContents=})')
                else:
                    alerts.append(alert)

        alerts.freeze()

        timeZoneStr = utils.getStrFromDict(jsonContents, 'timezone')
        timeZone = self.__timeZoneRepository.getTimeZone(timeZoneStr)

        current = await self.parseMoment(jsonContents.get('current'), timeZone)
        if current is None:
            self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value for \"current\" data: ({jsonContents=})')
            return None

        dailyArray: list[dict[str, Any]] | None = jsonContents.get('daily')
        days: list[OpenWeatherDay] | None = None

        if isinstance(dailyArray, list) and len(dailyArray) >= 1:
            days = list()

            for index, dailyEntryJson in enumerate(dailyArray):
                day = await self.parseDay(dailyEntryJson, timeZone)

                if day is None:
                    self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse value at index {index} for \"daily\" data: ({jsonContents=})')
                else:
                    days.append(day)

            days.sort(key = lambda day: day.dateTime.timestamp())

        if days is None or len(days) == 0:
            self.__timber.log('OpenWeatherJsonMapper', f'Unable to parse any \"daily\" data: ({jsonContents=})')
            return None

        frozenDays: FrozenList[OpenWeatherDay] = FrozenList(days)
        frozenDays.freeze()

        return OpenWeatherReport(
            latitude = latitude,
            longitude = longitude,
            alerts = alerts,
            days = frozenDays,
            current = current,
            timeZone = timeZone,
        )
