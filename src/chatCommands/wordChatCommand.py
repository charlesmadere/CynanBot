import traceback
from datetime import timedelta
from typing import Final

from .absChatCommand import AbsChatCommand
from ..language.exceptions import NoLanguageEntryFoundForCommandException, NoLanguageEntryFoundForWotdApiCodeException
from ..language.languageEntry import LanguageEntry
from ..language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ..language.wordOfTheDay.wordOfTheDayPresenterInterface import WordOfTheDayPresenterInterface
from ..language.wordOfTheDay.wordOfTheDayRepositoryInterface import WordOfTheDayRepositoryInterface
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class WordChatCommand(AbsChatCommand):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
        wordOfTheDayPresenter: WordOfTheDayPresenterInterface,
        wordOfTheDayRepository: WordOfTheDayRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 3),
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(wordOfTheDayPresenter, WordOfTheDayPresenterInterface):
            raise TypeError(f'wordOfTheDayPresenter argument is malformed: \"{wordOfTheDayPresenter}\"')
        elif not isinstance(wordOfTheDayRepository, WordOfTheDayRepositoryInterface):
            raise TypeError(f'wordOfTheDayRepository argument is malformed: \"{wordOfTheDayRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__languagesRepository: Final[LanguagesRepositoryInterface] = languagesRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository
        self.__wordOfTheDayPresenter: Final[WordOfTheDayPresenterInterface] = wordOfTheDayPresenter
        self.__wordOfTheDayRepository: Final[WordOfTheDayRepositoryInterface] = wordOfTheDayRepository
        self.__lastMessageTimes: Final[TimedDict] = TimedDict(cooldown)

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
            self.__twitchChatMessenger.send(
                text = f'⚠ A language code is necessary for the !word command. Example: !word {exampleEntry.requireWotdApiCode()}. Available languages: {allWotdApiCodes}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        language = splits[1]
        languageEntry: LanguageEntry

        try:
            languageEntry = await self.__languagesRepository.requireLanguageForCommand(
                command = language,
                hasWotdApiCode = True
            )
        except (NoLanguageEntryFoundForCommandException, NoLanguageEntryFoundForWotdApiCodeException, RuntimeError, TypeError, ValueError) as e:
            self.__timber.log('WordCommand', f'Error retrieving LanguageEntry ({language=}): {e}', e, traceback.format_exc())
            allWotdApiCodes = await self.__languagesRepository.getAllWotdApiCodes()
            self.__twitchChatMessenger.send(
                text = f'⚠ The given language code is not supported by the !word command. Available languages: {allWotdApiCodes}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        try:
            wotd = await self.__wordOfTheDayRepository.fetchWotd(languageEntry)

            wordOfTheDayString = await self.__wordOfTheDayPresenter.toString(
                includeRomaji = False,
                wordOfTheDay = wotd
            )

            self.__twitchChatMessenger.send(
                text = wordOfTheDayString,
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        except Exception as e:
            self.__timber.log('WordCommand', f'Error fetching Word Of The Day ({languageEntry=}): {e}', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ Error fetching Word Of The Day for \"{languageEntry.humanName}\"',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('WordChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
