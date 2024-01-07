from typing import Any, Dict, Optional

from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.recurringActions.recurringAction import RecurringAction
from CynanBot.recurringActions.recurringActionType import RecurringActionType


class WordOfTheDayRecurringAction(RecurringAction):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        minutesBetween: Optional[int] = None,
        languageEntry: Optional[LanguageEntry] = None
    ):
        super().__init__(
            enabled = enabled,
            twitchChannel = twitchChannel,
            minutesBetween = minutesBetween
        )

        if languageEntry is not None and not isinstance(languageEntry, LanguageEntry):
            raise ValueError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        self.__languageEntry: Optional[LanguageEntry] = languageEntry

    def getActionType(self) -> RecurringActionType:
        return RecurringActionType.WORD_OF_THE_DAY

    def getLanguageEntry(self) -> Optional[LanguageEntry]:
        return self.__languageEntry

    def hasLanguageEntry(self) -> bool:
        return self.__languageEntry is not None

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def requireLanguageEntry(self) -> LanguageEntry:
        languageEntry = self.__languageEntry

        if languageEntry is None:
            raise RuntimeError(f'No languageEntry value has been set!')

        return languageEntry

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'actionType': self.getActionType(),
            'enabled': self.isEnabled(),
            'languageEntry': self.__languageEntry,
            'minutesBetween': self.getMinutesBetween(),
            'twitchChannel': self.getTwitchChannel()
        }
