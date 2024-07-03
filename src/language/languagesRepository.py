import random

from .languageEntry import LanguageEntry
from .languagesRepositoryInterface import LanguagesRepositoryInterface
from ..misc import utils as utils


class LanguagesRepository(LanguagesRepositoryInterface):

    def __init__(self):
        self.__languageList: list[LanguageEntry] = self.__createLanguageList()

    def __createLanguageList(self) -> list[LanguageEntry]:
        languagesList: list[LanguageEntry] = list()

        languagesList.append(LanguageEntry(
            commandNames = [ 'de', 'deutsche', 'german', 'germany' ],
            flag = '🇩🇪',
            iso6391Code = 'de',
            name = 'German',
            wotdApiCode = 'de'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'en', 'eng', 'english', '英語' ],
            flag = '🇬🇧',
            iso6391Code = 'en',
            name = 'English'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'en-es' ],
            name = 'English for Spanish speakers',
            wotdApiCode = 'en-es'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'en-pt' ],
            name = 'English for Portuguese speakers',
            wotdApiCode = 'en-pt'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'es', 'español', 'sp', 'spanish' ],
            iso6391Code = 'es',
            name = 'Spanish',
            wotdApiCode = 'es'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'fr', 'français', 'france', 'french' ],
            flag = '🇫🇷',
            iso6391Code = 'fr',
            name = 'French',
            wotdApiCode = 'fr'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'el', 'greek' ],
            flag = '🇬🇷',
            iso6391Code = 'el',
            name = 'Greek'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'hi', 'hin', 'hindi' ],
            flag = '🇮🇳',
            iso6391Code = 'hi',
            name = 'Hindi',
            wotdApiCode = 'hindi'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'it', 'italian', 'italiano', 'italy' ],
            flag = '🇮🇹',
            iso6391Code = 'it',
            name = 'Italian',
            wotdApiCode = 'it'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'ja', 'japan', 'japanese', 'jp', '日本語', 'にほんご' ],
            flag = '🇯🇵',
            iso6391Code = 'ja',
            name = 'Japanese',
            wotdApiCode = 'ja'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'ko', 'korea', 'korean', '한국어' ],
            flag = '🇰🇷',
            iso6391Code = 'ko',
            name = 'Korean',
            wotdApiCode = 'korean'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'la', 'latin' ],
            iso6391Code = 'la',
            name = 'Latin'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'nl', 'dutch', 'nederlands', 'netherlands', 'vlaams' ],
            flag = '🇳🇱',
            iso6391Code = 'nl',
            name = 'Dutch',
            wotdApiCode = 'nl'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'no', 'norsk', 'norway', 'norwegian' ],
            flag = '🇳🇴',
            iso6391Code = 'no',
            name = 'Norwegian',
            wotdApiCode = 'norwegian'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'po', 'poland', 'polish' ],
            flag = '🇵🇱',
            iso6391Code = 'pl',
            name = 'Polish',
            wotdApiCode = 'polish',
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'pt', 'portuguese', 'português' ],
            flag = '🇵🇹',
            iso6391Code = 'pt',
            name = 'Portuguese',
            wotdApiCode = 'pt'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'ru', 'russia', 'russian', 'русский' ],
            flag = '🇷🇺',
            iso6391Code = 'ru',
            name = 'Russian',
            wotdApiCode = 'ru'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'se', 'sv', 'svenska', 'sw', 'sweden', 'swedish' ],
            flag = '🇸🇪',
            iso6391Code = 'sv',
            name = 'Swedish',
            wotdApiCode = 'swedish',
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'th', 'thai' ],
            flag = '🇹🇭',
            iso6391Code = 'th',
            name = 'Thai'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'ur', 'urd', 'urdu' ],
            flag = '🇵🇰',
            iso6391Code = 'ur',
            name = 'Urdu',
            wotdApiCode = 'urdu'
        ))

        languagesList.append(LanguageEntry(
            commandNames = [ 'zh', 'chinese', 'china', '中文' ],
            flag = '🇨🇳',
            iso6391Code = 'zh',
            name = 'Chinese',
            wotdApiCode = 'zh'
        ))

        if len(languagesList) == 0:
            raise RuntimeError(f'languagesList must contain at least 1 entry: \"{languagesList}\"')

        languagesNames: set[str] = set()

        for language in languagesList:
            if language.name.casefold() in languagesNames:
                raise ValueError(f'Every language name must be unique (found duplicate of \"{language.name}\"): {languagesList}')
            else:
                languagesNames.add(language.name.casefold())

        return languagesList

    async def getAllWotdApiCodes(
        self,
        delimiter: str = ', '
    ) -> str:
        if not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        wotdApiCodes: list[str] = list()
        validEntries = await self.__getLanguageEntries(hasWotdApiCode = True)

        for entry in validEntries:
            wotdApiCodes.append(entry.primaryCommandName)

        wotdApiCodes.sort(key = lambda commandName: commandName.lower())
        return delimiter.join(wotdApiCodes)

    async def getExampleLanguageEntry(
        self,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None
    ) -> LanguageEntry:
        if hasIso6391Code is not None and not utils.isValidBool(hasIso6391Code):
            raise TypeError(f'hasIso6391Code argument is malformed: \"{hasIso6391Code}\"')
        elif hasWotdApiCode is not None and not utils.isValidBool(hasWotdApiCode):
            raise TypeError(f'hasWotdApiCode argument is malformed: \"{hasWotdApiCode}\"')

        validEntries = await self.__getLanguageEntries(
            hasIso6391Code = hasIso6391Code,
            hasWotdApiCode = hasWotdApiCode
        )

        return random.choice(validEntries)

    async def __getLanguageEntries(
        self,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None
    ) -> list[LanguageEntry]:
        if hasIso6391Code is not None and not utils.isValidBool(hasIso6391Code):
            raise TypeError(f'hasIso6391Code argument is malformed: \"{hasIso6391Code}\"')
        elif hasWotdApiCode is not None and not utils.isValidBool(hasWotdApiCode):
            raise TypeError(f'hasWotdApiCode argument is malformed: \"{hasWotdApiCode}\"')

        validEntries: list[LanguageEntry] = list()

        for entry in self.__languageList:
            entryHasIso6391Code = utils.isValidStr(entry.iso6391Code)
            entryHasWotdApiCode = utils.isValidStr(entry.wotdApiCode)

            if hasIso6391Code is not None and hasWotdApiCode is not None:
                if hasIso6391Code == entryHasIso6391Code and hasWotdApiCode == entryHasWotdApiCode:
                    validEntries.append(entry)
            elif hasIso6391Code is not None:
                if hasIso6391Code == entryHasIso6391Code:
                    validEntries.append(entry)
            elif hasWotdApiCode is not None:
                if hasWotdApiCode == entryHasWotdApiCode:
                    validEntries.append(entry)
            else:
                validEntries.append(entry)

        if not utils.hasItems(validEntries):
            raise RuntimeError(f'Unable to find a single LanguageEntry with given requirements ({hasIso6391Code=}) ({hasWotdApiCode=})')

        return validEntries

    async def getLanguageForCommand(
        self,
        command: str,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None
    ) -> LanguageEntry | None:
        if not utils.isValidStr(command):
            raise TypeError(f'command argument is malformed: \"{command}\"')
        elif hasIso6391Code is not None and not utils.isValidBool(hasIso6391Code):
            raise TypeError(f'hasIso6391Code argument is malformed: \"{hasIso6391Code}\"')
        elif hasWotdApiCode is not None and not utils.isValidBool(hasWotdApiCode):
            raise TypeError(f'hasWotdApiCode argumet is malformed: \"{hasWotdApiCode}\"')

        validEntries = await self.__getLanguageEntries(
            hasIso6391Code = hasIso6391Code,
            hasWotdApiCode = hasWotdApiCode
        )

        command = command.casefold()

        for entry in validEntries:
            for entryCommandName in entry.commandNames:
                if entryCommandName.casefold() == command:
                    return entry

        return None

    async def getLanguageForWotdApiCode(
        self,
        wotdApiCode: str
    ) -> LanguageEntry | None:
        if not utils.isValidStr(wotdApiCode):
            raise TypeError(f'wotdApiCode argument is malformed: \"{wotdApiCode}\"')

        validEntries = await self.__getLanguageEntries(
            hasWotdApiCode = True
        )

        wotdApiCode = wotdApiCode.casefold()

        for entry in validEntries:
            if utils.isValidStr(entry.wotdApiCode) and entry.wotdApiCode.casefold() == wotdApiCode:
                return entry

        return None

    async def requireLanguageForCommand(
        self,
        command: str,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None
    ) -> LanguageEntry:
        if not utils.isValidStr(command):
            raise TypeError(f'command argument is malformed: \"{command}\"')
        elif hasIso6391Code is not None and not utils.isValidBool(hasIso6391Code):
            raise TypeError(f'hasIso6391Code argument is malformed: \"{hasIso6391Code}\"')
        elif hasWotdApiCode is not None and not utils.isValidBool(hasWotdApiCode):
            raise TypeError(f'hasWotdApiCode argumet is malformed: \"{hasWotdApiCode}\"')

        languageEntry = await self.getLanguageForCommand(
            command = command,
            hasIso6391Code = hasIso6391Code,
            hasWotdApiCode = hasWotdApiCode
        )

        if languageEntry is None:
            raise RuntimeError(f'Unable to find LanguageEntry for command ({command=})')

        return languageEntry

    async def requireLanguageForWotdApiCode(
        self,
        wotdApiCode: str
    ) -> LanguageEntry:
        if not utils.isValidStr(wotdApiCode):
            raise TypeError(f'wotdApiCode argument is malformed: \"{wotdApiCode}\"')

        languageEntry = await self.getLanguageForWotdApiCode(
            wotdApiCode = wotdApiCode
        )

        if languageEntry is None:
            raise RuntimeError(f'Unable to find LanguageEntry for wotdApiCode ({wotdApiCode=})')

        return languageEntry
