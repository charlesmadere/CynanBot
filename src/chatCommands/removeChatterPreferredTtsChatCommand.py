from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.repository.chatterPreferredTtsRepositoryInterface import \
    ChatterPreferredTtsRepositoryInterface
from ..chatterPreferredTts.settings.chatterPreferredTtsSettingsRepositoryInterface import \
    ChatterPreferredTtsSettingsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveChatterPreferredTtsChatCommand(AbsChatCommand):

    def __init__(
        self,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__chatterPreferredTtsPresenter: Final[ChatterPreferredTtsPresenter] = chatterPreferredTtsPresenter
        self.__chatterPreferredTtsRepository: Final[ChatterPreferredTtsRepositoryInterface] = chatterPreferredTtsRepository
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        if not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return

        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.isChatterPreferredTtsEnabled:
            return

        preferredTts = await self.__chatterPreferredTtsRepository.remove(
            chatterUserId = ctx.getAuthorId(),
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        if preferredTts is None:
            self.__twitchChatMessenger.send(
                text = f'ⓘ You don\'t currently have a preferred TTS to delete',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        else:
            printOut = await self.__chatterPreferredTtsPresenter.printOut(
                preferredTts = preferredTts,
            )

            self.__twitchChatMessenger.send(
                text = f'ⓘ Your preferred TTS was deleted, it previously was: {printOut}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('RemoveChatterPreferredTtsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
