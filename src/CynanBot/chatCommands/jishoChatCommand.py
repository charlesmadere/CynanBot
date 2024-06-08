import traceback
from datetime import timedelta

import CynanBot.misc.utils as utils
from CynanBot.chatCommands.absChatCommand import AbsChatCommand
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.language.jishoHelperInterface import JishoHelperInterface
from CynanBot.misc.timedDict import TimedDict
from CynanBot.network.exceptions import GenericNetworkException
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchContext import TwitchContext
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.usersRepositoryInterface import UsersRepositoryInterface


class JishoChatCommand(AbsChatCommand):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        jishoHelper: JishoHelperInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface,
        cooldown: timedelta = timedelta(seconds = 3)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(jishoHelper, JishoHelperInterface):
            raise TypeError(f'jishoHelper argument is malformed: \"{jishoHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__jishoHelper: JishoHelperInterface = jishoHelper
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isJishoEnabled():
            return
        elif not user.isJishoEnabled():
            return
        elif not ctx.isAuthorMod() and not ctx.isAuthorVip() and not self.__lastMessageTimes.isReady(user.getHandle()):
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, '⚠ A search term is necessary for the !jisho command. Example: !jisho 食べる')
            return

        query: str | None = splits[1]

        if not utils.isValidStr(query):
            await self.__twitchUtils.safeSend(ctx, f'⚠ A search term is necessary for the !jisho command. Example: !jisho 食べる')
            return

        self.__lastMessageTimes.update(user.getHandle())

        try:
            definitions = await self.__jishoHelper.search(query)

            for definition in definitions:
                await self.__twitchUtils.safeSend(ctx, definition)
        except GenericNetworkException as e:
            self.__timber.log('JishoCommand', f'Error searching Jisho for \"{query}\": {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Error searching Jisho for \"{query}\"')

        self.__timber.log('JishoCommand', f'Handled !jisho command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')
