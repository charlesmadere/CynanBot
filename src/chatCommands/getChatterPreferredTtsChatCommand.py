import traceback
from dataclasses import dataclass
from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from ..chatterPreferredTts.repository.chatterPreferredTtsRepositoryInterface import \
    ChatterPreferredTtsRepositoryInterface
from ..chatterPreferredTts.settings.chatterPreferredTtsSettingsRepositoryInterface import \
    ChatterPreferredTtsSettingsRepositoryInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.exceptions import NoSuchUserException
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class GetChatterPreferredTtsChatCommand(AbsChatCommand):

    @dataclass(frozen = True)
    class PreferredTtsLookupData:
        preferredTts: ChatterPreferredTts | None
        chatterUserId: str
        chatterUserName: str

    def __init__(
        self,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        timber: TimberInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__chatterPreferredTtsPresenter: Final[ChatterPreferredTtsPresenter] = chatterPreferredTtsPresenter
        self.__chatterPreferredTtsRepository: Final[ChatterPreferredTtsRepositoryInterface] = chatterPreferredTtsRepository
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        if not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return

        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.isChatterPreferredTtsEnabled:
            return

        messageContent = utils.cleanStr(ctx.getMessageContent())

        try:
            preferredTtsLookupData = await self.__lookupPreferredTts(
                messageContent = messageContent,
                chatterUserId = ctx.getAuthorId(),
                chatterUserName = ctx.getAuthorName(),
                twitchChannelId = await ctx.getTwitchChannelId()
            )
        except NoSuchUserException as e:
            self.__timber.log('GetChatterPreferredTtsChatCommand', f'Failed to find user ID information for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({messageContent=}): {e}', e, traceback.format_exc())

            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Failed to find preferred TTS info for the given user',
                replyMessageId = await ctx.getMessageId()
            )

            return

        await self.__twitchUtils.safeSend(
            messageable = ctx,
            message = await self.__toString(
                preferredTtsLookupData = preferredTtsLookupData,
                chatterUserId = ctx.getAuthorId(),
            ),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('GetChatterPreferredTtsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __lookupPreferredTts(
        self,
        messageContent: str | None,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str
    ) -> PreferredTtsLookupData:
        splits = utils.getCleanedSplits(messageContent)
        lookupUserName: str
        lookupUserId: str

        if len(splits) >= 2:
            lookupUserName = utils.removePreceedingAt(splits[1])

            lookupUserId = await self.__userIdsRepository.requireUserId(
                userName = lookupUserName,
                twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                    twitchChannelId = twitchChannelId
                )
            )
        else:
            lookupUserName = chatterUserName
            lookupUserId = chatterUserId

        preferredTts = await self.__chatterPreferredTtsRepository.get(
            chatterUserId = lookupUserId,
            twitchChannelId = twitchChannelId
        )

        return GetChatterPreferredTtsChatCommand.PreferredTtsLookupData(
            preferredTts = preferredTts,
            chatterUserId = lookupUserId,
            chatterUserName = lookupUserName
        )

    async def __toString(
        self,
        preferredTtsLookupData: PreferredTtsLookupData,
        chatterUserId: str,
    ) -> str:
        printOut: str

        if preferredTtsLookupData.preferredTts is None:
            printOut = ''
        else:
            printOut = await self.__chatterPreferredTtsPresenter.printOut(
                preferredTts = preferredTtsLookupData.preferredTts
            )

        if preferredTtsLookupData.chatterUserId == chatterUserId:
            if preferredTtsLookupData.preferredTts is None:
                return f'ⓘ You currently don\'t have a preferred TTS'
            else:
                return f'ⓘ Your preferred TTS: {printOut}'
        elif preferredTtsLookupData.preferredTts is None:
            return f'ⓘ @{preferredTtsLookupData.chatterUserName} doesn\'t have a preferred TTS'
        else:
            return f'ⓘ Preferred TTS for @{preferredTtsLookupData.chatterUserName}: {printOut}'
