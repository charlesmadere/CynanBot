from wotd import Wotd

class TransliteratableWotd(Wotd):
    def __init__(self,
        definition: str,
        englishExample: str,
        foreignExample: str,
        transliteration: str,
        word: str,
    ):
        super().__init__(
            definition = definition,
            englishExample = englishExample,
            foreignExample = foreignExample,
            word = word,
        )

        if transliteration == None or len(transliteration) == 0 or transliteration.isspace():
            raise ValueError(f'transliteration argument is malformed: \"{transliteration}\"')

        self.__transliteration = transliteration

    def getTransliteration(self):
        return self.__transliteration
