import re
from datetime import datetime
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..misc.simpleDateTime import SimpleDateTime
from ..timber.timberInterface import TimberInterface
from ..trivia.banned.triviaBanHelperInterface import TriviaBanHelperInterface
from ..trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from ..trivia.history.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class BanTriviaQuestionChatCommand(AbsChatCommand2):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        triviaBanHelper: TriviaBanHelperInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(triviaBanHelper, TriviaBanHelperInterface):
            raise TypeError(f'triviaBanHelper argument is malformed: \"{triviaBanHelper}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise TypeError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise TypeError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeZoneRepository: Final[TimeZoneRepositoryInterface] = timeZoneRepository
        self.__triviaBanHelper: Final[TriviaBanHelperInterface] = triviaBanHelper
        self.__triviaEmoteGenerator: Final[TriviaEmoteGeneratorInterface] = triviaEmoteGenerator
        self.__triviaHistoryRepository: Final[TriviaHistoryRepositoryInterface] = triviaHistoryRepository
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!bantrivia\b', re.IGNORECASE),
            re.compile(r'^\s*!bantriviaquestion\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'BanTriviaQuestionChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def __getRelativeTimeString(self, dateTime: datetime) -> str:
        now = self.__timeZoneRepository.getNow()
        questionDateTimeVersusNowSeconds = round((now - dateTime).total_seconds())

        if questionDateTimeVersusNowSeconds <= 30:
            # if the question was asked about 30 seconds ago or less, let's just say it was just now
            return 'asked just now'
        else:
            durationMessage = utils.secondsToDurationMessage(questionDateTimeVersusNowSeconds)
            return f'asked {durationMessage} ago'

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isTriviaGameEnabled and not chatMessage.twitchUser.isSuperTriviaGameEnabled:
            return ChatCommandResult.IGNORED

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return ChatCommandResult.IGNORED
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
        ):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__timber.log(self.commandName, f'Attempted to handle command, but no arguments were supplied ({splits=}) ({chatMessage=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to ban trivia question as no emote argument was given. Example: !bantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        emote: str | None = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log(self.commandName, f'Attempted to handle command, but an invalid emote argument was given ({emote=}) ({normalizedEmote=}) ({splits=}) ({chatMessage=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to ban trivia question as an invalid emote argument was given. Example: !bantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if reference is None:
            self.__timber.log(self.commandName, f'Attempted to handle command, but no trivia question reference was found ({emote=}) ({normalizedEmote=}) ({reference=}) ({splits=}) ({chatMessage=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        await self.__triviaBanHelper.ban(
            triviaId = reference.triviaId,
            userId = chatMessage.chatterUserId,
            triviaSource = reference.triviaSource,
        )

        dateAndTimeString = SimpleDateTime(reference.dateTime).getDateAndTimeStr()
        relativeTimeString = await self.__getRelativeTimeString(reference.dateTime)

        self.__twitchChatMessenger.send(
            text = f'{normalizedEmote} Banned trivia question {reference.triviaSource.toStr()}:{reference.triviaId} — {dateAndTimeString} ({relativeTimeString})',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({emote=}) ({normalizedEmote=}) ({reference=})')
        return ChatCommandResult.HANDLED
