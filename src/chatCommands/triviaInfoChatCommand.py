from .absChatCommand import AbsChatCommand
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..misc.simpleDateTime import SimpleDateTime
from ..timber.timberInterface import TimberInterface
from ..trivia.additionalAnswers.additionalTriviaAnswers import AdditionalTriviaAnswers
from ..trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import AdditionalTriviaAnswersRepositoryInterface
from ..trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from ..trivia.history.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from ..trivia.questions.triviaQuestionReference import TriviaQuestionReference
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TriviaInfoChatCommand(AbsChatCommand):

    def __init__(
        self,
        additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
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

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __buildTriviaInfoMessage(
        self,
        additionalTriviaAnswers: AdditionalTriviaAnswers | None,
        normalizedEmote: str,
        reference: TriviaQuestionReference
    ) -> str:
        dateTime = SimpleDateTime(reference.dateTime).getDateAndTimeStr()
        triviaSource = reference.triviaSource.toStr()
        triviaType = reference.triviaType.toStr()
        isLocal = str(reference.triviaSource.isLocal).lower()

        additionalAnswersLen = 0
        if additionalTriviaAnswers is not None:
            additionalAnswersLen = len(additionalTriviaAnswers.answers)

        return f'{normalizedEmote} {triviaSource} — {dateTime} — triviaType:{triviaType} isLocal:{isLocal} triviaId:{reference.triviaId} additionalAnswers:{additionalAnswersLen}'

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

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
        if len(splits) < 2:
            self.__timber.log('TriviaInfoChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to get trivia question info as an invalid emote argument was given. Example: !triviainfo {self.__triviaEmoteGenerator.getRandomEmote()}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        emote = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('TriviaInfoChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to get trivia question info as an invalid emote argument was given. Example: !triviainfo {self.__triviaEmoteGenerator.getRandomEmote()}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if reference is None:
            self.__timber.log('TriviaInfoChatCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no trivia question reference was found ({emote}=) ({normalizedEmote=})')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")',
                replyMessageId = await ctx.getMessageId()
            )
            return

        additionalTriviaAnswers = await self.__additionalTriviaAnswersRepository.getAdditionalTriviaAnswers(
            triviaId = reference.triviaId,
            triviaQuestionType = reference.triviaType,
            triviaSource = reference.triviaSource
        )

        triviaInfoMessage = await self.__buildTriviaInfoMessage(
            additionalTriviaAnswers = additionalTriviaAnswers,
            normalizedEmote = normalizedEmote,
            reference = reference
        )

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ {triviaInfoMessage}',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('TriviaInfoChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
