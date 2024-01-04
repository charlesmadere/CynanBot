from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry


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
        if not isinstance(languageEntry, LanguageEntry):
            raise ValueError(f'languageEntry argument is malformed: \"{languageEntry}\"')
        elif not utils.isValidStr(definition):
            raise ValueError(f'definition argument is malformed: \"{definition}\"')
        elif englishExample is not None and not isinstance(englishExample, str):
            raise ValueError(f'englishExample argument is malformed: \"{englishExample}\"')
        elif foreignExample is not None and not isinstance(foreignExample, str):
            raise ValueError(f'foreignExample argument is malformed: \"{foreignExample}\"')
        elif transliteration is not None and not isinstance(transliteration, str):
            raise ValueError(f'transliteration argument is malformed: \"{transliteration}\"')
        elif not utils.isValidStr(word):
            raise ValueError(f'word argument is malformed: \"{word}\"')

        self.__languageEntry: LanguageEntry = languageEntry
        self.__definition: str = definition
        self.__englishExample: Optional[str] = englishExample
        self.__foreignExample: Optional[str] = foreignExample
        self.__transliteration: Optional[str] = transliteration
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
