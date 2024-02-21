import re
from typing import List, Optional, Pattern

import CynanBot.misc.utils as utils
from CynanBot.contentScanner.contentCode import ContentCode
from CynanBot.contentScanner.contentScannerInterface import \
    ContentScannerInterface
from CynanBot.emojiHelper.emojiHelperInterface import EmojiHelperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.tts.ttsCheerDonation import TtsCheerDonation
from CynanBot.tts.ttsCommandBuilderInterface import TtsCommandBuilderInterface
from CynanBot.tts.ttsDonation import TtsDonation
from CynanBot.tts.ttsDonationType import TtsDonationType
from CynanBot.tts.ttsEvent import TtsEvent
from CynanBot.tts.ttsSettingsRepositoryInterface import \
    TtsSettingsRepositoryInterface
from CynanBot.tts.ttsSubscriptionDonation import TtsSubscriptionDonation
from CynanBot.tts.ttsSubscriptionDonationGiftType import \
    TtsSubscriptionDonationGiftType


class DecTalkCommandBuilder(TtsCommandBuilderInterface):

    def __init__(
        self,
        contentScanner: ContentScannerInterface,
        emojiHelper: EmojiHelperInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        assert isinstance(contentScanner, ContentScannerInterface), f"malformed {contentScanner=}"
        assert isinstance(emojiHelper, EmojiHelperInterface), f"malformed {emojiHelper=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface), f"malformed {ttsSettingsRepository=}"

        self.__contentScanner: ContentScannerInterface = contentScanner
        self.__emojiHelper: EmojiHelperInterface = emojiHelper
        self.__timber: TimberInterface = timber
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__cheerRegExes: List[Pattern] = self.__buildCheerStrings()
        self.__inlineCommandRegExes: List[Pattern] = self.__buildInlineCommandStrings()
        self.__inputFlagRegExes: List[Pattern] = self.__buildInputFlagStrings()
        self.__whiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

    async def buildAndCleanEvent(self, event: Optional[TtsEvent]) -> Optional[str]:
        assert event is None or isinstance(event, TtsEvent), f"malformed {event=}"

        if event is None:
            return None

        prefix = await self.__processDonationPrefix(event)
        message = event.getMessage()

        if utils.isValidStr(message):
            message = await self.buildAndCleanMessage(message)

        if utils.isValidStr(prefix) and utils.isValidStr(message):
            return f'{prefix} {message}'
        elif utils.isValidStr(prefix):
            return prefix
        elif utils.isValidStr(message):
            return message
        else:
            return None

    async def buildAndCleanMessage(self, message: Optional[str]) -> Optional[str]:
        if not utils.isValidStr(message):
            return None

        contentCode = await self.__contentScanner.scan(message)
        if contentCode is not ContentCode.OK:
            self.__timber.log('DecTalkCommandBuilder', f'TTS command \"{message}\" returned a bad content code: \"{contentCode}\"')
            return None

        message = await self.__purgeInputFlags(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__purgeCheers(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__purgeInlineCommands(message)
        if not utils.isValidStr(message):
            return None

        message = await self.__emojiHelper.replaceEmojisWithHumanNames(message)

        # remove extranneous whitespace
        message = self.__whiteSpaceRegEx.sub(' ', message)
        message = message.strip()

        if not utils.isValidStr(message):
            return None

        message = await self.__cropMessageIfNecessary(message)
        if not utils.isValidStr(message):
            return None

        # DECTalk requires Windows-1252 encoding
        return message.encode().decode('windows-1252')

    def __buildCheerStrings(self) -> List[Pattern]:
        cheerStrings: List[Pattern] = list()

        # purge "cheer100"
        cheerStrings.append(re.compile(r'(^|\s+)cheer\d+(\s+|$)', re.IGNORECASE))

        # purge "uni100"
        cheerStrings.append(re.compile(r'(^|\s+)uni\d+(\s+|$)', re.IGNORECASE))

        return cheerStrings

    def __buildInlineCommandStrings(self) -> List[Pattern]:
        inlineCommandStrings: List[Pattern] = list()

        # purge comma pause inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*(comm|cp).*?\]', re.IGNORECASE))

        # purge dial inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*dial.*?\]', re.IGNORECASE))

        # purge design voice inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*dv.*?\]', re.IGNORECASE))

        # purge error inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*err.*?\]', re.IGNORECASE))

        # purge log inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*log.*?\]', re.IGNORECASE))

        # purge sync mode inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*mode.*?\]', re.IGNORECASE))

        # purge period pause inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*(peri|pp).*?\]', re.IGNORECASE))

        # purge pitch inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*pitch.*?\]', re.IGNORECASE))

        # purge play inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*play.*?\]', re.IGNORECASE))

        # purge rate inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*rate.*?\]', re.IGNORECASE))

        # purge sync inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*sync.*?\]', re.IGNORECASE))

        # purge tone inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*t.*?\]', re.IGNORECASE))

        # purge volume inline command
        inlineCommandStrings.append(re.compile(r'\[\s*\:\s*vol.*?\]', re.IGNORECASE))

        return inlineCommandStrings

    def __buildInputFlagStrings(self) -> List[Pattern]:
        inputFlagStrings: List[Pattern] = list()

        # purge potentially dangerous/tricky characters
        inputFlagStrings.append(re.compile(r'\&|\%|\;|\=|\'|\"|\||\^|\~', re.IGNORECASE))

        # purge what might be directory traversal sequences
        inputFlagStrings.append(re.compile(r'\.{2}', re.IGNORECASE))

        # purge various help flags
        inputFlagStrings.append(re.compile(r'(^|\s+)-h', re.IGNORECASE))
        inputFlagStrings.append(re.compile(r'(^|\s+)-\?', re.IGNORECASE))

        # purge various input flags
        inputFlagStrings.append(re.compile(r'(^|\s+)-pre', re.IGNORECASE))
        inputFlagStrings.append(re.compile(r'(^|\s+)-post', re.IGNORECASE))
        inputFlagStrings.append(re.compile(r'^\s*text', re.IGNORECASE))

        # purge user dictionary flag
        inputFlagStrings.append(re.compile(r'(^|\s+)-d', re.IGNORECASE))

        # purge version information flag
        inputFlagStrings.append(re.compile(r'(^|\s+)-v', re.IGNORECASE))

        # purge language flag
        inputFlagStrings.append(re.compile(r'(^|\s+)-lang(\s+\w+)?', re.IGNORECASE))

        # purge various output flags
        inputFlagStrings.append(re.compile(r'(^|\s+)-w', re.IGNORECASE))
        inputFlagStrings.append(re.compile(r'(^|\s+)-l((\[\w+\])|\w+)?', re.IGNORECASE))

        return inputFlagStrings

    async def __cropMessageIfNecessary(self, message: Optional[str]) -> Optional[str]:
        if not utils.isValidStr(message):
            return None

        maxMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()

        if len(message) > maxMessageSize:
            self.__timber.log('DecTalkCommandBuilder', f'Chopping down TTS command \"{message}\" as it is too long (len={len(message)}) ({maxMessageSize=}) ({message})')
            message = message[:maxMessageSize].strip()

        if not utils.isValidStr(message):
            return None

        return message

    async def __processCheerDonationPrefix(
        self,
        event: TtsEvent,
        donation: TtsCheerDonation
    ) -> Optional[str]:
        assert isinstance(event, TtsEvent), f"malformed {event=}"
        assert isinstance(donation, TtsCheerDonation), f"malformed {donation=}"
        if donation.getType() is not TtsDonationType.CHEER:
            raise TypeError(f'TtsDonationType is not {TtsDonationType.CHEER}: \"{donation.getType()}\" ({donation=})')

        return f'{event.getUserName()} cheered {donation.getBits()}!'

    async def __processDonationPrefix(self, event: TtsEvent) -> Optional[str]:
        assert isinstance(event, TtsEvent), f"malformed {event=}"

        donation: Optional[TtsDonation] = event.getDonation()

        if donation is None:
            return None

        donationType = donation.getType()

        if donationType is TtsDonationType.CHEER:
            return await self.__processCheerDonationPrefix(
                event = event,
                donation = donation
            )
        elif donationType is TtsDonationType.SUBSCRIPTION:
            return await self.__processSubcriptionDonationPrefix(
                event = event,
                donation = donation
            )
        else:
            raise RuntimeError(f'donationType is unknown: \"{donationType}\"')

    async def __processSubcriptionDonationPrefix(
        self,
        event: TtsEvent,
        donation: TtsSubscriptionDonation
    ) -> str:
        assert isinstance(event, TtsEvent), f"malformed {event=}"
        assert isinstance(donation, TtsSubscriptionDonation), f"malformed {donation=}"
        if donation.getType() is not TtsDonationType.SUBSCRIPTION:
            raise TypeError(f'TtsDonationType is not {TtsDonationType.SUBSCRIPTION}: \"{donation.getType()}\" ({donation=})')

        # I don't think it makes sense for a subscription to be anonymous, and also not a gift?

        if donation.getGiftType() is TtsSubscriptionDonationGiftType.GIVER:
            if donation.isAnonymous():
                return f'anonymous gifted a sub!'
            else:
                return f'{event.getUserName()} gifted a sub!'
        elif donation.getGiftType() is TtsSubscriptionDonationGiftType.RECEIVER:
            return f'{event.getUserName()} received a sub gift!'
        else:
            return f'{event.getUserName()} subscribed!'

    async def __purgeCheers(self, message: Optional[str]) -> Optional[str]:
        if not utils.isValidStr(message):
            return None

        for cheerRegEx in self.__cheerRegExes:
            message = cheerRegEx.sub(' ', message)

            if not utils.isValidStr(message):
                return None

        if not utils.isValidStr(message):
            return None

        return message.strip()

    async def __purgeInlineCommands(self, message: Optional[str]) -> Optional[str]:
        if not utils.isValidStr(message):
            return None

        repeat = True

        while repeat:
            if repeat:
                repeat = False

            for inlineCommandRegEx in self.__inlineCommandRegExes:
                if inlineCommandRegEx.search(message) is None:
                    continue

                repeat = True
                message = inlineCommandRegEx.sub(' ', message)

                if not utils.isValidStr(message):
                    return None

        if not utils.isValidStr(message):
            return None

        return message.strip()

    async def __purgeInputFlags(self, message: Optional[str]) -> Optional[str]:
        if not utils.isValidStr(message):
            return None

        repeat = True

        while repeat:
            if repeat:
                repeat = False

            for inputFlagRegEx in self.__inputFlagRegExes:
                if inputFlagRegEx.search(message) is None:
                    continue

                repeat = True
                message = inputFlagRegEx.sub('', message)

                if not utils.isValidStr(message):
                    return None

        if not utils.isValidStr(message):
            return None

        return message.strip()
