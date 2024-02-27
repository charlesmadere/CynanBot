from datetime import timedelta

import CynanBot.misc.utils as utils
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.misc.timedDict import TimedDict
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class CommandsChatCommand(AbsChatCommand):

    def __init__(
        self,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        commandsUrl: str = 'https://cynanbot.io/',
        cooldown: timedelta = timedelta(minutes = 1),
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidUrl(commandsUrl):
            raise TypeError(f'commandsUrl argument is malformed: \"{commandsUrl}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__commandsUrl: str = commandsUrl
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not ctx.isAuthorMod() and not self.__lastMessageTimes.isReadyAndUpdate(user.getHandle()):
            return

        await self.__twitchUtils.safeSend(ctx, f'ⓘ Commands: {self.__commandsUrl}')
        self.__timber.log('CommandsChatCommand', f'Handled !commands command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
