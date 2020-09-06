from wotd import Wotd

class JpWotd(Wotd):
    def __init__(self,
        definition: str,
        englishExample: str,
        foreignExample: str,
        romaji: str,
        word: str,
    ):
        super().__init__(
            definition = definition,
            englishExample = englishExample,
            foreignExample = foreignExample,
            word = word,
        )

        if romaji == None or len(romaji) == 0 or romaji.isspace():
            raise ValueError(f'romaji argument is malformed: \"{romaji}\"')

        self.__romaji = romaji

    def getRomaji(self):
        return self.__romaji
