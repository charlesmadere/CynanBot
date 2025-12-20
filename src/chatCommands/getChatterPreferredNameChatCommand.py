from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ..chatterPreferredName.settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext


class GetChatterPreferredNameChatCommand(AbsChatCommand):

    def __init__(
        self,
        chatterPreferredNameHelper: ChatterPreferredNameHelperInterface,
        chatterPreferredNameSettings: ChatterPreferredNameSettingsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(chatterPreferredNameHelper, ChatterPreferredNameHelperInterface):
            raise TypeError(f'chatterPreferredNameHelper argument is malformed: \"{chatterPreferredNameHelper}\"')
        elif not isinstance(chatterPreferredNameSettings, ChatterPreferredNameSettingsInterface):
            raise TypeError(f'chatterPreferredNameSettings argument is malformed: \"{chatterPreferredNameSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__chatterPreferredNameHelper: Final[ChatterPreferredNameHelperInterface] = chatterPreferredNameHelper
        self.__chatterPreferredNameSettings: Final[ChatterPreferredNameSettingsInterface] = chatterPreferredNameSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

    async def handleChatCommand(self, ctx: TwitchContext):
        if not await self.__chatterPreferredNameSettings.isEnabled():
            return

        preferredNameData = await self.__chatterPreferredNameHelper.get(
            chatterUserId = ctx.getAuthorId(),
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        if preferredNameData is None:
            self.__twitchChatMessenger.send(
                text = f'ⓘ You currently don\'t have a preferred name',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        else:
            self.__twitchChatMessenger.send(
                text = f'ⓘ Your preferred name: {preferredNameData.preferredName}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('GetChatterPreferredNameChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}')
