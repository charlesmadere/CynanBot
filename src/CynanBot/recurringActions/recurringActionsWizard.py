from datetime import timedelta
from typing import Optional

from CynanBot.recurringActions.recurringActionsWizardInterface import \
    RecurringActionsWizardInterface
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchChannelProvider import \
    TwitchChannelProvider
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface


class RecurringActionsWizard(RecurringActionsWizardInterface):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        timePerStep: timedelta = timedelta(minutes = 1)
    ):
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__timePerStep: timedelta = timePerStep

        self.__twitchChannelProvider: Optional[TwitchChannelProvider] = None

    def setTwitchChannelProvider(self, twitchChannelProvider: Optional[TwitchChannelProvider]):
        if twitchChannelProvider is not None and not isinstance(twitchChannelProvider, TwitchChannelProvider):
            raise TypeError(f'twitchChannelProvider argument is malformed: \"{twitchChannelProvider}\"')

        self.__twitchChannelProvider = twitchChannelProvider

    async def start(self, recurringActionType: RecurringActionType, twitchChannel: str):
        twitchChannelProvider = self.__twitchChannelProvider

        if twitchChannelProvider is None:
            self.__timber.log('RecurringActionsWizard', f'Attempted to start, but twitchChannelProvider is None ({recurringActionType=}) ({twitchChannel=}) ({twitchChannelProvider=})')
            return

        pass
