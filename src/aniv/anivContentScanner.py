import re
from re import Match
from typing import Pattern

from .anivContentCode import AnivContentCode
from .anivContentScannerInterface import AnivContentScannerInterface
from ..contentScanner.contentCode import ContentCode
from ..contentScanner.contentScannerInterface import ContentScannerInterface
from ..misc import utils as utils
from ..misc.stack import Stack
from ..timber.timberInterface import TimberInterface


class AnivContentScanner(AnivContentScannerInterface):

    def __init__(
        self,
        contentScanner: ContentScannerInterface,
        timber: TimberInterface
    ):
        if not isinstance(contentScanner, ContentScannerInterface):
            raise TypeError(f'contentScanner argument is malformed: \"{contentScanner}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__contentScanner: ContentScannerInterface = contentScanner
        self.__timber: TimberInterface = timber

        self.__parens: dict[str, str] = {
            '[': ']',
            '(': ')',
            '{': '}'
        }

        self.__quotes: dict[str, str] = {
            '“': '”',
            '「': '」'
        }

        self.__twitchEmojiPatterns: list[Pattern] = [
            re.compile(r'^[BR:;]-?[\)]$'),
            re.compile(r'^[:>]\($'),
            re.compile(r'^<3$')
        ]

    async def __cleanTwitchEmojisFromString(self, message: str) -> str:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        splits = utils.getCleanedSplits(message)
        indexesToBlank: list[int] = list()

        for index, split in enumerate(splits):
            emojiMatch: Match | None = None

            for emojiPattern in self.__twitchEmojiPatterns:
                emojiMatch = emojiPattern.fullmatch(split)

                if emojiMatch is not None:
                    break

            if emojiMatch is not None:
                indexesToBlank.append(index)

        if len(indexesToBlank) == 0:
            return message

        for indexToBlank in indexesToBlank:
            splits[indexToBlank] = ''

        return ' '.join(splits).strip()

    async def __containsMatchingCharacterPairs(
        self,
        characterPairs: dict[str, str],
        message: str
    ) -> bool:
        if not isinstance(characterPairs, dict):
            raise TypeError(f'characterPairs argument is malformed: \"{characterPairs}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        stack: Stack[str] = Stack()
        keys: set[str] = set(characterPairs.keys())
        values: set[str] = set(characterPairs.values())
        items: list[tuple[str, str]] = list(characterPairs.items())

        try:
            for character in message:
                if character in keys:
                    stack.push(character)
                elif character in values:
                    startCharacter: str | None = None

                    for start, end in items:
                        if end == character:
                            startCharacter = start
                            break

                    if not isinstance(startCharacter, str):
                        raise RuntimeError(f'Unable to find corresponding start character for end character \"{character}\"')
                    elif stack.top() == startCharacter:
                        stack.pop()
                    else:
                        self.__timber.log('AnivContentScanner', f'Discovered mismatching character pairs within aniv message ({message=}) ({stack=})')
                        return False
        except IndexError:
            return False

        if len(stack) == 0:
            return True
        else:
            self.__timber.log('AnivContentScanner', f'Discovered mismatching character pairs within aniv message ({message=}) ({stack=})')
            return False

    async def __containsMatchingStraightQuotes(self, message: str) -> bool:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        count = message.count('\"')

        if count % 2 == 0:
            return True
        else:
            self.__timber.log('AnivContentScanner', f'Discovered mismatching straight quotes within aniv message ({message=}) ({count=})')
            return False

    async def __deepScan(self, message: str) -> AnivContentCode:
        if not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')

        emojiCleanedMessage = await self.__cleanTwitchEmojisFromString(message)

        if not utils.isValidStr(emojiCleanedMessage):
            # This case means that the message was only basic Twitch emojis, and after those were
            # removed from the string, the message is now blank. So let's consider this message OK.
            return AnivContentCode.OK

        if not await self.__containsMatchingCharacterPairs(
            characterPairs = self.__parens,
            message = emojiCleanedMessage
        ):
            return AnivContentCode.OPEN_PAREN

        if not await self.__containsMatchingCharacterPairs(
            characterPairs = self.__quotes,
            message = message
        ):
            return AnivContentCode.OPEN_QUOTES

        if not await self.__containsMatchingStraightQuotes(
            message = message
        ):
            return AnivContentCode.OPEN_QUOTES

        return AnivContentCode.OK

    async def scan(self, message: str | None) -> AnivContentCode:
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
            # perform aniv-specific additional message scanning
            return await self.__deepScan(message)
