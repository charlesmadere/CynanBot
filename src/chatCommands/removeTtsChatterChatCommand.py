from .absChatCommand import AbsChatCommand
from ..timber.timberInterface import TimberInterface
from ..ttsChatter.repository.ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveTtsChatterChatCommand(AbsChatCommand):

    def __init__(
        self,
        timber: TimberInterface,
        ttsChatterRepository: TtsChatterRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(ttsChatterRepository, TtsChatterRepositoryInterface):
            raise TypeError(f'ttsChatterRepository argument is malformed: \"{ttsChatterRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__timber: TimberInterface = timber
        self.__ttsChatterRepository: TtsChatterRepositoryInterface = ttsChatterRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.areTtsChattersEnabled:
            return

        wasTtsChatter = await self.__ttsChatterRepository.remove(
            chatterUserId = ctx.getAuthorId(),
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if wasTtsChatter:
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'ⓘ You are no longer a TTS Chatter',
                replyMessageId = await ctx.getMessageId()
            )
        else:
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'ⓘ You weren\'t already a TTS Chatter',
                replyMessageId = await ctx.getMessageId()
            )

        self.__timber.log('RemoveTtsChatterChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
