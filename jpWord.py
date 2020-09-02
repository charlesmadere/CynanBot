class JpWord():
    def __init__(
        self,
        word: str,
        definition: str,
        romaji: str
    ):
        if word == None or len(word) == 0 or word.isspace():
            raise ValueError(f'word argument is malformed: \"{word}\"')
        elif definition == None or len(definition) == 0 or definition.isspace():
            raise ValueError(f'definition argument is malformed: \"{definition}\"')
        elif romaji == None or len(romaji) == 0 or romaji.isspace():
            raise ValueError(f'romaji argument is malformed: \"{romaji}\"')

        self.__word = word
        self.__definition = definition
        self.__romaji = romaji

    def getDefinition(self):
        return self.__definition

    def getRomaji(self):
        return self.__romaji

    def getWord(self):
        return self.__word
