from typing import Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.contentScanner.aniv.anivContentCode import AnivContentCode
from CynanBot.contentScanner.aniv.anivContentScannerInterface import \
    AnivContentScannerInterface
from CynanBot.contentScanner.contentCode import ContentCode
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.timber.timberInterface import TimberInterface


class AnivContentScanner(AnivContentScannerInterface):

    def __init__(
        self,
        contentScanner: ContentScannerInterface,
        timber: TimberInterface
    ):
        if not isinstance(contentScanner, ContentScannerInterface):
            raise ValueError(f'contentScanner argument is malformed: \"{contentScanner}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__contentScanner: ContentScannerInterface = contentScanner
        self.__timber: TimberInterface = timber
        self.__parens: Dict[str, str] = self.__createParensDict()
        self.__quotes: Dict[str, str] = self.__createQuotesDict()

    def __createParensDict(self) -> Dict[str, str]:
        return {
            '[': ']',
            '(': ')',
            '{': '}'
        }

    def __createQuotesDict(self) -> Dict[str, str]:
        return {
            '\"': '\"',
            '“': '”'
        }

    async def __deepScan(self, message: str) -> AnivContentCode:
        if not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        for startParen, endParen in self.__parens.items():
            occurences = 0

            for character in message:
                if character == startParen:
                    occurences += 1
                elif character == endParen:
                    occurences -= 1

            if occurences != 0:
                self.__timber.log('AnivContentScanner', f'Discovered open parens within aniv message ({message=}) ({occurences=})')
                return AnivContentCode.OPEN_PAREN

        for startQuote, endQuote in self.__quotes.items():
            occurences = 0

            for character in message:
                if character == startQuote:
                    occurences += 1
                elif character == endQuote:
                    occurences -= 1

            if occurences != 0:
                self.__timber.log('AnivContentScanner', f'Discovered open quotes within aniv message ({message=}) ({occurences=})')
                return AnivContentCode.OPEN_QUOTES

        return AnivContentCode.OK

    async def scan(self, message: Optional[str]) -> AnivContentCode:
        if not utils.isValidStr(message):
            return AnivContentCode.IS_NONE_OR_EMPTY_BLANK

        contentCode = await self.__contentScanner.scan(message)

        if contentCode is ContentCode.CONTAINS_BANNED_CONTENT:
            return AnivContentCode.CONTAINS_BANNED_CONTENT
        elif contentCode is ContentCode.CONTAINS_URL:
            return AnivContentCode.CONTAINS_URL
        elif contentCode is ContentCode.IS_NONE or contentCode is ContentCode.IS_EMPTY or contentCode is ContentCode.IS_BLANK:
            return AnivContentCode.IS_NONE_OR_EMPTY_BLANK
        elif contentCode is not ContentCode.OK:
            # this case is actually an error, it means that we're not properly mapping together
            # ContentCode values and AnivContentCode values
            self.__timber.log('AnivContentScanner', f'Message from aniv returned a ContentCode that we\'re not properly supporting ({contentCode=}) ({message=})')
            return AnivContentCode.CONTAINS_BANNED_CONTENT
        else:
            return await self.__deepScan(message)
