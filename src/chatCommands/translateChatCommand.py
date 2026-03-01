import traceback
from typing import Final

from .absChatCommand import AbsChatCommand
from ..language.languageEntry import LanguageEntry
from ..language.languagesRepositoryInterface import LanguagesRepositoryInterface
from ..language.translationHelperInterface import TranslationHelperInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class TranslateChatCommand(AbsChatCommand):

    def __init__(
        self,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        translationHelper: TranslationHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(translationHelper, TranslationHelperInterface):
            raise TypeError(f'translationHelper argument is malformed: \"{translationHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__languagesRepository: Final[LanguagesRepositoryInterface] = languagesRepository
        self.__timber: Final[TimberInterface] = timber
        self.__translationHelper: Final[TranslationHelperInterface] = translationHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def __determineOptionalLanguageEntry(self, splits: list[str]) -> LanguageEntry | None:
        if not isinstance(splits, list) or len(splits) == 0:
            raise TypeError(f'splits argument is malformed: \"{splits}\"')

        if len(splits[1]) >= 3 and splits[1][0:2] == '--':
            return await self.__languagesRepository.getLanguageForCommand(
                command = splits[1][2:],
                hasIso6391Code = True,
            )

        return None

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.isTranslateEnabled:
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__twitchChatMessenger.send(
                text = f'⚠ Please specify the text you want to translate. Example: !translate I like tamales',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        targetLanguageEntry = await self.__determineOptionalLanguageEntry(splits)

        startSplitIndex = 1
        if targetLanguageEntry is not None:
            startSplitIndex = 2

        text = ' '.join(splits[startSplitIndex:])

        try:
            response = await self.__translationHelper.translate(
                text = text,
                targetLanguage = targetLanguageEntry,
            )

            self.__twitchChatMessenger.send(
                text = response.toStr(),
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        except Exception as e:
            self.__timber.log('TranslateCommand', f'Error translating ({targetLanguageEntry=}) ({text=})', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = '⚠ Error translating',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('TranslateCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
