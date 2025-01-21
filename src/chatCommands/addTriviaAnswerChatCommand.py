import traceback

from .absChatCommand import AbsChatCommand
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
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AddTriviaAnswerChatCommand(AbsChatCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        answerDelimiter: str = ', '
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
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(answerDelimiter, str):
            raise TypeError(f'answerDelimiter argument is malformed: \"{answerDelimiter}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__answerDelimiter: str = answerDelimiter

    async def handleChatCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled and not user.isSuperTriviaGameEnabled:
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 3:
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but not enough arguments were supplied')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to add additional trivia answer as not enough arguments were given. Example: !addtriviaanswer {self.__triviaEmoteGenerator.getRandomEmote()} Theodore Roosevelt',
                replyMessageId = await ctx.getMessageId()
            )
            return

        emote: str | None = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to add additional trivia answer as an invalid emote argument was given. Example: !addtriviaanswer {self.__triviaEmoteGenerator.getRandomEmote()} Theodore Roosevelt',
                replyMessageId = await ctx.getMessageId()
            )
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if reference is None:
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")',
                replyMessageId = await ctx.getMessageId()
            )
            return

        additionalAnswer: str | None = ' '.join(splits[2:])
        if not utils.isValidStr(additionalAnswer):
            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but an invalid additional answer was given: \"{additionalAnswer}\"')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to add additional trivia answer as an invalid answer argument was given. Example: !addtriviaanswer {self.__triviaEmoteGenerator.getRandomEmote()} Theodore Roosevelt',
                replyMessageId = await ctx.getMessageId()
            )
            return

        try:
            result = await self.__additionalTriviaAnswersRepository.addAdditionalTriviaAnswer(
                additionalAnswer = additionalAnswer,
                triviaId = reference.triviaId,
                userId = ctx.getAuthorId(),
                triviaQuestionType = reference.triviaType,
                triviaSource = reference.triviaSource
            )

            additionalAnswers = self.__answerDelimiter.join(result.answerStrings)

            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'{reference.emote} Added additional trivia answer for {result.triviaSource.toStr()}:{result.triviaId} — {additionalAnswers}',
                replyMessageId = await ctx.getMessageId()
            )

            self.__timber.log('AddTriviaAnswerCommand', f'Added additional trivia answer for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}: \"{additionalAnswer}\"')
        except AdditionalTriviaAnswerAlreadyExistsException as e:
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'{reference.emote} Unable to add additional trivia answer for {reference.triviaSource.toStr()}:{reference.triviaId} as it already exists',
                replyMessageId = await ctx.getMessageId()
            )

            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but the additional answer already exists: \"{additionalAnswer}\"', e, traceback.format_exc())
        except AdditionalTriviaAnswerIsMalformedException as e:
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'{reference.emote} Unable to add additional trivia answer for {reference.triviaSource.toStr()}:{reference.triviaId} as it is malformed',
                replyMessageId = await ctx.getMessageId()
            )

            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but the additional answer is malformed: \"{additionalAnswer}\"', e, traceback.format_exc())
        except AdditionalTriviaAnswerIsUnsupportedTriviaTypeException as e:
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'{reference.emote} Unable to add additional trivia answer for {reference.triviaSource.toStr()}:{reference.triviaId} as the question is an unsupported type ({reference.triviaType.toStr()})',
                replyMessageId = await ctx.getMessageId()
            )

            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but the question is an unsupported type: \"{reference.triviaType.toStr()}\"', e, traceback.format_exc())
        except TooManyAdditionalTriviaAnswersException as e:
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'{reference.emote} Unable to add additional trivia answer for {reference.triviaSource.toStr()}:{reference.triviaId} as the question has too many additional answers ({reference.triviaType.toStr()})',
                replyMessageId = await ctx.getMessageId()
            )

            self.__timber.log('AddTriviaAnswerCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but the question has too many additional answers', e, traceback.format_exc())

        self.__timber.log('AddTriviaAnswerCommand', f'Handled !addtriviaanswer command with for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
