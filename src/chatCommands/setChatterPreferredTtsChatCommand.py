import re
import traceback
from dataclasses import dataclass
from typing import Final, Pattern

from .absChatCommand import AbsChatCommand
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.exceptions import FailedToChooseRandomTtsException, NoEnabledTtsProvidersException, \
    TtsProviderIsNotEnabledException, UnableToParseUserMessageIntoTtsException
from ..chatterPreferredTts.helper.chatterPreferredTtsHelperInterface import ChatterPreferredTtsHelperInterface
from ..chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from ..chatterPreferredTts.settings.chatterPreferredTtsSettingsRepositoryInterface import \
    ChatterPreferredTtsSettingsRepositoryInterface
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..tts.jsonMapper.ttsJsonMapperInterface import TtsJsonMapperInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.tokens.twitchTokensUtilsInterface import TwitchTokensUtilsInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class SetChatterPreferredTtsChatCommand(AbsChatCommand):

    @dataclass(frozen = True)
    class LookupUserInfo:
        userId: str | None
        userName: str

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        chatterPreferredTtsHelper: ChatterPreferredTtsHelperInterface,
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        timber: TimberInterface,
        ttsJsonMapper: TtsJsonMapperInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensUtils: TwitchTokensUtilsInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(chatterPreferredTtsHelper, ChatterPreferredTtsHelperInterface):
            raise TypeError(f'chatterPreferredTtsHelper argument is malformed: \"{chatterPreferredTtsHelper}\"')
        elif not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsJsonMapper, TtsJsonMapperInterface):
            raise TypeError(f'ttsJsonMapper argument is malformed: \"{ttsJsonMapper}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensUtils, TwitchTokensUtilsInterface):
            raise TypeError(f'twitchTokensUtils argument is malformed: \"{twitchTokensUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__chatterPreferredTtsHelper: Final[ChatterPreferredTtsHelperInterface] = chatterPreferredTtsHelper
        self.__chatterPreferredTtsPresenter: Final[ChatterPreferredTtsPresenter] = chatterPreferredTtsPresenter
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

        self.__randomRegEx: Final[Pattern] = re.compile(r'^\s*random\s*$', re.IGNORECASE)

    async def __getExampleTtsProvider(self, user: UserInterface) -> str:
        return await self.__ttsJsonMapper.asyncSerializeProvider(
            ttsProvider = user.defaultTtsProvider
        )

    async def handleChatCommand(self, ctx: TwitchContext):
        if not await self.__chatterPreferredTtsSettingsRepository.isEnabled():
            return

        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        if not user.isChatterPreferredTtsEnabled:
            return

        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('SetChatterPreferredTtsChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} tried using this command!')
            return

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        exampleTtsProvider = await self.__getExampleTtsProvider(user)

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 3:
            self.__timber.log('SetChatterPreferredTtsChatCommand', f'Less than 2 arguments given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Username and preferred TTS voice is necessary for this command. Example: !setpreferredtts {twitchHandle} {exampleTtsProvider}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        lookupUser = await self.__lookupUser(
            twitchChannelId = await ctx.getTwitchChannelId(),
            userName = splits[1]
        )

        if lookupUser is None:
            self.__timber.log('SetChatterPreferredTtsChatCommand', f'Invalid user name argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Username and preferred TTS voice is necessary for this command. Example: !setpreferredtts {twitchHandle} {exampleTtsProvider}',
                replyMessageId = await ctx.getMessageId()
            )
            return
        elif not utils.isValidStr(lookupUser.userId):
            self.__timber.log('SetChatterPreferredTtsChatCommand', f'Unknown user name argument given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to find info for user \"{lookupUser.userName}\". A username and preferred TTS voice is necessary for this command. Example: !setpreferredtts {twitchHandle} {exampleTtsProvider}',
                replyMessageId = await ctx.getMessageId()
            )
            return

        userMessage = ' '.join(splits[2:])
        preferredTts: ChatterPreferredTts

        try:
            if self.__randomRegEx.fullmatch(userMessage):
                preferredTts = await self.__chatterPreferredTtsHelper.applyRandomPreferredTts(
                    chatterUserId = lookupUser.userId,
                    twitchChannelId = await ctx.getTwitchChannelId()
                )
            else:
                preferredTts = await self.__chatterPreferredTtsHelper.applyUserMessagePreferredTts(
                    chatterUserId = lookupUser.userId,
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    userMessage = userMessage
                )
        except (FailedToChooseRandomTtsException, NoEnabledTtsProvidersException, TtsProviderIsNotEnabledException, UnableToParseUserMessageIntoTtsException) as e:
            self.__timber.log('SetChatterPreferredTtsChatCommand', f'Failed to set preferred TTS given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({lookupUser=}) ({userMessage=}): {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to set preferred TTS for @{lookupUser.userName}! Please check your input and try again.',
                replyMessageId = await ctx.getMessageId()
            )
            return

        printOut = await self.__chatterPreferredTtsPresenter.printOut(preferredTts)
        await self.__twitchUtils.safeSend(ctx, f'ⓘ New preferred TTS set for @{lookupUser.userName} — {printOut}')
        self.__timber.log('SetChatterPreferredTtsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')

    async def __lookupUser(
        self,
        twitchChannelId: str,
        userName: str | None
    ) -> LookupUserInfo | None:
        if not utils.isValidStr(userName):
            return None

        userName = utils.removePreceedingAt(userName)

        if not utils.strContainsAlphanumericCharacters(userName):
            return None

        userId = await self.__userIdsRepository.fetchUserId(
            userName = userName,
            twitchAccessToken = await self.__twitchTokensUtils.getAccessTokenByIdOrFallback(
                twitchChannelId = twitchChannelId
            )
        )

        return SetChatterPreferredTtsChatCommand.LookupUserInfo(
            userId = userId,
            userName = userName
        )
