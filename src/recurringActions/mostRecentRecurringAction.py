from dataclasses import dataclass
from datetime import datetime

from .actions.recurringActionType import RecurringActionType


@dataclass(frozen = True, slots = True)
class MostRecentRecurringAction:
    dateTime: datetime
    actionType: RecurringActionType
    twitchChannel: str
    twitchChannelId: str
