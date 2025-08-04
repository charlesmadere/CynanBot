import re
from typing import Final, Pattern

from .supStreamerHelperInterface import SupStreamerHelperInterface
from ..misc import utils as utils


class SupStreamerHelper(SupStreamerHelperInterface):

    def __init__(self):
        self.__supStreamerRegEx: Final[Pattern] = re.compile(r'[^[:alnum:]]', re.IGNORECASE)

    async def isSupStreamerMessage(
        self,
        chatMessage: str | None,
        supStreamerMessage: str,
    ) -> bool:
        if chatMessage is not None and not isinstance(chatMessage, str):
            raise TypeError(f'chatMessage argument is malformed: \"{chatMessage}\"')
        elif not utils.isValidStr(supStreamerMessage):
            raise TypeError(f'supStreamerMessage argument is malformed: \"{supStreamerMessage}\"')

        chatMessage = utils.cleanStr(chatMessage)
        if not utils.isValidStr(chatMessage):
            return False

        # take these incoming message strings and replace every non-alphanumeric character with ' '
        chatMessage = self.__supStreamerRegEx.sub(' ', chatMessage).strip().casefold()
        supStreamerMessage = self.__supStreamerRegEx.sub(' ', supStreamerMessage).strip().casefold()

        if chatMessage == supStreamerMessage:
            return True

        supStreamerVariants: set[str] = {
            f'{supStreamerMessage} ',
            f' {supStreamerMessage}',
            f' {supStreamerMessage} '
        }

        for variant in supStreamerVariants:
            if variant in chatMessage:
                return True

        return False
