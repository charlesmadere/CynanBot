from .absChatCommand import AbsChatCommand
from ..cheerActions.beanChance.beanChanceCheerAction import BeanChanceCheerAction
from ..cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class BeanInstructionsChatCommand(AbsChatCommand):

    def __init__(
        self,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        delimiter: str = ', '
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(delimiter, str):
            raise TypeError(f'delimiter argument is malformed: \"{delimiter}\"')

        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__delimiter: str = delimiter

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        cheerActions = await self.__cheerActionsRepository.getActions(
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if cheerActions is None or len(cheerActions) == 0:
            return

        beanCheerActions: list[BeanChanceCheerAction] = list()

        for cheerAction in cheerActions.values():
            if isinstance(cheerAction, BeanChanceCheerAction):
                beanCheerActions.append(cheerAction)

        if len(beanCheerActions) == 0:
            return

        beanCheerActions.sort(key = lambda element: element.bits, reverse = True)
        beanCheerActionStrings: list[str] = list()

        for beanCheerAction in beanCheerActions:
            string = await self.__toString(beanCheerAction)
            beanCheerActionStrings.append(string)

        beanChanceCheerActionsString = self.__delimiter.join(beanCheerActionStrings)

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = f'ⓘ Bean Chances: {beanChanceCheerActionsString}',
            replyMessageId = await ctx.getMessageId()
        )

        self.__timber.log('BeanInstructionsChatCommand', f'Handled !beaninstructions command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __toString(self, beanCheerAction: BeanChanceCheerAction) -> str:
        bits: str

        if beanCheerAction.bits == 1:
            bits = 'bit'
        else:
            bits = 'bits'

        return f'{beanCheerAction.bitsString} {bits} for a {beanCheerAction.randomChance}% bean chance'
