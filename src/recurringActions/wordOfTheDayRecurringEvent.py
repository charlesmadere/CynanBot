from typing import Any

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ..language.languageEntry import LanguageEntry
from ..language.wordOfTheDayResponse import WordOfTheDayResponse


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

    def getEventType(self) -> RecurringEventType:
        return RecurringEventType.WORD_OF_THE_DAY

    def getLanguageEntry(self) -> LanguageEntry:
        return self.__languageEntry

    def getWordOfTheDayResponse(self) -> WordOfTheDayResponse:
        return self.__wordOfTheDayResponse

    def toDictionary(self) -> dict[str, Any]:
        return {
            'eventType': self.getEventType(),
            'languageEntry': self.__languageEntry,
            'twitchChannel': self.getTwitchChannel(),
            'twitchChannelId': self.getTwitchChannelId(),
            'wordOfTheDayResponse': self.getWordOfTheDayResponse()
        }
