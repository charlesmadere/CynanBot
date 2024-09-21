import re
from typing import Pattern

from .ttsCheerDonation import TtsCheerDonation
from .ttsCommandBuilderInterface import TtsCommandBuilderInterface
from .ttsDonationType import TtsDonationType
from .ttsEvent import TtsEvent
from .ttsProvider import TtsProvider
from .ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from .ttsSubscriptionDonation import TtsSubscriptionDonation
from .ttsSubscriptionDonationGiftType import TtsSubscriptionDonationGiftType
from ..contentScanner.contentCode import ContentCode
from ..contentScanner.contentScannerInterface import ContentScannerInterface
from ..emojiHelper.emojiHelperInterface import EmojiHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface


class TtsCommandBuilder(TtsCommandBuilderInterface):

    def __init__(
        self,
        contentScanner: ContentScannerInterface,
        emojiHelper: EmojiHelperInterface,
        timber: TimberInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface
    ):
        if not isinstance(contentScanner, ContentScannerInterface):
            raise TypeError(f'contentScanner argument is malformed: \"{contentScanner}\"')
        elif not isinstance(emojiHelper, EmojiHelperInterface):
            raise TypeError(f'emojiHelper argument is malformed: \"{emojiHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')

        self.__contentScanner: ContentScannerInterface = contentScanner
        self.__emojiHelper: EmojiHelperInterface = emojiHelper
        self.__timber: TimberInterface = timber
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository

        self.__inlineCommandRegExes: list[Pattern] = self.__buildInlineCommandStrings()
        self.__inputFlagRegExes: list[Pattern] = self.__buildInputFlagStrings()
        self.__whiteSpaceRegEx: Pattern = re.compile(r'\s{2,}', re.IGNORECASE)

    async def buildAndCleanEvent(self, event: TtsEvent | None) -> str | None:
        if event is not None and not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if event is None:
            return None

        prefix = await self.__processDonationPrefix(event)
        message = event.message

        if utils.isValidStr(message):
            message = await self.buildAndCleanMessage(
                provider = event.provider,
                message = message
            )

        if utils.isValidStr(prefix) and utils.isValidStr(message):
            return f'{prefix} {message}'
        elif utils.isValidStr(prefix):
            return prefix
        elif utils.isValidStr(message):
            return message
        else:
            return None

    async def buildAndCleanMessage(
        self,
        provider: TtsProvider,
        message: str | None
    ) -> str | None:
        if not isinstance(provider, TtsProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')
        elif not utils.isValidStr(message):
            return None

        contentCode = await self.__contentScanner.scan(message)
        if contentCode is not ContentCode.OK:
            self.__timber.log('TtsCommandBuilder', f'TTS command \"{message}\" returned a bad content code: \"{contentCode}\"')
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

        if provider is TtsProvider.DEC_TALK:
            # DECTalk requires Windows-1252 encoding
            message = message.encode().decode('windows-1252')

        return message

    def __buildInlineCommandStrings(self) -> list[Pattern]:
        inlineCommandStrings: list[Pattern] = list()

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

    def __buildInputFlagStrings(self) -> list[Pattern]:
        inputFlagStrings: list[Pattern] = list()

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

    async def __cropMessageIfNecessary(self, message: str | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        maxMessageSize = await self.__ttsSettingsRepository.getMaximumMessageSize()

        if len(message) > maxMessageSize:
            self.__timber.log('TtsCommandBuilder', f'Chopping down TTS command \"{message}\" as it is too long (len={len(message)}) ({maxMessageSize=}) ({message})')
            message = message[:maxMessageSize].strip()

        if not utils.isValidStr(message):
            return None

        return message

    async def __processCheerDonationPrefix(
        self,
        event: TtsEvent,
        donation: TtsCheerDonation
    ) -> str | None:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(donation, TtsCheerDonation):
            raise TypeError(f'donation argument is malformed: \"{donation}\"')
        elif donation.donationType is not TtsDonationType.CHEER:
            raise TypeError(f'TtsDonationType is not {TtsDonationType.CHEER}: \"{donation.donationType}\" ({donation=})')

        return f'{event.userName} cheered {donation.bits}!'

    async def __processDonationPrefix(self, event: TtsEvent) -> str | None:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        donation = event.donation

        if donation is None:
            return None

        if isinstance(donation, TtsCheerDonation):
            return await self.__processCheerDonationPrefix(
                event = event,
                donation = donation
            )
        elif isinstance(donation, TtsSubscriptionDonation):
            return await self.__processSubscriptionDonationPrefix(
                event = event,
                donation = donation
            )
        else:
            raise RuntimeError(f'donation type is unknown: \"{type(donation)=}\"')

    async def __processSubscriptionDonationPrefix(
        self,
        event: TtsEvent,
        donation: TtsSubscriptionDonation
    ) -> str:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')
        elif not isinstance(donation, TtsSubscriptionDonation):
            raise TypeError(f'donation argument is malformed: \"{donation}\"')
        elif donation.donationType is not TtsDonationType.SUBSCRIPTION:
            raise TypeError(f'TtsDonationType is not {TtsDonationType.SUBSCRIPTION}: \"{donation.donationType}\" ({donation=})')

        # I don't think it makes sense for a subscription to be anonymous, and also not a gift?

        match donation.giftType:
            case TtsSubscriptionDonationGiftType.GIVER:
                if donation.isAnonymous:
                    return 'anonymous gifted a sub!'
                else:
                    return f'{event.userName} gifted a sub!'

            case TtsSubscriptionDonationGiftType.RECEIVER:
                if utils.isValidStr(donation.subGiftGiverDisplayName) and not donation.isAnonymous:
                    return f'{event.userName} received a sub gift from {donation.subGiftGiverDisplayName}!'
                else:
                    return f'{event.userName} received a sub gift!'

            case _:
                return f'{event.userName} subscribed!'

    async def __purgeCheers(self, message: str | None) -> str | None:
        if not utils.isValidStr(message):
            return None

        message = utils.removeCheerStrings(message)

        if not utils.isValidStr(message):
            return None

        return message.strip()

    async def __purgeInlineCommands(self, message: str | None) -> str | None:
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

    async def __purgeInputFlags(self, message: str | None) -> str | None:
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
