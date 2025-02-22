import traceback
from datetime import timedelta

from .absChatCommand import AbsChatCommand
from ..language.languageEntry import LanguageEntry
from ..language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ..language.wordOfTheDay.wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from ..language.wordOfTheDay.wordOfTheDayRepositoryInterface import WordOfTheDayRepositoryInterface
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..network.exceptions import GenericNetworkException
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class WordChatCommand(AbsChatCommand):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        wordOfTheDayPresenter: WordOfTheDayPresenterInterface,
        wordOfTheDayRepository: WordOfTheDayRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(wordOfTheDayPresenter, WordOfTheDayPresenterInterface):
            raise TypeError(f'wordOfTheDayPresenter argument is malformed: \"{wordOfTheDayPresenter}\"')
        elif not isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface):
            raise TypeError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__wordOfTheDayPresenter: WordOfTheDayPresenterInterface = wordOfTheDayPresenter
        self.__wordOfTheDayRepository: WordOfTheDayRepositoryInterface = wordOfTheDayRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isWordOfTheDayEnabled:
            return
        elif not ctx.isAuthorMod and not ctx.isAuthorVip and not self.__lastMessageTimes.isReadyAndUpdate(user.handle):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            exampleEntry = await self.__languagesRepository.getExampleLanguageEntry(hasWotdApiCode = True)
            allWotdApiCodes = await self.__languagesRepository.getAllWotdApiCodes()
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ A language code is necessary for the !word command. Example: !word {exampleEntry.requireWotdApiCode()}. Available languages: {allWotdApiCodes}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        language = splits[1]
        languageEntry: LanguageEntry

        try:
            languageEntry = await self.__languagesRepository.requireLanguageForCommand(
                command = language,
                hasWotdApiCode = True
            )
        except (RuntimeError, TypeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error retrieving LanguageEntry ({language=}): {e}', e, traceback.format_exc())
            allWotdApiCodes = await self.__languagesRepository.getAllWotdApiCodes()
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ The given language code is not supported by the !word command. Available languages: {allWotdApiCodes}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        try:
            wotd = await self.__wordOfTheDayRepository.fetchWotd(languageEntry)

            wordOfTheDayString = await self.__wordOfTheDayPresenter.toString(
                includeRomaji = False,
                wordOfTheDay = wotd
            )

            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = wordOfTheDayString,
                replyMessageId = await ctx.getMessageId()
            )
        except (GenericNetworkException, RuntimeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error fetching Word Of The Day ({languageEntry=}): {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Error fetching Word Of The Day for \"{languageEntry.humanName}\"',
                replyMessageId = await ctx.getMessageId()
            )

        self.__timber.log('WordCommand', f'Handled !word command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
