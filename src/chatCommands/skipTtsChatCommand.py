from .absChatCommand import AbsChatCommand
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..tts.compositeTtsManagerInterface import CompositeTtsManagerInterface
from ..twitch.configuration.twitchContext import TwitchContext


class SkipTtsChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        compositeTtsManager: CompositeTtsManagerInterface,
        timber: TimberInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(compositeTtsManager, CompositeTtsManagerInterface):
            raise TypeError(f'compositeTtsManager argument is malformed: \"{compositeTtsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__compositeTtsManager: CompositeTtsManagerInterface = compositeTtsManager
        self.__timber: TimberInterface = timber

    async def handleChatCommand(self, ctx: TwitchContext):
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if administrator != ctx.getAuthorId():
            self.__timber.log('SkipTtsChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()} tried using this command!')
            return

        await self.__compositeTtsManager.stopTtsEvent()
        self.__timber.log('SkipTtsChatCommand', f'Handled !skiptts command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}')
