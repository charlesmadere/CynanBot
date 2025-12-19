from dataclasses import dataclass
from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterPreferredName.repositories.chatterPreferredNameRepositoryInterface import \
    ChatterPreferredNameRepositoryInterface
from ..chatterPreferredName.settings.chatterPreferredNameSettingsInterface import ChatterPreferredNameSettingsInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class RemoveChatterPreferredNameChatCommand(AbsChatCommand):

    @dataclass(frozen = True)
    class LookupUserInfo:
        userId: str | None
        userName: str

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        chatterPreferredNameRepository: ChatterPreferredNameRepositoryInterface,
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
        elif not isinstance(chatterPreferredNameRepository, ChatterPreferredNameRepositoryInterface):
            raise TypeError(f'chatterPreferredNameRepository argument is malformed: \"{chatterPreferredNameRepository}\"')
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
        self.__chatterPreferredNameRepository: Final[ChatterPreferredNameRepositoryInterface] = chatterPreferredNameRepository
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
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('RemoveChatterPreferredNameChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            self.__timber.log('RemoveChatterPreferredNameChatCommand', f'No arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

            self.__twitchChatMessenger.send(
                text = f'⚠ Username is necessary for this command. Example: !removepreferredname {twitchHandle}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        lookupUser = await self.__lookupUser(
            twitchChannelId = await ctx.getTwitchChannelId(),
            userName = splits[1],
        )

        if lookupUser is None:
            self.__timber.log('RemoveChatterPreferredNameChatCommand', f'Invalid user name argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            self.__twitchChatMessenger.send(
                text = f'⚠ Username is necessary for this command. Example: !removepreferredname {twitchHandle}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return
        elif not utils.isValidStr(lookupUser.userId):
            self.__timber.log('RemoveChatterPreferredNameChatCommand', f'Unknown user name argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            self.__twitchChatMessenger.send(
                text = f'⚠ Unable to find info for user \"{lookupUser.userName}\". Example: !removepreferredname {twitchHandle}',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        oldPreferredNameData = await self.__chatterPreferredNameRepository.remove(
            chatterUserId = lookupUser.userId,
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        if oldPreferredNameData is None:
            self.__twitchChatMessenger.send(
                text = f'ⓘ @{lookupUser.userName} has no preferred name',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
        else:
            self.__twitchChatMessenger.send(
                text = f'ⓘ Removed preferred name for @{lookupUser.userName} (previously was {oldPreferredNameData.preferredName})',
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )

        self.__timber.log('RemoveChatterPreferredNameChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

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

        return RemoveChatterPreferredNameChatCommand.LookupUserInfo(
            userId = userId,
            userName = userName,
        )
