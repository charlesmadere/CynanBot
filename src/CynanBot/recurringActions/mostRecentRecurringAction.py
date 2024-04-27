from dataclasses import dataclass
from datetime import datetime

from CynanBot.recurringActions.recurringActionType import RecurringActionType


@dataclass(frozen = True)
class MostRecentRecurringAction():
    dateTime: datetime
    actionType: RecurringActionType
    twitchChannel: str
