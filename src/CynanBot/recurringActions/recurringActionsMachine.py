import asyncio
import queue
import random
import traceback
from datetime import datetime, timedelta, timezone
from queue import SimpleQueue
from typing import Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.language.wordOfTheDayRepositoryInterface import \
    WordOfTheDayRepositoryInterface
from CynanBot.language.wordOfTheDayResponse import WordOfTheDayResponse
from CynanBot.location.locationsRepositoryInterface import \
    LocationsRepositoryInterface
from CynanBot.recurringActions.mostRecentRecurringActionRepositoryInterface import \
    MostRecentRecurringActionRepositoryInterface
from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionEventListener import \
    RecurringActionEventListener
from CynanBot.recurringActions.recurringActionsMachineInterface import \
    RecurringActionsMachineInterface
from CynanBot.recurringActions.recurringActionsRepositoryInterface import \
    RecurringActionsRepositoryInterface
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.recurringEvent import RecurringEvent
from CynanBot.recurringActions.superTriviaRecurringAction import \
    SuperTriviaRecurringAction
from CynanBot.recurringActions.superTriviaRecurringEvent import \
    SuperTriviaRecurringEvent
from CynanBot.recurringActions.weatherRecurringAction import \
    WeatherRecurringAction
from CynanBot.recurringActions.weatherRecurringEvent import \
    WeatherRecurringEvent
from CynanBot.recurringActions.wordOfTheDayRecurringAction import \
    WordOfTheDayRecurringAction
from CynanBot.recurringActions.wordOfTheDayRecurringEvent import \
    WordOfTheDayRecurringEvent
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.builder.triviaGameBuilderInterface import \
    TriviaGameBuilderInterface
from CynanBot.trivia.triviaGameMachineInterface import \
    TriviaGameMachineInterface
from CynanBot.twitch.isLiveOnTwitchRepositoryInterface import \
    IsLiveOnTwitchRepositoryInterface
from CynanBot.users.userInterface import UserInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface
from CynanBot.weather.weatherReport import WeatherReport
from CynanBot.weather.weatherRepositoryInterface import \
    WeatherRepositoryInterface


