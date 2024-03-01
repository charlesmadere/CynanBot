from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.recurringActions.recurringAction import RecurringAction


class RecurringActionsHelperInterface(ABC):

    @abstractmethod
    async def disableRecurringAction(
        self,
        recurringAction: Optional[RecurringAction]
    ) -> bool:
        pass
