import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..location.exceptions import NoSuchLocationException
from ..location.locationsRepositoryInterface import LocationsRepositoryInterface
from ..misc import utils as utils
from ..openWeather.exceptions import OpenWeatherApiKeyUnavailableException
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..users.usersRepositoryInterface import UsersRepositoryInterface
from ..weather.weatherReport import WeatherReport
from ..weather.weatherReportPresenterInterface import WeatherReportPresenterInterface
from ..weather.weatherRepositoryInterface import WeatherRepositoryInterface


class WeatherChatCommand(AbsChatCommand2):

    def __init__(
        self,
        locationsRepository: LocationsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
        weatherReportPresenter: WeatherReportPresenterInterface,
        weatherRepository: WeatherRepositoryInterface,
    ):
        if not isinstance(locationsRepository, LocationsRepositoryInterface):
            raise TypeError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(weatherReportPresenter, WeatherReportPresenterInterface):
            raise TypeError(f'weatherReportPresenter argument is malformed: \"{weatherReportPresenter}\"')
        elif not isinstance(weatherRepository, WeatherRepositoryInterface):
            raise TypeError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')

        self.__locationsRepository: Final[LocationsRepositoryInterface] = locationsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__weatherReportPresenter: Final[WeatherReportPresenterInterface] = weatherReportPresenter
        self.__weatherRepository: Final[WeatherRepositoryInterface] = weatherRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!weather\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'WeatherChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isWeatherEnabled:
            return ChatCommandResult.IGNORED

        locationId = chatMessage.twitchUser.locationId
        if not utils.isValidStr(locationId):
            return ChatCommandResult.IGNORED

        try:
            location = await self.__locationsRepository.getLocation(locationId)
        except NoSuchLocationException as e:
            self.__timber.log(self.commandName, f'The given user has no location ID available ({locationId=}) ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.IGNORED

        weatherReport: WeatherReport | None = None

        try:
            weatherReport = await self.__weatherRepository.fetchWeather(
                location = location,
            )

            weatherReportString = await self.__weatherReportPresenter.toString(
                weather = weatherReport,
            )

            self.__twitchChatMessenger.send(
                text = weatherReportString,
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        except OpenWeatherApiKeyUnavailableException as e:
            self.__timber.log(self.commandName, f'OpenWeather API key unavailable when fetching weather ({locationId=}) ({chatMessage=})', e, traceback.format_exc())
        except Exception as e:
            self.__timber.log(self.commandName, f'Error fetching weather ({locationId=}) ({chatMessage=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = '⚠ Error fetching weather',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Handled ({weatherReport=})')
        return ChatCommandResult.HANDLED
