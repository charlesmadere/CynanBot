import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.recurringActions.recurringActionType import RecurringActionType


class MostRecentRecurringAction():

    def __init__(
        self,
        actionType: RecurringActionType,
        dateTime: SimpleDateTime,
        twitchChannel: str
    ):
        assert isinstance(actionType, RecurringActionType), f"malformed {actionType=}"
        assert isinstance(dateTime, SimpleDateTime), f"malformed {dateTime=}"
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__actionType: RecurringActionType = actionType
        self.__dateTime: SimpleDateTime = dateTime
        self.__twitchChannel: str = twitchChannel

    def getActionType(self) -> RecurringActionType:
        return self.__actionType

    def getDateTime(self) -> SimpleDateTime:
        return self.__dateTime

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
