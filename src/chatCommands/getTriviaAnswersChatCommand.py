import re
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from ..trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from ..trivia.gameController.triviaGameControllersHelperInterface import TriviaGameControllersHelperInterface
from ..trivia.history.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from ..trivia.settings.triviaSettingsInterface import TriviaSettingsInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class GetTriviaAnswersChatCommand(AbsChatCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        timber: TimberInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaGameControllersHelper: TriviaGameControllersHelperInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaSettings: TriviaSettingsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        answerDelimiter: str = ', ',
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise TypeError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaGameControllersHelper, TriviaGameControllersHelperInterface):
            raise TypeError(f'triviaGameControllersHelper argument is malformed: \"{triviaGameControllersHelper}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise TypeError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaSettings, TriviaSettingsInterface):
            raise TypeError(f'triviaSettings argument is malformed: \"{triviaSettings}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(answerDelimiter, str):
            raise TypeError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: Final[AdditionalTriviaAnswersRepositoryInterface] = additionalTriviaAnswersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaEmoteGenerator: Final[TriviaEmoteGeneratorInterface] = triviaEmoteGenerator
        self.__triviaGameControllersHelper: Final[TriviaGameControllersHelperInterface] = triviaGameControllersHelper
        self.__triviaHistoryRepository: Final[TriviaHistoryRepositoryInterface] = triviaHistoryRepository
        self.__triviaSettings: Final[TriviaSettingsInterface] = triviaSettings
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__answerDelimiter: Final[str] = answerDelimiter

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!(?:get)?triviaanswers\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'GetTriviaAnswersChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__triviaSettings.isEnabled():
            return ChatCommandResult.IGNORED
        if not chatMessage.twitchUser.isTriviaGameEnabled or not chatMessage.twitchUser.isSuperTriviaGameEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to get additional trivia answers as not enough arguments were given. Example: !gettriviaanswers {self.__triviaEmoteGenerator.getRandomEmote()}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Attempted to handle command, but not enough arguments were supplied ({splits=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        emote: str | None = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to get additional trivia answers as an invalid emote argument was given. Example: !gettriviaanswers {self.__triviaEmoteGenerator.getRandomEmote()}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Attempted to handle command, but an invalid emote argument was given ({emote=}) ({normalizedEmote=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if reference is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Attempted to handle command, but no trivia question reference was found ({reference=}) ({emote=}) ({normalizedEmote=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.CONSUMED

        result = await self.__additionalTriviaAnswersRepository.getAdditionalTriviaAnswers(
            triviaId = reference.triviaId,
            triviaQuestionType = reference.triviaType,
            triviaSource = reference.triviaSource,
        )

        if result is None:
            self.__twitchChatMessenger.send(
                text = f'{reference.emote} There are no additional trivia answers for {reference.triviaSource.toStr()}:{reference.triviaId}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
        else:
            additionalAnswers = self.__answerDelimiter.join(result.answerStrings)
            self.__twitchChatMessenger.send(
                text = f'{reference.emote} Additional trivia answers for {result.triviaSource.toStr()}:{result.triviaId} — {additionalAnswers}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

        self.__timber.log(self.commandName, f'Consumed ({result=}) ({emote=}) ({normalizedEmote=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isTriviaController = await self.__triviaGameControllersHelper.isController(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
        )

        return isStreamer or isTriviaController
