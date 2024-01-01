from typing import Dict, List, Optional

import CynanBot.misc.utils as utils
from CynanBot.aniv.anivContentCode import AnivContentCode
from CynanBot.aniv.anivContentScannerInterface import \
    AnivContentScannerInterface
from CynanBot.contentScanner.contentCode import ContentCode
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.misc.stack import Stack
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
        self.__quotes: Dict[str, Optional[str]] = self.__createQuotesDict()

    async def __checkParens(self, message: str) -> AnivContentCode:
        if not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        stack: Stack[str] = Stack()
        encounteredError = False

        try:
            for character in message:
                if character in self.__parens.keys():
                    stack.push(character)
                elif character in self.__parens.values():
                    startCharacter: Optional[str] = None

                    for start, end in self.__parens.items():
                        if end == character:
                            startCharacter = start
                            break

                    if not isinstance(startCharacter, str):
                        raise RuntimeError(f'Unable to find corresponding start character for end character \"{character}\"')
                    elif stack.top() != startCharacter:
                        encounteredError = True
                        break

                    stack.pop()
        except IndexError:
            encounteredError = True

        if encounteredError:
            self.__timber.log('AnivContentScanner', f'Discovered open parens within aniv message ({message=}) ({stack=})')
            return AnivContentCode.OPEN_PAREN
        else:
            return AnivContentCode.OK

    async def __checkQuotes(self, message: str) -> AnivContentCode:
        if not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        for start, end in self.__quotes.items():
            stack = 0

            for character in message:
                if character == start:
                    if end is None and (stack % 2) != 0:
                        stack -= 1
                    else:
                        stack += 1
                elif character == end:
                    stack -= 1

            if stack != 0:
                self.__timber.log('AnivContentScanner', f'Discovered open quotes within aniv message ({message=}) ({stack=})')
                return AnivContentCode.OPEN_QUOTES

        return AnivContentCode.OK

    def __createParensDict(self) -> Dict[str, str]:
        return {
            '[': ']',
            '(': ')',
            '{': '}'
        }

    def __createQuotesDict(self) -> Dict[str, Optional[str]]:
        return {
            '\"': None,
            '“': '”'
        }

    async def __deepScan(self, message: str) -> AnivContentCode:
        if not utils.isValidStr(message):
            raise ValueError(f'message argument is malformed: \"{message}\"')

        parensContentCode = await self.__checkParens(message)
        if parensContentCode is not AnivContentCode.OK:
            return parensContentCode

        quotesContentCode = await self.__checkQuotes(message)
        if quotesContentCode is not AnivContentCode.OK:
            return quotesContentCode

        return AnivContentCode.OK

    async def scan(self, message: Optional[str]) -> AnivContentCode:
        if not utils.isValidStr(message):
            return AnivContentCode.IS_NONE_OR_EMPTY_OR_BLANK

        contentCode = await self.__contentScanner.scan(message)

        if contentCode is ContentCode.CONTAINS_BANNED_CONTENT:
            return AnivContentCode.CONTAINS_BANNED_CONTENT
        elif contentCode is ContentCode.CONTAINS_URL:
            return AnivContentCode.CONTAINS_URL
        elif contentCode is ContentCode.IS_NONE or contentCode is ContentCode.IS_EMPTY or contentCode is ContentCode.IS_BLANK:
            return AnivContentCode.IS_NONE_OR_EMPTY_OR_BLANK
        elif contentCode is not ContentCode.OK:
            # This case is actually a programmatic error of some kind, it means that we're not
            # properly mapping together ContentCode values and AnivContentCode values.
            self.__timber.log('AnivContentScanner', f'Message from aniv returned a ContentCode that we\'re not properly supporting ({contentCode=}) ({message=})')
            return AnivContentCode.CONTAINS_BANNED_CONTENT
        else:
            return await self.__deepScan(message)
