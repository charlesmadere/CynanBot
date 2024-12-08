import re
from typing import Pattern

from .supStreamerHelperInterface import SupStreamerHelperInterface
from ..misc import utils as utils


class SupStreamerHelper(SupStreamerHelperInterface):

    def __init__(self):
        self.__supStreamerRegEx: Pattern = re.compile(r'[^[:alnum:]]', re.IGNORECASE)

    async def isSupStreamerMessage(
        self,
        chatMessage: str | None,
        supStreamerMessage: str
    ) -> bool:
        if chatMessage is not None and not isinstance(chatMessage, str):
            raise TypeError(f'chatMessage argument is malformed: \"{chatMessage}\"')
        elif not utils.isValidStr(supStreamerMessage):
            raise TypeError(f'supStreamerMessage argument is malformed: \"{supStreamerMessage}\"')

        if not utils.isValidStr(chatMessage):
            return False

        cleanedChatMessage = self.__supStreamerRegEx.sub(' ', chatMessage)
        return supStreamerMessage.casefold() in cleanedChatMessage.casefold()
