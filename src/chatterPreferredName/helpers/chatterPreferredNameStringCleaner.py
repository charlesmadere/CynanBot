import re
from typing import Any, Final, Pattern

from ...misc import utils as utils


class ChatterPreferredNameStringCleaner:

    def __init__(
        self,
        maxLength: int = 24,
    ):
        if not utils.isValidInt(maxLength):
            raise TypeError(f'maxLength argument is malformed: \"{maxLength}\"')
        elif maxLength < 8 or maxLength > 128:
            raise ValueError(f'maxLength argument is out of bounds: {maxLength}')

        self.__maxLength: Final[int] = maxLength

        self.__invalidCharactersRegEx: Final[Pattern] = re.compile(r'[^\w\s]', re.IGNORECASE)
        self.__spaceReplacementCharactersRegEx: Final[Pattern] = re.compile(r'[_-]', re.IGNORECASE)

    async def clean(self, name: str | Any | None) -> str | None:
        if not isinstance(name, str):
            return None

        name = utils.cleanStr(name)
        name = self.__spaceReplacementCharactersRegEx.sub(' ', name).strip()
        name = self.__invalidCharactersRegEx.sub('', name).strip()
        name = utils.cleanStr(name)

        if len(name) > self.__maxLength:
            name = utils.cleanStr(name[:self.__maxLength])

        if utils.isValidStr(name):
            return name
        else:
            return None
