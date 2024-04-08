from typing import Any

from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionType import RecurringActionType


class WordOfTheDayRecurringAction(RecurringAction):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        twitchChannelId: str,
        minutesBetween: int | None = None,
        languageEntry: LanguageEntry | None = None
    ):
        super().__init__(
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween
        )

        if languageEntry is not None and not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        self.__languageEntry: LanguageEntry | None = languageEntry

    def getActionType(self) -> RecurringActionType:
        return RecurringActionType.WORD_OF_THE_DAY

    def getLanguageEntry(self) -> LanguageEntry | None:
        return self.__languageEntry

    def requireLanguageEntry(self) -> LanguageEntry:
        languageEntry = self.__languageEntry

        if languageEntry is None:
            raise RuntimeError(f'No languageEntry value has been set!')

        return languageEntry

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionType': self.getActionType(),
            'enabled': self.isEnabled(),
            'languageEntry': self.__languageEntry,
            'minutesBetween': self.getMinutesBetween(),
            'twitchChannel': self.getTwitchChannel(),
            'twitchChannelId': self.getTwitchChannelId()
        }
