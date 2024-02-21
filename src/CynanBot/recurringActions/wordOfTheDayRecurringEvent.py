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

        assert isinstance(languageEntry, LanguageEntry), f"malformed {languageEntry=}"
        assert isinstance(wordOfTheDayResponse, WordOfTheDayResponse), f"malformed {wordOfTheDayResponse=}"

        self.__languageEntry: LanguageEntry = languageEntry
        self.__wordOfTheDayResponse: WordOfTheDayResponse = wordOfTheDayResponse

    def getEventType(self) -> RecurringEventType:
        return RecurringEventType.WORD_OF_THE_DAY

    def getLanguageEntry(self) -> LanguageEntry:
        return self.__languageEntry

    def getWordOfTheDayResponse(self) -> WordOfTheDayResponse:
        return self.__wordOfTheDayResponse
