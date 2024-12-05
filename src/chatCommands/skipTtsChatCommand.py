from .absChatCommand import AbsChatCommand
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..tts.ttsManagerInterface import TtsManagerInterface
from ..twitch.configuration.twitchContext import TwitchContext


class SkipTtsChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        ttsManager: TtsManagerInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsManager, TtsManagerInterface):
            raise TypeError(f'ttsManager argument is malformed: \"{ttsManager}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__timber: TimberInterface = timber
        self.__ttsManager: TtsManagerInterface = ttsManager

    async def handleChatCommand(self, ctx: TwitchContext):
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if administrator != ctx.getAuthorId():
            self.__timber.log('SkipTtsChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()} tried using this command!')
            return

        await self.__ttsManager.stopTtsEvent()
        self.__timber.log('SkipTtsChatCommand', f'Handled !skiptts command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}')
