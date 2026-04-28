from dataclasses import dataclass

from .recurringEvent import RecurringEvent
from .recurringEventType import RecurringEventType
from ...language.languageEntry import LanguageEntry
from ...language.wordOfTheDay.wordOfTheDayResponse import WordOfTheDayResponse
from ...users.userInterface import UserInterface


@dataclass(frozen = True, slots = True)
class WordOfTheDayRecurringEvent(RecurringEvent):
    languageEntry: LanguageEntry
    twitchChannelId: str
    twitchUser: UserInterface
    wordOfTheDayResponse: WordOfTheDayResponse

    @property
    def eventType(self) -> RecurringEventType:
        return RecurringEventType.WORD_OF_THE_DAY

    def getTwitchChannelId(self) -> str:
        return self.twitchChannelId

    def getTwitchUser(self) -> UserInterface:
        return self.twitchUser
