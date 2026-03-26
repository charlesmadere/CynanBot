import re
import traceback
from dataclasses import dataclass
from typing import Collection, Final, Pattern

from .absChatCommand2 import AbsChatCommand2
from .chatCommandResult import ChatCommandResult
from ..chatterPreferredName.exceptions import ChatterPreferredNameFeatureIsDisabledException, \
    ChatterPreferredNameIsInvalidException
from ..chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ..chatterPreferredName.settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class SetChatterPreferredNameChatCommand(AbsChatCommand2):

    @dataclass(frozen = True, slots = True)
    class LookupUserInfo:
        userId: str | None
        userName: str

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        chatterPreferredNameHelper: ChatterPreferredNameHelperInterface,
        chatterPreferredNameSettings: ChatterPreferredNameSettingsInterface,
        timber: TimberInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(chatterPreferredNameHelper, ChatterPreferredNameHelperInterface):
            raise TypeError(f'chatterPreferredNameHelper argument is malformed: \"{chatterPreferredNameHelper}\"')
        elif not isinstance(chatterPreferredNameSettings, ChatterPreferredNameSettingsInterface):
            raise TypeError(f'chatterPreferredNameSettings argument is malformed: \"{chatterPreferredNameSettings}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__chatterPreferredNameHelper: Final[ChatterPreferredNameHelperInterface] = chatterPreferredNameHelper
        self.__chatterPreferredNameSettings: Final[ChatterPreferredNameSettingsInterface] = chatterPreferredNameSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!set(?:preferred)?name\b', re.IGNORECASE),
        })

    @property
    def commandName(self) -> str:
        return 'SetChatterPreferredNameChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not chatMessage.twitchUser.isChatterPreferredNameEnabled:
            return ChatCommandResult.IGNORED
        elif not await self.__chatterPreferredNameSettings.isEnabled():
            return ChatCommandResult.IGNORED
        elif not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 3:
            self.__twitchChatMessenger.send(
                text = f'⚠ Username and preferred name is necessary for this command. Example: !setpreferredname {twitchHandle} example',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Less than 3 arguments given ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED

        lookupUser = await self.__lookupUser(
            twitchChannelId = chatMessage.twitchChannelId,
            userName = splits[1],
        )

        if lookupUser is None:
            self.__twitchChatMessenger.send(
                text = f'⚠ Username and preferred name is necessary for this command. Example: !setpreferredname @{twitchHandle} John Smith',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Encountered invalid username argument ({lookupUser=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED
        elif not utils.isValidStr(lookupUser.userId):
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to find info for user \"{lookupUser.userName}\". A username and preferred name is necessary for this command. Example: !setpreferredname @{twitchHandle} John Smith',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'Encountered unknown username argument ({lookupUser=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.HANDLED

        oldPreferredNameData = await self.__chatterPreferredNameHelper.get(
            chatterUserId = lookupUser.userId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        try:
            newPreferredNameData = await self.__chatterPreferredNameHelper.set(
                chatterUserId = lookupUser.userId,
                preferredName = ' '.join(splits[2:]),
                twitchChannelId = chatMessage.twitchChannelId,
            )
        except ChatterPreferredNameFeatureIsDisabledException as e:
            self.__timber.log(self.commandName, f'This feature is currently disabled ({lookupUser=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.HANDLED
        except ChatterPreferredNameIsInvalidException as e:
            self.__twitchChatMessenger.send(
                text = f'⚠ The given preferred name for @{lookupUser.userName} is invalid',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            self.__timber.log(self.commandName, f'The given preferred name is invalid ({lookupUser=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.HANDLED

        oldPreferredNameSuffix = ''
        if oldPreferredNameData is not None:
            oldPreferredNameSuffix = f'(previously was {oldPreferredNameData.preferredName})'

        self.__twitchChatMessenger.send(
            text = f'ⓘ New preferred name set for @{lookupUser.userName} — {newPreferredNameData.preferredName} {oldPreferredNameSuffix}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Handled ({newPreferredNameData=}) ({oldPreferredNameData=}) ({lookupUser=}) ({chatMessage=})')
        return ChatCommandResult.HANDLED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        return isStreamer or isAdministrator

    async def __lookupUser(
        self,
        twitchChannelId: str,
        userName: str | None,
    ) -> LookupUserInfo | None:
        if not utils.isValidStr(userName):
            return None

        userName = utils.removePreceedingAt(userName)
        if not utils.strContainsAlphanumericCharacters(userName):
            return None

        userId = await self.__userIdsRepository.fetchUserId(
            userName = userName,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = twitchChannelId,
            ),
        )

        return SetChatterPreferredNameChatCommand.LookupUserInfo(
            userId = userId,
            userName = userName,
        )
