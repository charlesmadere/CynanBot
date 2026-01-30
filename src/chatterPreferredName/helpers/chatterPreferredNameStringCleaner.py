import re
from typing import Any, Final, Pattern

from .chatterPreferredNameStringCleanerInterface import ChatterPreferredNameStringCleanerInterface
from ...misc import utils as utils


class ChatterPreferredNameStringCleaner(ChatterPreferredNameStringCleanerInterface):

    def __init__(
        self,
        maxLength: int = 32,
    ):
        if not utils.isValidInt(maxLength):
            raise TypeError(f'maxLength argument is malformed: \"{maxLength}\"')
        elif maxLength < 8 or maxLength > 128:
            raise ValueError(f'maxLength argument is out of bounds: {maxLength}')

        self.__maxLength: Final[int] = maxLength

        self.__invalidCharactersRegEx: Final[Pattern] = re.compile(r'[^\w\s]', re.IGNORECASE)
        self.__spaceReplacementCharactersRegEx: Final[Pattern] = re.compile(r'[_-]', re.IGNORECASE)

    async def clean(
        self,
        preferredName: str | Any | None,
    ) -> str | None:
        if not utils.isValidStr(preferredName):
            return None

        cleanedPreferredName = utils.cleanStr(preferredName)
        cleanedPreferredName = self.__spaceReplacementCharactersRegEx.sub(' ', cleanedPreferredName).strip()
        cleanedPreferredName = self.__invalidCharactersRegEx.sub('', cleanedPreferredName).strip()
        cleanedPreferredName = utils.cleanStr(cleanedPreferredName)

        if len(cleanedPreferredName) > self.__maxLength:
            cleanedPreferredName = utils.cleanStr(cleanedPreferredName[:self.__maxLength])

        if not utils.isValidStr(cleanedPreferredName):
            return None

        return cleanedPreferredName
