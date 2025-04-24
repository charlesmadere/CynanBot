from .absChatCommand import AbsChatCommand
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.configuration.twitchContext import TwitchContext


class SkipTtsChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        compositeTtsManagerProvider: CompositeTtsManagerProviderInterface,
        timber: TimberInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__compositeTtsManagerProvider: CompositeTtsManagerProviderInterface = compositeTtsManagerProvider
        self.__timber: TimberInterface = timber
        self.__twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface = twitchChannelEditorsRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        administrator = await self.__administratorProvider.getAdministratorUserId()

        editorIds = await self.__twitchChannelEditorsRepository.fetchEditorIds(
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        if administrator != ctx.getAuthorId() and ctx.getAuthorId() not in editorIds:
            self.__timber.log('SkipTtsChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()} tried using this command!')
            return

        compositeTtsManager = self.__compositeTtsManagerProvider.getSharedInstance()
        await compositeTtsManager.stopTtsEvent()

        self.__timber.log('SkipTtsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {ctx.getTwitchChannelName()}')
