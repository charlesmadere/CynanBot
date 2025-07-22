from typing import Final

from .absChatCommand import AbsChatCommand
from ..ecco.eccoHelperInterface import EccoHelperInterface
from ..ecco.exceptions import EccoFailedToFetchTimeRemaining
from ..ecco.models.absEccoTimeRemaining import AbsEccoTimeRemaining
from ..ecco.models.eccoReleased import EccoReleased
from ..ecco.models.eccoTimeRemaining import EccoTimeRemaining
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class EccoChatCommand(AbsChatCommand):

    def __init__(
        self,
        eccoHelper: EccoHelperInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(eccoHelper, EccoHelperInterface):
            raise TypeError(f'eccoHelper argument is malformed: \"{eccoHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__eccoHelper: Final[EccoHelperInterface] = eccoHelper
        self.__timber: Final[TimberInterface] = timber
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isEccoEnabled:
            return

        try:
            eccoTimeRemaining = await self.__eccoHelper.fetchEccoTimeRemaining()
        except EccoFailedToFetchTimeRemaining as e:
            self.__timber.log('EccoChatCommand', f'Failed to fetch Ecco time remaining for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}: {e}', e)
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Error fetching Ecco time remaining',
                replyMessageId = await ctx.getMessageId(),
            )
            return

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = await self.__toString(eccoTimeRemaining),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('EccoChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __toString(self, eccoTimeRemaining: AbsEccoTimeRemaining) -> str:
        if isinstance(eccoTimeRemaining, EccoReleased):
            return f'🐬 Ecco info is available now! https://www.eccothedolphin.com/'

        elif isinstance(eccoTimeRemaining, EccoTimeRemaining):
            durationMessage = utils.secondsToDurationMessage(eccoTimeRemaining.remainingSeconds)
            return f'🐬 New Ecco info coming in {durationMessage}!'

        else:
            raise RuntimeError(f'Encountered unknown AbsEccoTimeRemaining type: \"{eccoTimeRemaining}\"')
