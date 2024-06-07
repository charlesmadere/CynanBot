import CynanBot.misc.utils as utils
from CynanBot.language.wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from CynanBot.language.wordOfTheDayResponse import WordOfTheDayResponse


class WordOfTheDayPresenter(WordOfTheDayPresenterInterface):

    async def toString(
        self,
        wordOfTheDay: WordOfTheDayResponse
    ) -> str:
        if not isinstance(wordOfTheDay, WordOfTheDayResponse):
            raise TypeError(f'wordOfTheDayResponse argument is malformed: \"{wordOfTheDay}\"')

        languageNameAndFlag: str
        if wordOfTheDay.languageEntry.hasFlag():
            languageNameAndFlag = f'{wordOfTheDay.languageEntry.getFlag()} {wordOfTheDay.languageEntry.getName()}'
        else:
            languageNameAndFlag = wordOfTheDay.languageEntry.getName()

        transliteration: str | None = None
        hasTransliteratedWord = utils.isValidStr(wordOfTheDay.transparentResponse.transliteratedWord)

        if hasTransliteratedWord:
            transliteration = f' ({wordOfTheDay.transparentResponse.transliteratedWord})'

        return f'{languageNameAndFlag} — {wordOfTheDay.transparentResponse.word}{transliteration} — {wordOfTheDay.transparentResponse.translation}. Example: {wordOfTheDay.transparentResponse.fnPhrase} {wordOfTheDay.transparentResponse.enPhrase}'.strip()