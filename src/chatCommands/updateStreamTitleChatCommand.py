import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.channelInformationHelper.twitchChannelInformationHelperInterface import \
    TwitchChannelInformationHelperInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage


class UpdateStreamTitleChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchChannelInformationHelper: TwitchChannelInformationHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')
        elif not isinstance(twitchChannelInformationHelper, TwitchChannelInformationHelperInterface):
            raise TypeError(f'twitchChannelInformationHelper argument is malformed: \"{twitchChannelInformationHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChannelEditorsRepository: Final[TwitchChannelEditorsRepositoryInterface] = twitchChannelEditorsRepository
        self.__twitchChannelInformationHelper: Final[TwitchChannelInformationHelperInterface] = twitchChannelInformationHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = twitchFriendsUserIdRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!set(?:stream)?title\b', re.IGNORECASE),
            re.compile(r'^\s*!update(?:stream)?title\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'UpdateStreamTitleChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            return ChatCommandResult.IGNORED

        newTitle = ' '.join(splits[1:])
        if not utils.isValidStr(newTitle):
            return ChatCommandResult.IGNORED

        if chatMessage.twitchUser.arePranksEnabled and await self.__stopForPrank(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        ):
            return ChatCommandResult.IGNORED

        try:
            updatedTitle = await self.__twitchChannelInformationHelper.setTitle(
                title = newTitle,
                twitchChannelId = chatMessage.twitchChannelId,
            )
        except Exception as e:
            self.__timber.log(self.commandName, f'Failed to update stream title ({newTitle=}) ({chatMessage=})', e, traceback.format_exc())

            self.__twitchChatMessenger.send(
                text = '⚠ Failed to update stream title',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            return ChatCommandResult.CONSUMED

        self.__twitchChatMessenger.send(
            text = f'ⓘ Updated stream title — {updatedTitle}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({updatedTitle=}) ({newTitle=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        isEditor = await self.__twitchChannelEditorsRepository.isEditor(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        return isStreamer or isAdministrator or isEditor

    async def __stopForPrank(
        self,
        chatterUserId: str,
        twitchChannelId: str,
    ) -> bool:
        # TODO prank code goes here
        return False
