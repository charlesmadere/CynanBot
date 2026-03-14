import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..timber.timberInterface import TimberInterface
from ..trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from ..trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from ..trivia.history.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from ..trivia.triviaExceptions import (AdditionalTriviaAnswerAlreadyExistsException,
                                       AdditionalTriviaAnswerIsMalformedException,
                                       AdditionalTriviaAnswerIsUnsupportedTriviaTypeException,
                                       TooManyAdditionalTriviaAnswersException)
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class AddTriviaAnswerChatCommand(AbsChatCommand2):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        answerDelimiter: str = ', ',
    ):
        if not isinstance(additionalTriviaAnswersRepository, AdditionalTriviaAnswersRepositoryInterface):
            raise TypeError(f'additionalTriviaAnswersRepository argument is malformed: \"{additionalTriviaAnswersRepository}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise TypeError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise TypeError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(answerDelimiter, str):
            raise TypeError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: Final[AdditionalTriviaAnswersRepositoryInterface] = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: Final[GeneralSettingsRepository] = generalSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__triviaEmoteGenerator: Final[TriviaEmoteGeneratorInterface] = triviaEmoteGenerator
        self.__triviaHistoryRepository: Final[TriviaHistoryRepositoryInterface] = triviaHistoryRepository
        self.__triviaUtils: Final[TriviaUtilsInterface] = triviaUtils
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__answerDelimiter: Final[str] = answerDelimiter

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!addtriviaanswer\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'AddTriviaAnswerChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isTriviaGameEnabled or not chatMessage.twitchUser.isSuperTriviaGameEnabled:
            return ChatCommandResult.IGNORED

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if not generalSettings.isTriviaGameEnabled() or not generalSettings.isSuperTriviaGameEnabled():
            return ChatCommandResult.IGNORED
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannelId = chatMessage.twitchChannelId,
            userId = chatMessage.chatterUserId,
        ):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 3:
            self.__timber.log(self.commandName, f'Attempted to handle command, but not enough arguments were supplied ({chatMessage=}) ({splits=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add additional trivia answer as not enough arguments were given. Example: !addtriviaanswer {self.__triviaEmoteGenerator.getRandomEmote()} Theodore Roosevelt',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        emote: str | None = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log(self.commandName, f'Attempted to handle command, but an invalid emote argument was given ({emote=}) ({normalizedEmote=}) ({chatMessage=}) ({splits=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add additional trivia answer as an invalid emote argument was given. Example: !addtriviaanswer {self.__triviaEmoteGenerator.getRandomEmote()} Theodore Roosevelt',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = chatMessage.twitchChannel,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        if reference is None:
            self.__timber.log(self.commandName, f'Attempted to handle command, but no trivia question reference was found with emote ({emote=}) ({normalizedEmote=}) ({reference=}) ({chatMessage=}) ({splits=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        additionalAnswer: str | None = ' '.join(splits[2:])
        if not utils.isValidStr(additionalAnswer):
            self.__timber.log(self.commandName, f'Attempted to handle command, but an invalid additional answer was given ({additionalAnswer=}) ({reference=}) ({emote=}) ({normalizedEmote=}) ({chatMessage=}) ({splits=})')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to add additional trivia answer as an invalid answer argument was given. Example: !addtriviaanswer {self.__triviaEmoteGenerator.getRandomEmote()} Theodore Roosevelt',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )
            return ChatCommandResult.HANDLED

        try:
            result = await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswer(
                additionalAnswer = additionalAnswer,
                triviaId = reference.triviaId,
                userId = chatMessage.chatterUserId,
                triviaQuestionType = reference.triviaType,
                triviaSource = reference.triviaSource,
            )

            additionalAnswers = self.__answerDelimiter.join(result.answerStrings)

            self.__twitchChatMessenger.send(
                text = f'{reference.emote} Added additional trivia answer for {result.triviaSource.toStr()}:{result.triviaId} — {additionalAnswers}',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Added additional trivia answer ({additionalAnswer=}) ({reference=}) ({emote=}) ({normalizedEmote=}) ({chatMessage=})')
        except AdditionalTriviaAnswerAlreadyExistsException as e:
            self.__twitchChatMessenger.send(
                text = f'{reference.emote} Unable to add additional trivia answer for {reference.triviaSource.toStr()}:{reference.triviaId} as it already exists',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Attempted to handle command, but the additional answer already exists ({additionalAnswer=}) ({reference=}) ({emote=}) ({normalizedEmote=}) ({chatMessage=})', e, traceback.format_exc())
        except AdditionalTriviaAnswerIsMalformedException as e:
            self.__twitchChatMessenger.send(
                text = f'{reference.emote} Unable to add additional trivia answer for {reference.triviaSource.toStr()}:{reference.triviaId} as it is malformed',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Attempted to handle command, but the additional answer is malformed ({additionalAnswer=}) ({reference=}) ({emote=}) ({normalizedEmote=}) ({chatMessage=})', e, traceback.format_exc())
        except AdditionalTriviaAnswerIsUnsupportedTriviaTypeException as e:
            self.__twitchChatMessenger.send(
                text = f'{reference.emote} Unable to add additional trivia answer for {reference.triviaSource.toStr()}:{reference.triviaId} as the question is an unsupported type ({reference=})',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Attempted to handle command, but the question is an unsupported type ({additionalAnswer=}) ({reference=}) ({emote=}) ({normalizedEmote=}) ({chatMessage=})', e, traceback.format_exc())
        except TooManyAdditionalTriviaAnswersException as e:
            self.__twitchChatMessenger.send(
                text = f'{reference.emote} Unable to add additional trivia answer for {reference.triviaSource.toStr()}:{reference.triviaId} as the question has too many additional answers ({reference.triviaType.toStr()})',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Attempted to handle command, but the question has too many additional answers ({additionalAnswer=}) ({reference=}) ({emote=}) ({normalizedEmote=}) ({chatMessage=})', e, traceback.format_exc())

        self.__timber.log(self.commandName, f'Handled ({additionalAnswer=}) ({reference=}) ({emote=}) ({normalizedEmote=})')
        return ChatCommandResult.HANDLED
