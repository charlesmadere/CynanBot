class Wotd():
    def __init__(
        self,
        definition: str,
        englishExample: str,
        foreignExample: str,
        language: str,
        transliteration: str,
        word: str
    ):
        if definition == None or len(definition) == 0 or definition.isspace():
            raise ValueError(f'definition argument is malformed: \"{definition}\"')
        elif language == None or len(language) == 0 or language.isspace():
            raise ValueError(f'language argument is malformed: \"{language}\"')
        elif word == None or len(word) == 0 or word.isspace():
            raise ValueError(f'word argument is malformed: \"{word}\"')

        self.__definition = definition
        self.__englishExample = englishExample
        self.__foreignExample = foreignExample
        self.__language = language
        self.__transliteration = transliteration
        self.__word = word

    def getDefinition(self):
        return self.__definition

    def getEnglishExample(self):
        return self.__englishExample

    def getForeignExample(self):
        return self.__foreignExample

    def getLanguage(self):
        return self.__language

    def getTransliteration(self):
        return self.__transliteration

    def getWord(self):
        return self.__word

    def hasExamples(self):
        return (
            self.__englishExample != None and len(self.__englishExample) != 0 and not self.__englishExample.isspace() and
            self.__foreignExample != None and len(self.__foreignExample) != 0 and not self.__foreignExample.isspace()
        )

    def hasTransliteration(self):
        return self.__transliteration != None and len(self.__transliteration) != 0 and not self.__transliteration.isspace()
