import re
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..aniv.helpers.anivCopyMessageTimeoutScoreHelperInterface import AnivCopyMessageTimeoutScoreHelperInterface
from ..aniv.presenters.anivCopyMessageTimeoutScorePresenterInterface import \
    AnivCopyMessageTimeoutScorePresenterInterface
from ..aniv.settings.anivSettingsInterface import AnivSettingsInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class AnivTimeoutsChatCommand(AbsChatCommand2):

    def __init__(
        self,
        anivCopyMessageTimeoutScoreHelper: AnivCopyMessageTimeoutScoreHelperInterface,
        anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface,
        anivSettings: AnivSettingsInterface,
        timber: TimberInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
    ):
        if not isinstance(anivCopyMessageTimeoutScoreHelper, AnivCopyMessageTimeoutScoreHelperInterface):
            raise TypeError(f'anivCopyMessageTimeoutScoreHelper argument is malformed: \"{anivCopyMessageTimeoutScoreHelper}\"')
        elif not isinstance(anivCopyMessageTimeoutScorePresenter, AnivCopyMessageTimeoutScorePresenterInterface):
            raise TypeError(f'anivCopyMessageTimeoutScorePresenter argument is malformed: \"{anivCopyMessageTimeoutScorePresenter}\"')
        elif not isinstance(anivSettings, AnivSettingsInterface):
            raise TypeError(f'anivSettings argument is malformed: \"{anivSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__anivCopyMessageTimeoutScoreHelper: Final[AnivCopyMessageTimeoutScoreHelperInterface] = anivCopyMessageTimeoutScoreHelper
        self.__anivCopyMessageTimeoutScorePresenter: Final[AnivCopyMessageTimeoutScorePresenterInterface] = anivCopyMessageTimeoutScorePresenter
        self.__anivSettings: Final[AnivSettingsInterface] = anivSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChannelEditorsRepository: Final[TwitchChannelEditorsRepositoryInterface] = twitchChannelEditorsRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!(?:my)?anivtimeouts?\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'AnivTimeoutsChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isAnivMessageCopyTimeoutEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__anivSettings.areCopyMessageTimeoutsEnabled():
            return ChatCommandResult.IGNORED

        printOut: str

        if await self.__twitchChannelEditorsRepository.isEditor(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId =  chatMessage.twitchChannelId,
        ):
            printOut = await self.__handleChatCommandAsEditor(
                chatMessage = chatMessage,
            )
        else:
            printOut = await self.__handleChatCommandAsRegularChatter(
                chatMessage = chatMessage,
            )

        self.__twitchChatMessenger.send(
            text = printOut,
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __handleChatCommandAsEditor(self, chatMessage: TwitchChatMessage) -> str:
        return await self.__anivCopyMessageTimeoutScorePresenter.getChannelEditorsCantPlayString(
            language = chatMessage.twitchUser.defaultLanguage,
        )

    async def __handleChatCommandAsRegularChatter(self, chatMessage: TwitchChatMessage) -> str:
        preparedScore = await self.__anivCopyMessageTimeoutScoreHelper.getScore(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        return await self.__anivCopyMessageTimeoutScorePresenter.getScoreString(
            language = chatMessage.twitchUser.defaultLanguage,
            preparedScore = preparedScore,
        )
