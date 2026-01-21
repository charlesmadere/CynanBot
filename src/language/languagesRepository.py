import random
from typing import Final

from frozenlist import FrozenList

from .exceptions import NoLanguageEntryFoundForCommandException, NoLanguageEntryFoundForWotdApiCodeException
from .languageEntry import LanguageEntry
from .languagesRepositoryInterface import LanguagesRepositoryInterface
from ..misc import utils as utils


class LanguagesRepository(LanguagesRepositoryInterface):

    def __init__(self):
        self.__languageList: Final[FrozenList[LanguageEntry]] = self.__createLanguageList()

    def __createLanguageList(self) -> FrozenList[LanguageEntry]:
        languagesList: list[LanguageEntry] = list(LanguageEntry)
        languagesList.sort(key = lambda element: element.name.casefold())

        frozenLanguagesList: FrozenList[LanguageEntry] = FrozenList(languagesList)
        frozenLanguagesList.freeze()

        return frozenLanguagesList

    async def getAllWotdApiCodes(
        self,
        delimiter: str = ', ',
    ) -> str:
        if not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        wotdApiCodes: list[str] = list()
        validEntries = await self.__getLanguageEntries(hasWotdApiCode = True)

        for entry in validEntries:
            wotdApiCodes.append(entry.primaryCommandName)

        wotdApiCodes.sort(key = lambda commandName: commandName.casefold())
        return delimiter.join(wotdApiCodes)

    async def getExampleLanguageEntry(
        self,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None,
    ) -> LanguageEntry:
        if hasIso6391Code is not None and not utils.isValidBool(hasIso6391Code):
            raise TypeError(f'hasIso6391Code argument is malformed: \"{hasIso6391Code}\"')
        elif hasWotdApiCode is not None and not utils.isValidBool(hasWotdApiCode):
            raise TypeError(f'hasWotdApiCode argument is malformed: \"{hasWotdApiCode}\"')

        validEntries = await self.__getLanguageEntries(
            hasIso6391Code = hasIso6391Code,
            hasWotdApiCode = hasWotdApiCode,
        )

        return random.choice(validEntries)

    async def __getLanguageEntries(
        self,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None,
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

        if len(validEntries) == 0:
            raise RuntimeError(f'Unable to find a single LanguageEntry with given requirements ({hasIso6391Code=}) ({hasWotdApiCode=})')

        return validEntries

    async def getLanguageForCommand(
        self,
        command: str,
        hasIso6391Code: bool | None = None,
        hasWotdApiCode: bool | None = None,
    ) -> LanguageEntry | None:
        if not utils.isValidStr(command):
            raise TypeError(f'command argument is malformed: \"{command}\"')
        elif hasIso6391Code is not None and not utils.isValidBool(hasIso6391Code):
            raise TypeError(f'hasIso6391Code argument is malformed: \"{hasIso6391Code}\"')
        elif hasWotdApiCode is not None and not utils.isValidBool(hasWotdApiCode):
            raise TypeError(f'hasWotdApiCode argumet is malformed: \"{hasWotdApiCode}\"')

        validEntries = await self.__getLanguageEntries(
            hasIso6391Code = hasIso6391Code,
            hasWotdApiCode = hasWotdApiCode,
        )

        command = command.casefold()

        for entry in validEntries:
            for entryCommandName in entry.commandNames:
                if entryCommandName.casefold() == command:
                    return entry

        return None

    async def getLanguageForIso6391Code(
        self,
        iso6391Code: str,
    ) -> LanguageEntry | None:
        if not utils.isValidStr(iso6391Code):
            raise TypeError(f'iso6391Code argument is malformed: \"{iso6391Code}\"')

        for languageEntry in LanguageEntry:
            if languageEntry.iso6391Code == iso6391Code:
                return languageEntry

        return None

    async def getLanguageForWotdApiCode(
        self,
        wotdApiCode: str,
    ) -> LanguageEntry | None:
        if not utils.isValidStr(wotdApiCode):
            raise TypeError(f'wotdApiCode argument is malformed: \"{wotdApiCode}\"')

        validEntries = await self.__getLanguageEntries(
            hasWotdApiCode = True,
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
        hasWotdApiCode: bool | None = None,
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
            hasWotdApiCode = hasWotdApiCode,
        )

        if languageEntry is None:
            raise NoLanguageEntryFoundForCommandException(
                message = f'Unable to find LanguageEntry for command ({command=})',
                command = command,
            )

        return languageEntry

    async def requireLanguageForWotdApiCode(
        self,
        wotdApiCode: str,
    ) -> LanguageEntry:
        if not utils.isValidStr(wotdApiCode):
            raise TypeError(f'wotdApiCode argument is malformed: \"{wotdApiCode}\"')

        languageEntry = await self.getLanguageForWotdApiCode(
            wotdApiCode = wotdApiCode,
        )

        if languageEntry is None:
            raise NoLanguageEntryFoundForWotdApiCodeException(
                message = f'Unable to find LanguageEntry for wotdApiCode ({wotdApiCode=})',
                wotdApiCode = wotdApiCode,
            )

        return languageEntry
