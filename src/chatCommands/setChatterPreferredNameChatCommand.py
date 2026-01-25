import traceback
from dataclasses import dataclass
from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterPreferredName.exceptions import ChatterPreferredNameFeatureIsDisabledException, \
    ChatterPreferredNameIsInvalidException
from ..chatterPreferredName.helpers.chatterPreferredNameHelperInterface import ChatterPreferredNameHelperInterface
from ..chatterPreferredName.settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class SetChatterPreferredNameChatCommand(AbsChatCommand):

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
        usersRepository: UsersRepositoryInterface,
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
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__chatterPreferredNameHelper: Final[ChatterPreferredNameHelperInterface] = chatterPreferredNameHelper
        self.__chatterPreferredNameSettings: Final[ChatterPreferredNameSettingsInterface] = chatterPreferredNameSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        if not await self.__chatterPreferredNameSettings.isEnabled():
            return

        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.isChatterPreferredNameEnabled:
            return

        twitchChannelId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if twitchChannelId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('SetChatterPreferredNameChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 3:
            self.__timber.log('SetChatterPreferredNameChatCommand', f'Less than 3 arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

            self.__twitchChatMessenger.send(
                text = f'⚠ Username and preferred name is necessary for this command. Example: !setpreferredname {twitchHandle} example',
                twitchChannelId = twitchChannelId,
                replyMessageId = await ctx.getMessageId(),
            )
            return

        lookupUser = await self.__lookupUser(
            twitchChannelId = twitchChannelId,
            userName = splits[1],
        )

        if lookupUser is None:
            self.__timber.log('SetChatterPreferredNameChatCommand', f'Invalid user name argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            self.__twitchChatMessenger.send(
                text = f'⚠ Username and preferred name is necessary for this command. Example: !setpreferredname {twitchHandle} John Smith',
                twitchChannelId = twitchChannelId,
                replyMessageId = await ctx.getMessageId(),
            )
            return
        elif not utils.isValidStr(lookupUser.userId):
            self.__timber.log('SetChatterPreferredNameChatCommand', f'Unknown user name argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to find info for user \"{lookupUser.userName}\". A username and preferred name is necessary for this command. Example: !setpreferredname {twitchHandle} John Smith',
                twitchChannelId = twitchChannelId,
                replyMessageId = await ctx.getMessageId(),
            )
            return

        oldPreferredNameData = await self.__chatterPreferredNameHelper.get(
            chatterUserId = lookupUser.userId,
            twitchChannelId = twitchChannelId,
        )

        try:
            newPreferredNameData = await self.__chatterPreferredNameHelper.set(
                chatterUserId = lookupUser.userId,
                preferredName = ' '.join(splits[2:]),
                twitchChannelId = twitchChannelId,
            )
        except ChatterPreferredNameFeatureIsDisabledException as e:
            self.__timber.log('SetChatterPreferredNameChatCommand', f'This feature is disabled when handling command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}', e, traceback.format_exc())
            return
        except ChatterPreferredNameIsInvalidException as e:
            self.__timber.log('SetChatterPreferredNameChatCommand', f'The given preferred name is invalid when handling command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}', e, traceback.format_exc())
            self.__twitchChatMessenger.send(
                text = f'⚠ The given preferred name for @{lookupUser.userName} is invalid',
                twitchChannelId = twitchChannelId,
                replyMessageId = await ctx.getMessageId(),
            )
            return

        oldPreferredNameSuffix = ''
        if oldPreferredNameData is not None:
            oldPreferredNameSuffix = f'(previously was {oldPreferredNameData.preferredName})'

        self.__twitchChatMessenger.send(
            text = f'ⓘ New preferred name set for @{lookupUser.userName} — {newPreferredNameData.preferredName} {oldPreferredNameSuffix}',
            twitchChannelId = twitchChannelId,
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('SetChatterPreferredNameChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

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
