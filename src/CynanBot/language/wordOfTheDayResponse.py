from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.romaji import to_romaji


class WordOfTheDayResponse():

    def __init__(
        self,
        languageEntry: LanguageEntry,
        definition: str,
        englishExample: Optional[str],
        foreignExample: Optional[str],
        transliteration: Optional[str],
        word: str
    ):
        assert isinstance(languageEntry, LanguageEntry), f"malformed {languageEntry=}"
        if not utils.isValidStr(definition):
            raise ValueError(f'definition argument is malformed: \"{definition}\"')
        assert englishExample is None or isinstance(englishExample, str), f"malformed {englishExample=}"
        assert foreignExample is None or isinstance(foreignExample, str), f"malformed {foreignExample=}"
        assert transliteration is None or isinstance(transliteration, str), f"malformed {transliteration=}"
        if not utils.isValidStr(word):
            raise ValueError(f'word argument is malformed: \"{word}\"')

        self.__languageEntry: LanguageEntry = languageEntry
        self.__definition: str = definition
        self.__englishExample: Optional[str] = englishExample
        self.__foreignExample: Optional[str] = foreignExample
        self.__transliteration: Optional[str]
        romaji = to_romaji(transliteration)
        if romaji is None:
            self.__transliteration = transliteration
        else:
            self.__transliteration = f"{transliteration} - {romaji}"
        self.__word: str = word

    def getDefinition(self) -> str:
        return self.__definition

    def getEnglishExample(self) -> Optional[str]:
        return self.__englishExample

    def getForeignExample(self) -> Optional[str]:
        return self.__foreignExample

    def getLanguageEntry(self) -> LanguageEntry:
        return self.__languageEntry

    def getLanguageName(self) -> str:
        return self.__languageEntry.getName()

    def getTransliteration(self) -> Optional[str]:
        return self.__transliteration

    def getWord(self) -> str:
        return self.__word

    def hasExamples(self) -> bool:
        return utils.isValidStr(self.__englishExample) and utils.isValidStr(self.__foreignExample)

    def hasTransliteration(self) -> bool:
        return utils.isValidStr(self.__transliteration)

    def toStr(self) -> str:
        languageNameAndFlag: str

        if self.__languageEntry.hasFlag():
            languageNameAndFlag = f'{self.__languageEntry.getFlag()} {self.getLanguageName()}'
        else:
            languageNameAndFlag = self.getLanguageName()

        if self.hasExamples():
            if self.hasTransliteration():
                return f'{languageNameAndFlag} — {self.getWord()} ({self.getTransliteration()}) — {self.getDefinition()}. Example: {self.getForeignExample()} {self.getEnglishExample()}'
            else:
                return f'{languageNameAndFlag} — {self.getWord()} — {self.getDefinition()}. Example: {self.getForeignExample()} {self.getEnglishExample()}'
        elif self.hasTransliteration():
            return f'{languageNameAndFlag} — {self.getWord()} ({self.getTransliteration()}) — {self.getDefinition()}'
        else:
            return f'{languageNameAndFlag} — {self.getWord()} — {self.getDefinition()}'
