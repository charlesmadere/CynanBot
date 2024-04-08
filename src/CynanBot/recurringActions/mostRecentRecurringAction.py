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
        if not isinstance(actionType, RecurringActionType):
            raise TypeError(f'actionType argument is malformed: \"{actionType}\"')
        elif not isinstance(dateTime, SimpleDateTime):
            raise TypeError(f'dateTime argument is malformed: \"{dateTime}\"')
        elif not utils.isValidStr(twitchChannel):
            raise TypeError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        self.__actionType: RecurringActionType = actionType
        self.__dateTime: SimpleDateTime = dateTime
        self.__twitchChannel: str = twitchChannel

    def getActionType(self) -> RecurringActionType:
        return self.__actionType

    def getDateTime(self) -> SimpleDateTime:
        return self.__dateTime

    def getTwitchChannel(self) -> str:
        return self.__twitchChannel
