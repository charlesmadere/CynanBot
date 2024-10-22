import re
import traceback
from typing import Any, Collection, Pattern

from frozenlist import FrozenList

from .decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from ..emojiHelper.emojiHelperInterface import EmojiHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class DecTalkMessageCleaner(DecTalkMessageCleanerInterface):

    def __init__(
        self,
        emojiHelper: EmojiHelperInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(emojiHelper, EmojiHelperInterface):
            raise TypeError(f'emojiHelper argument is malformed: \"{emojiHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__emojiHelper: EmojiHelperInterface = emojiHelper
        self.__timber: TimberInterface = timber
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__inlineCommandRegExes: Collection[Pattern] = self.__buildInlineCommandRegExes()
        self.__inputFlagRegExes: Collection[Pattern] = self.__buildInputFlagRegExes()
        self.__inputToneRegExes: Collection[Pattern] = self.__buildInputToneRegExes()
        self.__extraWhiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

    def __buildInlineCommandRegExes(self) -> FrozenList[Pattern]:
        inlineCommandRegExes: FrozenList[Pattern] = FrozenList()

        # purge comma pause inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*(comm|cp).*?]', re.IGNORECASE))

        # purge dial inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*dial.*?]', re.IGNORECASE))

        # purge design voice inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*dv.*?]', re.IGNORECASE))

        # purge error inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*err.*?]', re.IGNORECASE))

        # purge log inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*log.*?]', re.IGNORECASE))

        # purge sync mode inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*mode.*?]', re.IGNORECASE))

        # purge period pause inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*(peri|pp).*?]', re.IGNORECASE))

        # purge phoneme inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*phoneme.*?]', re.IGNORECASE))

        # purge pitch inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*pitch.*?]', re.IGNORECASE))

        # purge play inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*play.*?]', re.IGNORECASE))

        # purge rate inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*rate.*?]', re.IGNORECASE))

        # purge sync inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*sync.*?]', re.IGNORECASE))

        # purge tone inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*t.*?]', re.IGNORECASE))

        # purge volume inline command
        inlineCommandRegExes.append(re.compile(r'\[\s*:\s*vol.*?]', re.IGNORECASE))

        inlineCommandRegExes.freeze()
        return inlineCommandRegExes

    def __buildInputFlagRegExes(self) -> Collection[Pattern]:
        inputFlagRegExes: FrozenList[Pattern] = FrozenList()

        # purge potentially dangerous/tricky characters
        inputFlagRegExes.append(re.compile(r'[&%;=\'\"|^~]', re.IGNORECASE))

        # purge what might be directory traversal sequences
        inputFlagRegExes.append(re.compile(r'\.{2}', re.IGNORECASE))

        # purge various help flags
        inputFlagRegExes.append(re.compile(r'(^|\s+)-h', re.IGNORECASE))
        inputFlagRegExes.append(re.compile(r'(^|\s+)-\?', re.IGNORECASE))

        # purge various input flags
        inputFlagRegExes.append(re.compile(r'(^|\s+)-pre', re.IGNORECASE))
        inputFlagRegExes.append(re.compile(r'(^|\s+)-post', re.IGNORECASE))
        inputFlagRegExes.append(re.compile(r'^\s*text', re.IGNORECASE))

        # purge user dictionary flag
        inputFlagRegExes.append(re.compile(r'(^|\s+)-d', re.IGNORECASE))

        # purge version information flag
        inputFlagRegExes.append(re.compile(r'(^|\s+)-v', re.IGNORECASE))

        # purge language flag
        inputFlagRegExes.append(re.compile(r'(^|\s+)-lang(\s+\w+)?', re.IGNORECASE))

        # purge various output flags
        inputFlagRegExes.append(re.compile(r'(^|\s+)-w', re.IGNORECASE))
        inputFlagRegExes.append(re.compile(r'(^|\s+)-l((\[\w+])|\w+)?', re.IGNORECASE))

        inputFlagRegExes.freeze()
        return inputFlagRegExes

    def __buildInputToneRegExes(self) -> Collection[Pattern]:
        inputToneRegExes: FrozenList[Pattern] = FrozenList()

        # purge tone constructs
        inputToneRegExes.append(re.compile(r'\[\s*\w*\<\d+,\d+\>.*?]', re.IGNORECASE))

        inputToneRegExes.freeze()
        return inputToneRegExes

    async def clean(self, message: str | Any | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.removeCheerStrings(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__purgeInputFlags(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__purgeInlineCommands(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__purgeInputTones(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__emojiHelper.replaceEmojisWithHumanNames(message)
        message = self.__extraWhiteSpaceRegEx.sub(' ', message).strip()

        maximumMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()
        if len(message) > maximumMessageSize:
            message = message[0:maximumMessageSize].strip()

        try:
            # DECTalk requires Windows-1252 encoding
            message = message.encode().decode('windows-1252')
        except Exception as e:
            self.__timber.log('DecTalkMessageCleaner', f'Encountered an error when attempting to re-encode message for DECTalk ({message=}): {e}', e, traceback.format_exc())
            return None

        return message

    async def __purgeInlineCommands(self, message: str | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        repeat = True

        while repeat:
            repeat = False

            for inlineCommandRegEx in self.__inlineCommandRegExes:
                if inlineCommandRegEx.search(message) is None:
                    continue

                repeat = True
                message = inlineCommandRegEx.sub(' ', message).strip()

                if not utils.isValidStr(message):
                    return None

        if not utils.isValidStr(message):
            return None

        return message.strip()

    async def __purgeInputFlags(self, message: str | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        repeat = True

        while repeat:
            repeat = False

            for inputFlagRegEx in self.__inputFlagRegExes:
                if inputFlagRegEx.search(message) is None:
                    continue

                repeat = True
                message = inputFlagRegEx.sub(' ', message).strip()

                if not utils.isValidStr(message):
                    return None

        if not utils.isValidStr(message):
            return None

        return message.strip()

    async def __purgeInputTones(self, message: str | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        repeat = True

        while repeat:
            repeat = False

            for inputToneRegEx in self.__inputToneRegExes:
                if inputToneRegEx.search(message) is None:
                    continue

                repeat = True
                message = inputToneRegEx.sub(' ', message).strip()

                if not utils.isValidStr(message):
                    return None

        if not utils.isValidStr(message):
            return None

        return message.strip()
