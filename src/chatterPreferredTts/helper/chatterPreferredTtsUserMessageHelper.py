import re
from typing import Any, Match, Pattern

from .chatterPreferredTtsUserMessageHelperInterface import ChatterPreferredTtsUserMessageHelperInterface
from ..models.absPreferredTts import AbsPreferredTts
from ..models.decTalk.decTalkPreferredTts import DecTalkPreferredTts
from ..models.google.googlePreferredTts import GooglePreferredTts
from ..models.microsoftSam.microsoftSamPreferredTts import MicrosoftSamPreferredTts
from ...language.languageEntry import LanguageEntry
from ...language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ...misc import utils as utils


class ChatterPreferredTtsUserMessageHelper(ChatterPreferredTtsUserMessageHelperInterface):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')

        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository

        self.__decTalkRegEx: Pattern = re.compile(r'^\s*dec(\s+|_|-)?talk\s*$', re.IGNORECASE)
        self.__googleRegEx: Pattern = re.compile(r'^\s*goog(le?)?\s*(\w+)\s*$', re.IGNORECASE)
        self.__microsoftSamRegEx: Pattern = re.compile(r'^\s*(microsoft|ms)(\s|_|-)*sam\s*$', re.IGNORECASE)

    async def __createDecTalkTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return DecTalkPreferredTts()

    async def __createGoogleTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        languageEntry: LanguageEntry | None = None
        languageEntryCommand = match.group(2)

        if utils.isValidStr(languageEntryCommand):
            languageEntry = await self.__languagesRepository.getLanguageForCommand(
                command = languageEntryCommand
            )

        return GooglePreferredTts(
            languageEntry = languageEntry
        )

    async def __createMicrosoftSamTtsProperties(
        self,
        match: Match[str]
    ) -> AbsPreferredTts | None:
        if not isinstance(match, Match):
            raise TypeError(f'match argument is malformed: \"{match}\"')

        return MicrosoftSamPreferredTts()

    async def parseUserMessage(
        self,
        userMessage: str | Any | None
    ) -> AbsPreferredTts | None:
        if not utils.isValidStr(userMessage):
            return None

        userMessage = utils.cleanStr(userMessage)
        decTalkMatch = self.__decTalkRegEx.fullmatch(userMessage)
        googleMatch = self.__googleRegEx.fullmatch(userMessage)
        microsoftSamMatch = self.__microsoftSamRegEx.fullmatch(userMessage)

        if decTalkMatch is not None:
            return await self.__createDecTalkTtsProperties(decTalkMatch)

        elif googleMatch is not None:
            return await self.__createGoogleTtsProperties(googleMatch)

        elif microsoftSamMatch is not None:
            return await self.__createMicrosoftSamTtsProperties(microsoftSamMatch)

        else:
            return None
