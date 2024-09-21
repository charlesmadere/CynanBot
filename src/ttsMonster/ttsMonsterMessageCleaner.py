import re
from typing import Any, Pattern

from ..misc import utils as utils


class TtsMonsterMessageCleaner:

    def __init__(self):
        self.__extraWhiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.removeCheerStrings(message.strip()).strip()
        message = self.__extraWhiteSpaceRegEx.sub(' ', message.strip()).strip()

        return message
