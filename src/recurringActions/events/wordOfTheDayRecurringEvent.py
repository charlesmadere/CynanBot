from dataclasses import dataclass

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...language.languageEntry import LanguageEntry
from ...language.wordOfTheDay.wordOfTheDayResponse import WordOfTheDayResponse


@dataclass(frozen = True)
class WordOfTheDayRecurringEvent(RecurringEvent):
    languageEntry: LanguageEntry
    twitchChannel: str
    twitchChannelId: str
    wordOfTheDayResponse: WordOfTheDayResponse

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.WORD_OF_THE_DAY
