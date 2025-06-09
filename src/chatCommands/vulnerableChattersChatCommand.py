import locale
from dataclasses import dataclass
from typing import Final

from .absChatCommand import AbsChatCommand
from ..timber.timberInterface import TimberInterface
from ..twitch.activeChatters.activeChatter import ActiveChatter
from ..twitch.activeChatters.activeChattersRepositoryInterface import ActiveChattersRepositoryInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.timeout.timeoutImmuneUserIdsRepositoryInterface import TimeoutImmuneUserIdsRepositoryInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class VulnerableChattersChatCommand(AbsChatCommand):

    @dataclass(frozen = True)
    class VulnerableChattersData:
        totalActiveChatters: int
        totalVulnerableChatters: int

        @property
        def totalActiveChattersStr(self) -> str:
            return locale.format_string("%d", self.totalActiveChatters, grouping = True)

        @property
        def totalVulnerableChattersStr(self) -> str:
            return locale.format_string("%d", self.totalVulnerableChatters, grouping = True)

    def __init__(
        self,
        activeChattersRepository: ActiveChattersRepositoryInterface,
        timber: TimberInterface,
        timeoutImmuneUserIdsRepository: TimeoutImmuneUserIdsRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(activeChattersRepository, ActiveChattersRepositoryInterface):
            raise TypeError(f'activeChattersRepository argument is malformed: \"{activeChattersRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__activeChattersRepository: Final[ActiveChattersRepositoryInterface] = activeChattersRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutImmuneUserIdsRepository: Final[TimeoutImmuneUserIdsRepositoryInterface] = timeoutImmuneUserIdsRepository
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def __getVulnerableChattersData(self, twitchChannelId: str) -> VulnerableChattersData:
        activeChatters = await self.__activeChattersRepository.get(
            twitchChannelId = twitchChannelId
        )

        vulnerableChatters: dict[str, ActiveChatter] = dict(activeChatters)
        vulnerableChatters.pop(twitchChannelId, None)

        allImmuneUserIds = await self.__timeoutImmuneUserIdsRepository.getAllUserIds()

        for immuneUserId in allImmuneUserIds:
            vulnerableChatters.pop(immuneUserId, None)

        return VulnerableChattersChatCommand.VulnerableChattersData(
            totalActiveChatters = len(activeChatters),
            totalVulnerableChatters = len(vulnerableChatters)
        )

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isVulnerableChattersEnabled:
            return

        chattersData = await self.__getVulnerableChattersData(
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        message = f'ⓘ There are {chattersData.totalVulnerableChattersStr} vulnerable chatter(s) and {chattersData.totalActiveChattersStr} active chatter(s)'

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = message,
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('VulnerableChattersChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
