from abc import ABC, abstractmethod

from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.absWizard import AbsWizard


class RecurringActionsWizardInterface(ABC):

    @abstractmethod
    async def complete(self, twitchChannelId: str):
        pass

    @abstractmethod
    async def get(self, twitchChannelId: str) -> AbsWizard | None:
        pass

    @abstractmethod
    async def start(
        self,
        recurringActionType: RecurringActionType,
        twitchChannel: str,
        twitchChannelId: str
    ) -> AbsWizard:
        pass
