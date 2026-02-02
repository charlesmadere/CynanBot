from .wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from .wordOfTheDayResponse import WordOfTheDayResponse
from ...misc import utils as utils


class WordOfTheDayPresenter(WordOfTheDayPresenterInterface):

    async def toString(
        self,
        includeRomaji: bool,
        wordOfTheDay: WordOfTheDayResponse,
    ) -> str:
        if not utils.isValidBool(includeRomaji):
            raise TypeError(f'includeRomaji argument is malformed: \"{includeRomaji}\"')
        elif not isinstance(wordOfTheDay, WordOfTheDayResponse):
            raise TypeError(f'wordOfTheDayResponse argument is malformed: \"{wordOfTheDay}\"')

        languageNameAndFlag: str
        if utils.isValidStr(wordOfTheDay.languageEntry.flag):
            languageNameAndFlag = f'{wordOfTheDay.languageEntry.flag} {wordOfTheDay.languageEntry.humanName}'
        else:
            languageNameAndFlag = wordOfTheDay.languageEntry.humanName

        transliteration: str = ''
        hasTransliteratedWord = utils.isValidStr(wordOfTheDay.transparentResponse.transliteratedWord)

        if hasTransliteratedWord:
            transliteration = f' ({wordOfTheDay.transparentResponse.transliteratedWord})'

        return f'{languageNameAndFlag} — {wordOfTheDay.transparentResponse.word}{transliteration} — {wordOfTheDay.transparentResponse.translation}. Example: {wordOfTheDay.transparentResponse.fnPhrase} {wordOfTheDay.transparentResponse.enPhrase}'.strip()
