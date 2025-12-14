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

    async def clean(self, name: str | Any | None) -> str | None:
        if not isinstance(name, str):
            return None
        elif not utils.isValidStr(name):
            return None

        name = utils.cleanStr(name).strip()
        name = self.__invalidCharactersRegEx.sub('', name).strip()
        name = utils.cleanStr(name).strip()

        if len(name) > self.__maxLength:
            name = name[:self.__maxLength].strip()

        if utils.isValidStr(name):
            return name
        else:
            return None
