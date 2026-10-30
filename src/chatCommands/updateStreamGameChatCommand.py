import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.channelInformationHelper.exceptions import RequiredTwitchAuthorizationIsMissingException
from ..twitch.channelInformationHelper.twitchChannelInformationHelperInterface import \
    TwitchChannelInformationHelperInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.exceptions import TwitchStatusCodeException
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.moderator.twitchModeratorHelperInterface import TwitchModeratorHelperInterface


class UpdateStreamGameChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        timber: TimberInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchChannelInformationHelper: TwitchChannelInformationHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchModeratorHelper: TwitchModeratorHelperInterface,
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
        elif not isinstance(twitchModeratorHelper, TwitchModeratorHelperInterface):
            raise TypeError(f'twitchModeratorHelper argument is malformed: \"{twitchModeratorHelper}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChannelEditorsRepository: Final[TwitchChannelEditorsRepositoryInterface] = twitchChannelEditorsRepository
        self.__twitchChannelInformationHelper: Final[TwitchChannelInformationHelperInterface] = twitchChannelInformationHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchModeratorHelper: Final[TwitchModeratorHelperInterface] = twitchModeratorHelper

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!set(?:stream)?game\b', re.IGNORECASE),
            re.compile(r'^\s*!update(?:stream)?game\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'UpdateStreamGameChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__timber.log(self.commandName, f'No game argument specified ({splits=}) ({chatMessage=})')
            return ChatCommandResult.IGNORED

        newGame = ' '.join(splits[1:])
        if not utils.isValidStr(newGame):
            self.__timber.log(self.commandName, f'Game argument is empty ({newGame=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.IGNORED

        try:
            updatedGame = await self.__twitchChannelInformationHelper.setGame(
                gameName = newGame,
                twitchChannelId = chatMessage.twitchChannelId,
            )
        except RequiredTwitchAuthorizationIsMissingException as e:
            self.__timber.log(self.commandName, f'Can\'t update stream game as required Twitch authorization is missing ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.CONSUMED
        except TwitchStatusCodeException as e:
            self.__timber.log(self.commandName, f'Can\'t update stream game as we encountered a Twitch status code error ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.CONSUMED
        except Exception as e:
            self.__timber.log(self.commandName, f'Failed to update stream game ({newGame=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())

            self.__twitchChatMessenger.send(
                text = '⚠ Failed to update stream game',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            return ChatCommandResult.CONSUMED

        self.__twitchChatMessenger.send(
            text = f'ⓘ Updated stream game — {updatedGame}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({updatedGame=}) ({newGame=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        isEditor = await self.__twitchChannelEditorsRepository.isEditor(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        isModerator = await self.__twitchModeratorHelper.isModerator(
            request = TwitchModeratorHelperInterface.Request(
                chatterUserId = chatMessage.chatterUserId,
                twitchChannelId = chatMessage.twitchChannelId
            ),
        )

        return isStreamer or isAdministrator or isEditor or isModerator
