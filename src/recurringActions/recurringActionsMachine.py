import asyncio
import queue
import random
import traceback
from datetime import datetime, timedelta
from queue import SimpleQueue

from ..misc import utils as utils
from ..language.wordOfTheDayRepositoryInterface import \
    WordOfTheDayRepositoryInterface
from ..language.wordOfTheDayResponse import WordOfTheDayResponse
from ..location.locationsRepositoryInterface import LocationsRepositoryInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc.backgroundTaskHelperInterface import BackgroundTaskHelperInterface
from .mostRecentRecurringActionRepositoryInterface import \
    MostRecentRecurringActionRepositoryInterface
from .recurringAction import RecurringAction
from .recurringActionEventListener import \
    RecurringActionEventListener
from .recurringActionsMachineInterface import \
    RecurringActionsMachineInterface
from .recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from .recurringActionType import RecurringActionType
from .recurringEvent import RecurringEvent
from .superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from .superTriviaRecurringEvent import \
    SuperTriviaRecurringEvent
from .weatherRecurringAction import WeatherRecurringAction
from .weatherRecurringEvent import WeatherRecurringEvent
from .wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction
from .wordOfTheDayRecurringEvent import \
    WordOfTheDayRecurringEvent
from ..timber.timberInterface import TimberInterface
from ..trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from ..trivia.triviaGameMachineInterface import TriviaGameMachineInterface
from ..twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface
from ..weather.weatherReport import WeatherReport
from ..weather.weatherRepositoryInterface import WeatherRepositoryInterface


