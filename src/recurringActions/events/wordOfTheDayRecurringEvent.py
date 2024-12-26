from typing import Any

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...language.languageEntry import LanguageEntry
from ...language.wordOfTheDay.wordOfTheDayResponse import WordOfTheDayResponse


class WordOfTheDayRecurringEvent(RecurringEvent):

    def __init__(
        self,
        languageEntry: LanguageEntry,
        twitchChannel: str,
        twitchChannelId: str,
        wordOfTheDayResponse: WordOfTheDayResponse
    ):
        super().__init__(
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not isinstance(languageEntry, LanguageEntry):
            raise TypeError(f'languageEntry argument is malformed: \"{languageEntry}\"')
        elif not isinstance(wordOfTheDayResponse, WordOfTheDayResponse):
            raise TypeError(f'wordOfTheDayResponse argument is malformed: \"{wordOfTheDayResponse}\"')

        self.__languageEntry: LanguageEntry = languageEntry
        self.__wordOfTheDayResponse: WordOfTheDayResponse = wordOfTheDayResponse

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.WORD_OF_THE_DAY

    @property
    def languageEntry(self) -> LanguageEntry:
        return self.__languageEntry

    @property
    def wordOfTheDayResponse(self) -> WordOfTheDayResponse:
        return self.__wordOfTheDayResponse

    def toDictionary(self) -> dict[str, Any]:
        return {
            'eventType': self.eventType,
            'languageEntry': self.__languageEntry,
            'twitchChannel': self.twitchChannel,
            'twitchChannelId': self.twitchChannelId,
            'wordOfTheDayResponse': self.__wordOfTheDayResponse
        }
