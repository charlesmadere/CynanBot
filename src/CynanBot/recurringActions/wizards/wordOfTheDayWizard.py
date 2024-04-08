import CynanBot.misc.utils as utils
from CynanBot.recurringActions.recurringActionType import RecurringActionType
from CynanBot.recurringActions.wizards.absWizard import AbsWizard
from CynanBot.recurringActions.wizards.wordOfTheDaySteps import \
    WordOfTheDaySteps


class WordOfTheDayWizard(AbsWizard):

    def __init__(
        self,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        self.__steps = WordOfTheDaySteps()
        self.__minutesBetween: int | None = None

    def getMinutesBetween(self) -> int | None:
        return self.__minutesBetween

    def getRecurringActionType(self) -> RecurringActionType:
        return RecurringActionType.WORD_OF_THE_DAY

    def getSteps(self) -> WordOfTheDaySteps:
        return self.__steps

    def setMinutesBetween(self, minutesBetween: int):
        if not utils.isValidInt(minutesBetween):
            raise TypeError(f'minutesBetween argument is malformed: \"{minutesBetween}\"')
        elif minutesBetween < 1 or minutesBetween > utils.getIntMaxSafeSize():
            raise ValueError(f'minutesBetween argument is out of bounds: {minutesBetween}')

        self.__minutesBetween = minutesBetween
