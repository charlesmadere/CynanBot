import re
import traceback
from typing import Any, Collection, Final, Pattern

from frozenlist import FrozenList

from .decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from ..emojiHelper.emojiHelperInterface import EmojiHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..tts.settings.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ..twitch.twitchMessageStringUtilsInterface import TwitchMessageStringUtilsInterface


class DecTalkMessageCleaner(DecTalkMessageCleanerInterface):

    def __init__(
        self,
        emojiHelper: EmojiHelperInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        twitchMessageStringUtils: TwitchMessageStringUtilsInterface,
        isUnrestricted: bool = False
    ):
        if not isinstance(emojiHelper, EmojiHelperInterface):
            raise TypeError(f'emojiHelper argument is malformed: \"{emojiHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(twitchMessageStringUtils, TwitchMessageStringUtilsInterface):
            raise TypeError(f'twitchMessageStringUtils argument is malformed: \"{twitchMessageStringUtils}\"')
        elif not isinstance(isUnrestricted, bool):
            raise TypeError(f'isUnrestricted argument is malformed: \"{isUnrestricted}\"')

        self.__emojiHelper: Final[EmojiHelperInterface] = emojiHelper
        self.__timber: Final[TimberInterface] = timber
        self.__ttsSettingsRepository: Final[TtsSettingsRepositoryInterface] = ttsSettingsRepository
        self.__twitchMessageStringUtils: Final[TwitchMessageStringUtilsInterface] = twitchMessageStringUtils
        self.__isUnrestricted: Final[bool] = isUnrestricted

        self.__decTalkInlineCommandRegExes: Collection[Pattern] = self.__buildDecTalkInlineCommandRegExes()
        self.__decTalkInputFlagRegExes: Collection[Pattern] = self.__buildDecTalkInputFlagRegExes()
        self.__terminalExploitRegExes: Collection[Pattern] = self.__buildTerminalExploitRegExes()
        self.__decTalkIllegalCharactersRegEx: Pattern = re.compile(r'[\[\]]', re.IGNORECASE)
        self.__extraWhiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

    def __buildDecTalkInlineCommandRegExes(self) -> FrozenList[Pattern]:
        regExes: FrozenList[Pattern] = FrozenList()

        # purge comma pause inline command
        regExes.append(re.compile(r'\[\s*:\s*(comm|cp).*?]', re.IGNORECASE))

        # purge dial inline command
        regExes.append(re.compile(r'\[\s*:\s*dial.*?]', re.IGNORECASE))

        # purge design voice inline command
        regExes.append(re.compile(r'\[\s*:\s*dv.*?]', re.IGNORECASE))

        # purge error inline command
        regExes.append(re.compile(r'\[\s*:\s*err.*?]', re.IGNORECASE))

        # purge log inline command
        regExes.append(re.compile(r'\[\s*:\s*log.*?]', re.IGNORECASE))

        # purge sync mode inline command
        regExes.append(re.compile(r'\[\s*:\s*mode.*?]', re.IGNORECASE))

        # purge period pause inline command
        regExes.append(re.compile(r'\[\s*:\s*(peri|pp).*?]', re.IGNORECASE))

        # purge phoneme inline command
        regExes.append(re.compile(r'\[\s*:\s*phoneme.*?]', re.IGNORECASE))

        # purge pitch inline command
        regExes.append(re.compile(r'\[\s*:\s*pitch.*?]', re.IGNORECASE))

        # purge play inline command
        regExes.append(re.compile(r'\[\s*:\s*play.*?]', re.IGNORECASE))

        # purge rate inline command
        regExes.append(re.compile(r'\[\s*:\s*rate.*?]', re.IGNORECASE))

        # purge sync inline command
        regExes.append(re.compile(r'\[\s*:\s*sync.*?]', re.IGNORECASE))

        # purge tone inline command
        regExes.append(re.compile(r'\[\s*\w*\<\d+,\d+\>.*?]', re.IGNORECASE))

        # purge tone inline command
        regExes.append(re.compile(r'\[\s*:\s*t.*?]', re.IGNORECASE))

        # purge voice inline command
        regExes.append(re.compile(r'\[\s*:n\w+.*?]', re.IGNORECASE))

        # purge volume inline command
        regExes.append(re.compile(r'\[\s*:\s*vol.*?]', re.IGNORECASE))

        regExes.freeze()
        return regExes

    def __buildDecTalkInputFlagRegExes(self) -> Collection[Pattern]:
        regExes: FrozenList[Pattern] = FrozenList()

        # purge various help flags
        regExes.append(re.compile(r'(^|\s+)-h', re.IGNORECASE))
        regExes.append(re.compile(r'(^|\s+)-\?', re.IGNORECASE))

        # purge pre input flag
        regExes.append(re.compile(r'(^|\s+)-pre', re.IGNORECASE))

        # purge post input flag
        regExes.append(re.compile(r'(^|\s+)-post', re.IGNORECASE))

        # purge text flag
        regExes.append(re.compile(r'^\s*text', re.IGNORECASE))

        # purge user dictionary flag
        regExes.append(re.compile(r'(^|\s+)-d', re.IGNORECASE))

        # purge version information flag
        regExes.append(re.compile(r'(^|\s+)-v', re.IGNORECASE))

        # purge language flag
        regExes.append(re.compile(r'(^|\s+)-lang(\s+\w+)?', re.IGNORECASE))

        # purge various output flags
        regExes.append(re.compile(r'(^|\s+)-w', re.IGNORECASE))
        regExes.append(re.compile(r'(^|\s+)-l((\[\w+])|\w+)?', re.IGNORECASE))

        regExes.freeze()
        return regExes

    def __buildTerminalExploitRegExes(self) -> Collection[Pattern]:
        regExes: FrozenList[Pattern] = FrozenList()

        # purge potentially dangerous/tricky characters
        regExes.append(re.compile(r'[<>&%;=\"|^~`\\]', re.IGNORECASE))

        # purge what might be directory traversal sequences
        regExes.append(re.compile(r'\.{2}', re.IGNORECASE))

        regExes.freeze()
        return regExes

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.cleanStr(message)
        message = await self.__twitchMessageStringUtils.removeCheerStrings(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__purge(self.__decTalkInputFlagRegExes, message)
        if not utils.isValidStr(message):
            return None

        if not self.__isUnrestricted:
            message = await self.__purge(self.__decTalkInlineCommandRegExes, message)
            if not utils.isValidStr(message):
                return None

            message = await self.__purge(self.__terminalExploitRegExes, message)
            if not utils.isValidStr(message):
                return None

            message = self.__decTalkIllegalCharactersRegEx.sub(' ', message).strip()
            if not utils.isValidStr(message):
                return None

        message = await self.__emojiHelper.replaceEmojisWithHumanNames(message)
        message = self.__extraWhiteSpaceRegEx.sub(' ', message).strip()

        maximumMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()
        if len(message) > maximumMessageSize:
            message = message[0:maximumMessageSize].strip()

        if not utils.isValidStr(message):
            return None

        try:
            # DECTalk requires Windows-1252 encoding
            message = message.encode().decode('windows-1252')
        except Exception as e:
            self.__timber.log('DecTalkMessageCleaner', f'Encountered an error when attempting to re-encode message for DECTalk ({message=}): {e}', e, traceback.format_exc())
            return None

        return message

    async def __purge(
        self,
        regExes: Collection[Pattern],
        message: str | None
    ) -> str | None:
        if not utils.isValidStr(message):
            return None

        repeat = True

        while repeat:
            repeat = False

            for regEx in regExes:
                if regEx.search(message) is None:
                    continue

                repeat = True
                message = regEx.sub(' ', message).strip()

                if not utils.isValidStr(message):
                    return None

        if not utils.isValidStr(message):
            return None

        return message.strip()