class RecurringActionsMachine(RecurringActionsMachineInterface):

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface,
        locationsRepository: LocationsRepositoryInterface,
        mostRecentRecurringActionRepository: MostRecentRecurringActionRepositoryInterface,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
        triviaGameBuilder: TriviaGameBuilderInterface,
        triviaGameMachine: TriviaGameMachineInterface,
        usersRepository: UsersRepositoryInterface,
        weatherRepository: Optional[WeatherRepositoryInterface],
        wordOfTheDayRepository: WordOfTheDayRepositoryInterface,
        queueSleepTimeSeconds: float = 3,
        refreshSleepTimeSeconds: float = 90,
        queueTimeoutSeconds: int = 3,
        superTriviaCountdownSeconds: int = 5,
        cooldown: timedelta = timedelta(minutes = 3),
        timeZone: timezone = timezone.utc
    ):
        assert isinstance(backgroundTaskHelper, BackgroundTaskHelper), f"malformed {backgroundTaskHelper=}"
        assert isinstance(isLiveOnTwitchRepository, IsLiveOnTwitchRepositoryInterface), f"malformed {isLiveOnTwitchRepository=}"
        assert isinstance(locationsRepository, LocationsRepositoryInterface), f"malformed {locationsRepository=}"
        assert isinstance(mostRecentRecurringActionRepository, MostRecentRecurringActionRepositoryInterface), f"malformed {mostRecentRecurringActionRepository=}"
        assert isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface), f"malformed {recurringActionsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(triviaGameBuilder, TriviaGameBuilderInterface), f"malformed {triviaGameBuilder=}"
        assert isinstance(triviaGameMachine, TriviaGameMachineInterface), f"malformed {triviaGameMachine=}"
        assert isinstance(usersRepository, UsersRepositoryInterface), f"malformed {usersRepository=}"
        assert weatherRepository is None or isinstance(weatherRepository, WeatherRepositoryInterface), f"malformed {weatherRepository=}"
        assert isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface), f"malformed {wordOfTheDayRepository=}"
        if not utils.isValidNum(queueSleepTimeSeconds):
            raise ValueError(f'queueSleepTimeSeconds argument is malformed: \"{queueSleepTimeSeconds}\"')
        if queueSleepTimeSeconds < 1 or queueSleepTimeSeconds > 15:
            raise ValueError(f'queueSleepTimeSeconds argument is out of bounds: {queueSleepTimeSeconds}')
        if not utils.isValidNum(refreshSleepTimeSeconds):
            raise ValueError(f'refreshSleepTimeSeconds argument is malformed: \"{refreshSleepTimeSeconds}\"')
        if refreshSleepTimeSeconds < 30 or refreshSleepTimeSeconds > 600:
            raise ValueError(f'refreshSleepTimeSeconds argument is out of bounds: {refreshSleepTimeSeconds}')
        if not utils.isValidInt(queueTimeoutSeconds):
            raise ValueError(f'queueTimeoutSeconds argument is malformed: \"{queueTimeoutSeconds}\"')
        if queueTimeoutSeconds < 1 or queueTimeoutSeconds > 5:
            raise ValueError(f'queueTimeoutSeconds argument is out of bounds: {queueTimeoutSeconds}')
        if not utils.isValidInt(superTriviaCountdownSeconds):
            raise ValueError(f'superTriviaCountdownSeconds argument is malformed: \"{superTriviaCountdownSeconds}\"')
        if superTriviaCountdownSeconds < 3 or superTriviaCountdownSeconds > 10:
            raise ValueError(f'superTriviaCountdownSeconds argument is out of bounds: {superTriviaCountdownSeconds}')
        assert isinstance(cooldown, timedelta), f"malformed {cooldown=}"
        assert isinstance(timeZone, timezone), f"malformed {timeZone=}"

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__isLiveOnTwitchRepository: IsLiveOnTwitchRepositoryInterface = isLiveOnTwitchRepository
        self.__locationsRepository: LocationsRepositoryInterface = locationsRepository
        self.__mostRecentRecurringActionsRepository: MostRecentRecurringActionRepositoryInterface = mostRecentRecurringActionRepository
        self.__recurringActionsRepository: RecurringActionsRepositoryInterface = recurringActionsRepository
        self.__timber: TimberInterface = timber
        self.__triviaGameBuilder: TriviaGameBuilderInterface = triviaGameBuilder
        self.__triviaGameMachine: TriviaGameMachineInterface = triviaGameMachine
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__weatherRepository: Optional[WeatherRepositoryInterface] = weatherRepository
        self.__wordOfTheDayRepository: WordOfTheDayRepositoryInterface = wordOfTheDayRepository
        self.__queueSleepTimeSeconds: float = queueSleepTimeSeconds
        self.__refreshSleepTimeSeconds: float = refreshSleepTimeSeconds
        self.__queueTimeoutSeconds: int = queueTimeoutSeconds
        self.__superTriviaCountdownSeconds: int = superTriviaCountdownSeconds
        self.__cooldown: timedelta = cooldown
        self.__timeZone: timezone = timeZone

        self.__isStarted: bool = False
        self.__eventListener: Optional[RecurringActionEventListener] = None
        self.__eventQueue: SimpleQueue[RecurringEvent] = SimpleQueue()

    async def __fetchViableUsers(self) -> List[UserInterface]:
        users = await self.__usersRepository.getUsersAsync()
        usersToRemove: List[UserInterface] = list()

        for user in users:
            if not user.isEnabled() or not user.areRecurringActionsEnabled():
                usersToRemove.append(user)

        for userToRemove in usersToRemove:
            users.remove(userToRemove)

        return users

    async def __findDueRecurringAction(self, user: UserInterface) -> Optional[RecurringAction]:
        assert isinstance(user, UserInterface), f"malformed {user=}"

        actionTypes: List[RecurringActionType] = list(RecurringActionType)
        action: Optional[RecurringAction] = None

        mostRecentAction = await self.__mostRecentRecurringActionsRepository.getMostRecentRecurringAction(user.getHandle())
        now = datetime.now(self.__timeZone)

        while len(actionTypes) >= 1 and action is None:
            actionType = random.choice(actionTypes)
            actionTypes.remove(actionType)

            if actionType is RecurringActionType.SUPER_TRIVIA:
                action = await self.__recurringActionsRepository.getSuperTriviaRecurringAction(user.getHandle())
            elif actionType is RecurringActionType.WEATHER:
                action = await self.__recurringActionsRepository.getWeatherRecurringAction(user.getHandle())
            elif actionType is RecurringActionType.WORD_OF_THE_DAY:
                action = await self.__recurringActionsRepository.getWordOfTheDayRecurringAction(user.getHandle())
            else:
                raise RuntimeError(f'Unknown RecurringActionType: \"{actionType}\"')

            if action is not None and not action.isEnabled():
                action = None
            elif mostRecentAction is not None and action is not None:
                if now < mostRecentAction.getDateTime() + self.__cooldown:
                    action = None
                else:
                    minutesBetweenInt = action.getMinutesBetween()

                    if not utils.isValidInt(minutesBetweenInt):
                        minutesBetweenInt = action.getActionType().getDefaultRecurringActionTimingMinutes()

                    minutesBetween = timedelta(minutes = minutesBetweenInt)

                    if now < mostRecentAction.getDateTime() + minutesBetween:
                        action = None

        return action

    async def __processRecurringAction(self, user: UserInterface, action: RecurringAction):
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(action, RecurringAction), f"malformed {action=}"

        if not action.isEnabled():
            raise RuntimeError(f'Attempting to process a disabled action: \"{action}\"')

        actionType = action.getActionType()

        if actionType is RecurringActionType.SUPER_TRIVIA:
            return await self.__processSuperTriviaRecurringAction(
                user = user,
                action = action
            )
        elif actionType is RecurringActionType.WEATHER:
            return await self.__processWeatherRecurringAction(
                user = user,
                action = action
            )
        elif actionType is RecurringActionType.WORD_OF_THE_DAY:
            return await self.__processWordOfTheDayRecurringAction(
                user = user,
                action = action
            )
        else:
            raise RuntimeError(f'Unknown RecurringActionType: \"{actionType}\"')

    async def __processSuperTriviaRecurringAction(
        self,
        user: UserInterface,
        action: SuperTriviaRecurringAction
    ) -> bool:
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(action, SuperTriviaRecurringAction), f"malformed {action=}"

        newTriviaGame = await self.__triviaGameBuilder.createNewSuperTriviaGame(
            twitchChannel = user.getHandle(),
            numberOfGames = 1
        )

        if newTriviaGame is None:
            return False

        await self.__submitEvent(SuperTriviaRecurringEvent(
            twitchChannel = action.getTwitchChannel()
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
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(action, WeatherRecurringAction), f"malformed {action=}"

        if self.__weatherRepository is None:
            return False

        locationId = user.getLocationId()
        if not utils.isValidStr(locationId):
            return False

        location = await self.__locationsRepository.getLocation(locationId)
        weatherReport: Optional[WeatherReport] = None

        try:
            weatherReport = await self.__weatherRepository.fetchWeather(location)
        except:
            pass

        if weatherReport is None:
            return False
        elif action.isAlertsOnly() and not weatherReport.hasAlerts():
            return False

        await self.__submitEvent(WeatherRecurringEvent(
            twitchChannel = action.getTwitchChannel(),
            alertsOnly = action.isAlertsOnly(),
            weatherReport = weatherReport
        ))

        return True

    async def __processWordOfTheDayRecurringAction(
        self,
        user: UserInterface,
        action: WordOfTheDayRecurringAction
    ) -> bool:
        assert isinstance(user, UserInterface), f"malformed {user=}"
        assert isinstance(action, WordOfTheDayRecurringAction), f"malformed {action=}"

        languageEntry = action.getLanguageEntry()

        if languageEntry is None:
            return False

        wordOfTheDayResponse: Optional[WordOfTheDayResponse] = None

        try:
            wordOfTheDayResponse = await self.__wordOfTheDayRepository.fetchWotd(languageEntry)
        except:
            pass

        if wordOfTheDayResponse is None:
            return False

        await self.__submitEvent(WordOfTheDayRecurringEvent(
            languageEntry = languageEntry,
            twitchChannel = action.getTwitchChannel(),
            wordOfTheDayResponse = wordOfTheDayResponse
        ))

        return True

    async def __refreshActions(self):
        users = await self.__fetchViableUsers()

        userToRecurringAction: Dict[UserInterface, RecurringAction] = dict()
        twitchHandles: List[str] = list()

        for user in users:
            action = await self.__findDueRecurringAction(user)

            if action is not None:
                userToRecurringAction[user] = action
                twitchHandles.append(user.getHandle().lower())

        if not utils.hasItems(userToRecurringAction) or not utils.hasItems(twitchHandles):
            return

        usersToLiveStatus = await self.__isLiveOnTwitchRepository.isLive(twitchHandles)

        for user, action in userToRecurringAction.items():
            if not usersToLiveStatus.get(user.getHandle().lower(), False):
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

    def setEventListener(self, listener: Optional[RecurringActionEventListener]):
        assert listener is None or isinstance(listener, RecurringActionEventListener), f"malformed {listener=}"

        self.__eventListener = listener

    async def __startEventLoop(self):
        while True:
            eventListener = self.__eventListener

            if eventListener is not None:
                events: List[RecurringEvent] = list()

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
        assert isinstance(event, RecurringEvent), f"malformed {event=}"

        try:
            self.__eventQueue.put(event, block = True, timeout = self.__queueTimeoutSeconds)
        except queue.Full as e:
            self.__timber.log('RecurringActionsMachine', f'Encountered queue.Full when submitting a new event ({event}) into the event queue (queue size: {self.__eventQueue.qsize()}): {e}', e, traceback.format_exc())
