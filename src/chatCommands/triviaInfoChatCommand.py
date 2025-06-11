import locale
from datetime import datetime

from .absChatCommand import AbsChatCommand
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..misc.simpleDateTime import SimpleDateTime
from ..timber.timberInterface import TimberInterface
from ..trivia.additionalAnswers.additionalTriviaAnswers import AdditionalTriviaAnswers
from ..trivia.additionalAnswers.additionalTriviaAnswersRepositoryInterface import \
    AdditionalTriviaAnswersRepositoryInterface
from ..trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from ..trivia.history.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from ..trivia.history.triviaQuestionOccurrences import TriviaQuestionOccurrences
from ..trivia.history.triviaQuestionOccurrencesRepositoryInterface import TriviaQuestionOccurrencesRepositoryInterface
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
        timeZoneRepository: TimeZoneRepositoryInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaQuestionOccurrencesRepository: TriviaQuestionOccurrencesRepositoryInterface,
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
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(triviaEmoteGenerator, TriviaEmoteGeneratorInterface):
            raise TypeError(f'triviaEmoteGenerator argument is malformed: \"{triviaEmoteGenerator}\"')
        elif not isinstance(triviaHistoryRepository, TriviaHistoryRepositoryInterface):
            raise TypeError(f'triviaHistoryRepository argument is malformed: \"{triviaHistoryRepository}\"')
        elif not isinstance(triviaQuestionOccurrencesRepository, TriviaQuestionOccurrencesRepositoryInterface):
            raise TypeError(f'triviaQuestionOccurrencesRepository argument is malformed: \"{triviaQuestionOccurrencesRepository}\"')
        elif not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__additionalTriviaAnswersRepository: AdditionalTriviaAnswersRepositoryInterface = additionalTriviaAnswersRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaQuestionOccurrencesRepository: TriviaQuestionOccurrencesRepositoryInterface = triviaQuestionOccurrencesRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __buildTriviaInfoMessage(
        self,
        additionalTriviaAnswers: AdditionalTriviaAnswers | None,
        normalizedEmote: str,
        occurrences: TriviaQuestionOccurrences,
        reference: TriviaQuestionReference
    ) -> str:
        dateAndTimeString = SimpleDateTime(reference.dateTime).getDateAndTimeStr()
        relativeTimeString = await self.__getRelativeTimeString(reference.dateTime)
        triviaSource = reference.triviaSource.toStr()
        triviaType = reference.triviaType.toStr()
        isLocal = str(reference.triviaSource.isLocal).lower()

        additionalAnswersLen = 0
        if additionalTriviaAnswers is not None:
            additionalAnswersLen = len(additionalTriviaAnswers.answers)

        occurrencesStr = locale.format_string("%d", occurrences.occurrences, grouping = True)

        return f'{normalizedEmote} {triviaSource}:{reference.triviaId} — dateTime:{dateAndTimeString} ({relativeTimeString}) triviaType:{triviaType} isLocal:{isLocal} additionalAnswers:{additionalAnswersLen} occurrences:{occurrencesStr}'

    async def __getRelativeTimeString(self, dateTime: datetime) -> str:
        now = datetime.now(self.__timeZoneRepository.getDefault())
        questionDateTimeVersusNowSeconds = round((now - dateTime).total_seconds())

        if questionDateTimeVersusNowSeconds <= 3:
            return 'just now'
        else:
            durationMessage = utils.secondsToDurationMessage(questionDateTimeVersusNowSeconds)
            return f'{durationMessage} ago'

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

        occurrences = await self.__triviaQuestionOccurrencesRepository.getOccurrences(
            triviaId = reference.triviaId,
            triviaSource = reference.triviaSource
        )

        triviaInfoMessage = await self.__buildTriviaInfoMessage(
            additionalTriviaAnswers = additionalTriviaAnswers,
            normalizedEmote = normalizedEmote,
            occurrences = occurrences,
            reference = reference
        )

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ {triviaInfoMessage}',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('TriviaInfoChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
