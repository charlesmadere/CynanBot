from datetime import datetime

from .absChatCommand import AbsChatCommand
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..misc import utils as utils
from ..misc.generalSettingsRepository import GeneralSettingsRepository
from ..misc.simpleDateTime import SimpleDateTime
from ..timber.timberInterface import TimberInterface
from ..trivia.banned.triviaBanHelperInterface import TriviaBanHelperInterface
from ..trivia.emotes.triviaEmoteGeneratorInterface import TriviaEmoteGeneratorInterface
from ..trivia.history.triviaHistoryRepositoryInterface import TriviaHistoryRepositoryInterface
from ..trivia.triviaUtilsInterface import TriviaUtilsInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class BanTriviaQuestionChatCommand(AbsChatCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        triviaBanHelper: TriviaBanHelperInterface,
        triviaEmoteGenerator: TriviaEmoteGeneratorInterface,
        triviaHistoryRepository: TriviaHistoryRepositoryInterface,
        triviaUtils: TriviaUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
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
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__triviaBanHelper: TriviaBanHelperInterface = triviaBanHelper
        self.__triviaEmoteGenerator: TriviaEmoteGeneratorInterface = triviaEmoteGenerator
        self.__triviaHistoryRepository: TriviaHistoryRepositoryInterface = triviaHistoryRepository
        self.__triviaUtils: TriviaUtilsInterface = triviaUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def __getRelativeTimeString(self, dateTime: datetime) -> str:
        now = datetime.now(self.__timeZoneRepository.getDefault())
        questionDateTimeVersusNowSeconds = round((now - dateTime).total_seconds())

        if questionDateTimeVersusNowSeconds <= 30:
            # if the question was asked about 30 seconds ago or less, let's just say it was just now
            return 'asked just now'
        else:
            durationMessage = utils.secondsToDurationMessage(questionDateTimeVersusNowSeconds)
            return f'asked {durationMessage} ago'

    async def handleChatCommand(self, ctx: TwitchContext):
        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not generalSettings.isTriviaGameEnabled() and not generalSettings.isSuperTriviaGameEnabled():
            return
        elif not user.isTriviaGameEnabled and not user.isSuperTriviaGameEnabled:
            return
        elif not await self.__triviaUtils.isPrivilegedTriviaUser(
            twitchChannelId = await ctx.getTwitchChannelId(),
            userId = ctx.getAuthorId()
        ):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('BanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no arguments were supplied')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to ban trivia question as no emote argument was given. Example: !bantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        emote: str | None = splits[1]
        normalizedEmote = await self.__triviaEmoteGenerator.getValidatedAndNormalizedEmote(emote)

        if not utils.isValidStr(normalizedEmote):
            self.__timber.log('BanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but an invalid emote argument was given: \"{emote}\"')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to ban trivia question as an invalid emote argument was given. Example: !bantriviaquestion {self.__triviaEmoteGenerator.getRandomEmote()}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        reference = await self.__triviaHistoryRepository.getMostRecentTriviaQuestionDetails(
            emote = normalizedEmote,
            twitchChannel = user.handle,
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if reference is None:
            self.__timber.log('BanTriviaQuestionCommand', f'Attempted to handle command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}, but no trivia question reference was found with emote \"{emote}\"')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ No trivia question reference was found with emote \"{emote}\" (normalized: \"{normalizedEmote}\")',
                replyMessageId = await ctx.getMessageId()
            )
            return

        await self.__triviaBanHelper.ban(
            triviaId = reference.triviaId,
            userId = ctx.getAuthorId(),
            triviaSource = reference.triviaSource
        )

        dateAndTimeString = SimpleDateTime(reference.dateTime).getDateAndTimeStr()
        relativeTimeString = await self.__getRelativeTimeString(reference.dateTime)

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'{normalizedEmote} Banned trivia question {reference.triviaSource.toStr()}:{reference.triviaId} — {dateAndTimeString} ({relativeTimeString})',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('BanTriviaQuestionCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({emote=}) ({normalizedEmote=}) ({reference=})')
