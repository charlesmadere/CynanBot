from typing import Final

from .absChatCommand import AbsChatCommand
from ..timber.timberInterface import TimberInterface
from ..ttsChatter.repository.ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveTtsChatterChatCommand(AbsChatCommand):

    def __init__(
        self,
        timber: TimberInterface,
        ttsChatterRepository: TtsChatterRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        usersRepository: UsersRepositoryInterface,
    ):
        if not isinstance(ttsChatterRepository, TtsChatterRepositoryInterface):
            raise TypeError(f'ttsChatterRepository argument is malformed: \"{ttsChatterRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: Final[TimberInterface] = timber
        self.__ttsChatterRepository: Final[TtsChatterRepositoryInterface] = ttsChatterRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.areTtsChattersEnabled:
            return

        wasTtsChatter = await self.__ttsChatterRepository.remove(
            chatterUserId = ctx.getAuthorId(),
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        if wasTtsChatter:
            self.__twitchChatMessenger.send(
                text = f'ⓘ You are no longer a TTS Chatter',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        else:
            self.__twitchChatMessenger.send(
                text = f'ⓘ You weren\'t already a TTS Chatter',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('RemoveTtsChatterChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
