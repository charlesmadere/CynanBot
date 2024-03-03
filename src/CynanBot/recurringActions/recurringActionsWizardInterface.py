from abc import ABC, abstractmethod

from CynanBot.recurringActions.recurringActionType import RecurringActionType


class RecurringActionsWizardInterface(ABC):

    @abstractmethod
    async def start(
        self,
        recurringActionType: RecurringActionType,
        twitchChannel: str,
        twitchChannelId: str
    ):
        pass
