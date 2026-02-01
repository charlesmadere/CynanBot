from typing import Any, Final

from .recurringAction import RecurringAction
from .recurringActionType import RecurringActionType
from ...language.languageEntry import LanguageEntry


class WordOfTheDayRecurringAction(RecurringAction):

    def __init__(
        self,
        enabled: bool,
        twitchChannel: str,
        twitchChannelId: str,
        minutesBetween: int | None = None,
        languageEntry: LanguageEntry | None = None,
    ):
        super().__init__(
            enabled = enabled,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId,
            minutesBetween = minutesBetween,
        )

        if languageEntry is not None and not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')

        self.__languageEntry: Final[LanguageEntry | None] = languageEntry

    @property
    def actionType(self) -> RecurringActionType:
        return RecurringActionType.WORD_OF_THE_DAY

    @property
    def languageEntry(self) -> LanguageEntry | None:
        return self.__languageEntry

    def requireLanguageEntry(self) -> LanguageEntry:
        languageEntry = self.__languageEntry

        if languageEntry is None:
            raise RuntimeError(f'No languageEntry value has been set!')

        return languageEntry

    def toDictionary(self) -> dict[str, Any]:
        return {
            'actionType': self.actionType,
            'enabled': self.isEnabled,
            'languageEntry': self.__languageEntry,
            'minutesBetween': self.minutesBetween,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
        }
