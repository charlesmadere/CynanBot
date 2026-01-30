from typing import Final

from .actions.cutenessRecurringAction import CutenessRecurringAction
from .actions.recurringAction import RecurringAction
from .actions.superTriviaRecurringAction import SuperTriviaRecurringAction
from .actions.weatherRecurringAction import WeatherRecurringAction
from .actions.wordOfTheDayRecurringAction import WordOfTheDayRecurringAction
from .recurringActionsHelperInterface import RecurringActionsHelperInterface
from .recurringActionsRepositoryInterface import RecurringActionsRepositoryInterface
from ..timber.timberInterface import TimberInterface


class RecurringActionsHelper(RecurringActionsHelperInterface):

    def __init__(
        self,
        recurringActionsRepository: RecurringActionsRepositoryInterface,
        timber: TimberInterface,
    ):
        if not isinstance(recurringActionsRepository, RecurringActionsRepositoryInterface):
            raise TypeError(f'recurringActionsRepository argument is malformed: \"{recurringActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__recurringActionsRepository: Final[RecurringActionsRepositoryInterface] = recurringActionsRepository
        self.__timber: Final[TimberInterface] = timber

    async def __disableCutenessRecurringAction(self, recurringAction: CutenessRecurringAction):
        await self.__recurringActionsRepository.setRecurringAction(CutenessRecurringAction(
            enabled = False,
            twitchChannel = recurringAction.twitchChannel,
            twitchChannelId = recurringAction.twitchChannelId,
            minutesBetween = recurringAction.minutesBetween,
        ))

    async def disableRecurringAction(self, recurringAction: RecurringAction | None) -> bool:
        if recurringAction is not None and not isinstance(recurringAction, RecurringAction):
            raise TypeError(f'recurringAction argument is malformed: \"{recurringAction}\"')

        if recurringAction is None:
            self.__timber.log('RecurringActionsHelper', f'Not disabling the given RecurringAction as it is None: \"{recurringAction}\"')
            return False
        elif not recurringAction.isEnabled:
            self.__timber.log('RecurringActionsHelper', f'Not disabling the given RecurringAction as it is already disabled: \"{recurringAction}\"')
            return False

        if isinstance(recurringAction, CutenessRecurringAction):
            await self.__disableCutenessRecurringAction(recurringAction)
        elif isinstance(recurringAction, SuperTriviaRecurringAction):
            await self.__disableSuperTriviaRecurringAction(recurringAction)
        elif isinstance(recurringAction, WeatherRecurringAction):
            await self.__disableWeatherRecurringAction(recurringAction)
        elif isinstance(recurringAction, WordOfTheDayRecurringAction):
            await self.__disableWordOfTheDayRecurringAction(recurringAction)
        else:
            raise ValueError(f'unknown RecurringAction instance ({recurringAction=})')

        self.__timber.log('RecurringActionsHelper', f'Finished disabling RecurringAction ({recurringAction=})')
        return True

    async def __disableSuperTriviaRecurringAction(self, recurringAction: SuperTriviaRecurringAction):
        await self.__recurringActionsRepository.setRecurringAction(SuperTriviaRecurringAction(
            enabled = False,
            twitchChannel = recurringAction.twitchChannel,
            twitchChannelId = recurringAction.twitchChannelId,
            minutesBetween = recurringAction.minutesBetween,
        ))

    async def __disableWeatherRecurringAction(self, recurringAction: WeatherRecurringAction):
        await self.__recurringActionsRepository.setRecurringAction(WeatherRecurringAction(
            enabled = False,
            twitchChannel = recurringAction.twitchChannel,
            twitchChannelId = recurringAction.twitchChannelId,
            alertsOnly = recurringAction.isAlertsOnly,
            minutesBetween = recurringAction.minutesBetween,
        ))

    async def __disableWordOfTheDayRecurringAction(self, recurringAction: WordOfTheDayRecurringAction):
        await self.__recurringActionsRepository.setRecurringAction(WordOfTheDayRecurringAction(
            enabled = False,
            twitchChannel = recurringAction.twitchChannel,
            twitchChannelId = recurringAction.twitchChannelId,
            minutesBetween = recurringAction.minutesBetween,
            languageEntry = recurringAction.languageEntry,
        ))