class RecurringActionsMachine(RecurringActionsMachineInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelperInterface,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        locationsRepository: LocationsRepositoryInterface,
        mostRecentRecurringActionRepository: MostRecentRecurringActionRepositoryInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
        weatherRepository: WeatherRepositoryInterface | None,
        wordOfTheDayRepository: WordOfTheDayRepositoryInterface,
        queueSleepTimeSeconds: float = 3,
        refreshSleepTimeSeconds: float = 90,
        queueTimeoutSeconds: int = 3,
        superTriviaCountdownSeconds: int = 5,
        cooldown: timedelta = timedelta(minutes = 3)
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelperInterface):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface):
            raise TypeError(f'isLiveOnTwitchRepository argument is malformed: \"{isLiveOnTwitchRepository}\"')
        elif not isinstance(locationsRepository, LocationsRepositoryInterface):
            raise TypeError(f'locationsRepository argument is malformed: \"{locationsRepository}\"')
        elif not isinstance(mostRecentRecurringActionRepository, MostRecentRecurringActionRepositoryInterface):
            raise TypeError(f'mostRecentRecurringActionRepository argument is malformed: \"{mostRecentRecurringActionRepository}\"')
        elif not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(triviaGameBuilder, TriviaGameBuilderInterface):
            raise TypeError(f'triviaGameBuilder argument is malformed: \"{triviaGameBuilder}\"')
        elif not isinstance(triviaGameMachine, TriviaGameMachineInterface):
            raise TypeError(f'triviaGameMachine argument is malformed: \"{triviaGameMachine}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif weatherRepository is not None and not isinstance(weatherRepository, WeatherRepositoryInterface):
            raise TypeError(f'weatherRepository argument is malformed: \"{weatherRepository}\"')
        elif not isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface):
            raise TypeError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')
        elif not utils.isValidNum(queueSleepTimeSeconds):
            raise TypeError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        elif queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 15:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        elif not utils.isValidNum(refreshSleepTimeSeconds):
            raise TypeError(f'refreshSleepTimeSeconds argument is malformed: \"{refreshSleepTimeSeconds}\"')
        elif refreshSleepTimeSeconds < 30 or refreshSleepTimeSeconds > 600:
            raise ValueError(f'refreshSleepTimeSeconds argument is out of bounds: {refreshSleepTimeSeconds}')
        elif not utils.isValidInt(queueTimeoutSeconds):
            raise TypeError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        elif queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        elif not utils.isValidInt(superTriviaCountdownSeconds):
            raise TypeError(f'superTriviaCountdownSeconds argument is malformed: \"{superTriviaCountdownSeconds}\"')
        elif superTriviaCountdownSeconds < 3 or superTriviaCountdownSeconds > 10:
            raise ValueError(f'superTriviaCountdownSeconds argument is out of bounds: {superTriviaCountdownSeconds}')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__backgroundTaskHelper: BackgroundTaskHelperInterface = backgroundTaskHelper
        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__locationsRepository: LocationsRepositoryInterface = locationsRepository
        self.__mostRecentRecurringActionsRepository: MostRecentRecurringActionRepositoryInterface = mostRecentRecurringActionRepository
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__triviaGameBuilder: TriviaGameBuilderInterface = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface = triviaGameMachine
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__weatherRepository: WeatherRepositoryInterface | None = weatherRepository
        self.__wordOfTheDayRepository: WordOfTheDayRepositoryInterface = wordOfTheDayRepository
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__refreshSleepTimeSeconds: float = refreshSleepTimeSeconds
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds
        self.__superTriviaCountdownSeconds: int = superTriviaCountdownSeconds
        self.__cooldown: timedelta = cooldown

        self.__isStarted: bool = False
        self.__eventListener: RecurringActionEventListener | None = None
        self.__eventQueue: SimpleQueue[RecurringEvent] = SimpleQueue()

    async def __fetchViableUsers(self) -> list[UserInterface]:
        users = await self.__usersRepository.getUsersAsync()
        return [ user for user in users if user.isEnabled() and user.areRecurringActionsEnabled() ]

    async def __findDueRecurringAction(
        self,
        twitchChannelId: str,
        user: UserInterface
    ) -> RecurringAction | None:
        if not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        actionTypes: list[RecurringActionType] = list(RecurringActionType)
        action: RecurringAction | None = None

        mostRecentAction = await self.__mostRecentRecurringActionsRepository.getMostRecentRecurringAction(
            twitchChannel = user.getHandle(),
            twitchChannelId = twitchChannelId
        )

        now = datetime.now(self.__timeZoneRepository.getDefault())

        while len(actionTypes) >= 1 and action is None:
            actionType = random.choice(actionTypes)
            actionTypes.remove(actionType)

            match actionType:
                case RecurringActionType.SUPER_TRIVIA:
                    action = await self.__recurringActionsRepository.getSuperTriviaRecurringAction(
                        twitchChannel = user.getHandle(),
                        twitchChannelId = twitchChannelId
                    )

                case RecurringActionType.WEATHER:
                    action = await self.__recurringActionsRepository.getWeatherRecurringAction(
                        twitchChannel = user.getHandle(),
                        twitchChannelId = twitchChannelId
                    )

                case RecurringActionType.WORD_OF_THE_DAY:
                    action = await self.__recurringActionsRepository.getWordOfTheDayRecurringAction(
                        twitchChannel = user.getHandle(),
                        twitchChannelId = twitchChannelId
                    )

                case _:
                    raise RuntimeError(f'Unknown RecurringActionType: \"{actionType}\"')

            if action is not None and not action.isEnabled():
                action = None
            elif mostRecentAction is not None and action is not None:
                if now < mostRecentAction.dateTime + self.__cooldown:
                    action = None
                else:
                    minutesBetweenInt = action.getMinutesBetween()

                    if not utils.isValidInt(minutesBetweenInt):
                        minutesBetweenInt = action.getActionType().getDefaultRecurringActionTimingMinutes()

                    minutesBetween = timedelta(minutes = minutesBetweenInt)

                    if now < mostRecentAction.dateTime + minutesBetween:
                        action = None

        return action

    async def __processRecurringAction(
        self,
        user: UserInterface,
        action: RecurringAction
    ):
        if not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(action, RecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if not action.isEnabled():
            raise RuntimeError(f'Attempting to process a disabled action: \"{action}\"')

        if isinstance(action, SuperTriviaRecurringAction):
            return await self.__processSuperTriviaRecurringAction(
                user = user,
                action = action
            )
        elif isinstance(action, WeatherRecurringAction):
            return await self.__processWeatherRecurringAction(
                user = user,
                action = action
            )
        elif isinstance(action, WordOfTheDayRecurringAction):
            return await self.__processWordOfTheDayRecurringAction(
                user = user,
                action = action
            )
        else:
            raise RuntimeError(f'Unknown RecurringAction type: \"{type(action)=}\"')

    async def __processSuperTriviaRecurringAction(
        self,
        user: UserInterface,
        action: SuperTriviaRecurringAction
    ) -> bool:
        if not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(action, SuperTriviaRecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        newTriviaGame = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            twitchChannelId = await self.__userIdsRepository.requireUserId(user.getHandle())
        )

        if newTriviaGame is None:
            return False

        await self.__submitEvent(SuperTriviaRecurringEvent(
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId()
        ))

        # delay to allow users to prepare for an incoming trivia question
        await asyncio.sleep(self.__superTriviaCountdownSeconds)

        self.__triviaGameMachine.submitAction(newTriviaGame)
        return True

    async def __processWeatherRecurringAction(
        self,
        user: UserInterface,
        action: WeatherRecurringAction
    ) -> bool:
        if not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(action, WeatherRecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        if self.__weatherRepository is None:
            return False

        locationId = user.getLocationId()
        if not utils.isValidStr(locationId):
            return False

        location = await self.__locationsRepository.getLocation(locationId)
        weatherReport: WeatherReport | None = None

        try:
            weatherReport = await self.__weatherRepository.fetchWeather(location)
        except Exception:
            pass

        if weatherReport is None:
            return False
        elif action.isAlertsOnly() and (weatherReport.report.alerts is None or len(weatherReport.report.alerts) == 0):
            return False

        await self.__submitEvent(WeatherRecurringEvent(
            alertsOnly = action.isAlertsOnly(),
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId(),
            weatherReport = weatherReport
        ))

        return True

    async def __processWordOfTheDayRecurringAction(
        self,
        user: UserInterface,
        action: WordOfTheDayRecurringAction
    ) -> bool:
        if not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')
        elif not isinstance(action, WordOfTheDayRecurringAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        languageEntry = action.getLanguageEntry()

        if languageEntry is None:
            return False

        wordOfTheDayResponse: WordOfTheDayResponse | None = None

        try:
            wordOfTheDayResponse = await self.__wordOfTheDayRepository.fetchWotd(languageEntry)
        except Exception:
            pass

        if wordOfTheDayResponse is None:
            return False

        await self.__submitEvent(WordOfTheDayRecurringEvent(
            languageEntry = languageEntry,
            twitchChannel = action.getTwitchChannel(),
            twitchChannelId = action.getTwitchChannelId(),
            wordOfTheDayResponse = wordOfTheDayResponse
        ))

        return True

    async def __refreshActions(self):
        users = await self.__fetchViableUsers()

        userToRecurringAction: dict[UserInterface, RecurringAction] = dict()
        twitchChannelIds: set[str] = set()

        for user in users:
            twitchChannelId = await self.__userIdsRepository.fetchUserId(user.getHandle())

            if not utils.isValidStr(twitchChannelId):
                self.__timber.log('RecurringActionsMachine', f'Unable to find Twitch user ID for \"{user.getHandle()}\" when refreshing recurring actions')
                continue

            action = await self.__findDueRecurringAction(
                twitchChannelId = twitchChannelId,
                user = user
            )

            if action is not None:
                userToRecurringAction[user] = action
                twitchChannelIds.add(twitchChannelId)

        if len(userToRecurringAction) == 0 or len(twitchChannelIds) == 0:
            return

        twitchChannelIdToLiveStatus = await self.__isLiveOnTwitchRepository.areLive(twitchChannelIds)

        for user, action in userToRecurringAction.items():
            if not twitchChannelIdToLiveStatus.get(action.getTwitchChannelId(), False):
                continue

            if await self.__processRecurringAction(
                user = user,
                action = action
            ):
                await self.__mostRecentRecurringActionsRepository.setMostRecentRecurringAction(action)

    async def __startActionRefreshLoop(self):
        while True:
            try:
                await self.__refreshActions()
            except Exception as e:
                self.__timber.log('RecurringActionsMachine', f'Encountered unknown Exception when refreshing actions: {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__refreshSleepTimeSeconds)

    def setEventListener(self, listener: RecurringActionEventListener | None):
        if listener is not None and not isinstance(listener, RecurringActionEventListener):
            raise TypeError(f'listener argument is malformed: \"{listener}\"')

        self.__eventListener = listener

    async def __startEventLoop(self):
        while True:
            eventListener = self.__eventListener

            if eventListener is not None:
                events: list[RecurringEvent] = list()

                try:
                    while not self.__eventQueue.empty():
                        events.append(self.__eventQueue.get_nowait())
                except queue.Empty as e:
                    self.__timber.log('RecurringActionsMachine', f'Encountered queue.Empty when building up events list (queue size: {self.__eventQueue.qsize()}) (events size: {len(events)}): {e}', e, traceback.format_exc())

                for event in events:
                    try:
                        await eventListener.onNewRecurringActionEvent(event)
                    except Exception as e:
                        self.__timber.log('RecurringActionsMachine', f'Encountered unknown Exception when looping through events (queue size: {self.__eventQueue.qsize()}) (event=\"{event}\"): {e}', e, traceback.format_exc())

            await asyncio.sleep(self.__queueSleepTimeSeconds)

    def startMachine(self):
        if self.__isStarted:
            self.__timber.log('RecurringActionsMachine', 'Not starting RecurringActionsMachine as it has already been started')
            return

        self.__isStarted = True
        self.__timber.log('RecurringActionsMachine', 'Starting RecurringActionsMachine...')
        self.__backgroundTaskHelper.createTask(self.__startActionRefreshLoop())
        self.__backgroundTaskHelper.createTask(self.__startEventLoop())

    async def __submitEvent(self, event: RecurringEvent):
        if not isinstance(event, RecurringEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('RecurringActionsMachine', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())
