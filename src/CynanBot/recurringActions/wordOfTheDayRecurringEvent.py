from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.wordOfTheDayResponse import WordOfTheDayResponse
from CynanBot.recurringActions.recurringEvent import RecurringEvent
from CynanBot.recurringActions.recurringEventType import RecurringEventType


class WordOfTheDayRecurringEvent(RecurringEvent):

    def __init__(
        self,
        languageEntry: LanguageEntry,
        twitchChannel: str,
        wordOfTheDayResponse: WordOfTheDayResponse
    ):
        super().__init__(twitchChannel = twitchChannel)

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
