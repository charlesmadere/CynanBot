from dataclasses import dataclass
from typing import Final

from .absChatCommand import AbsChatCommand
from ..chatterPreferredTts.chatterPreferredTtsPresenter import ChatterPreferredTtsPresenter
from ..chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelperInterface import \
    ChatterPreferredTtsUserMessageHelperInterface
from ..chatterPreferredTts.models.chatterPrefferedTts import ChatterPreferredTts
from ..chatterPreferredTts.repository.chatterPreferredTtsRepositoryInterface import \
    ChatterPreferredTtsRepositoryInterface
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
        chatterPreferredTtsPresenter: ChatterPreferredTtsPresenter,
        chatterPreferredTtsRepository: ChatterPreferredTtsRepositoryInterface,
        chatterPreferredTtsSettingsRepository: ChatterPreferredTtsSettingsRepositoryInterface,
        chatterPreferredTtsUserMessageHelper: ChatterPreferredTtsUserMessageHelperInterface,
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
        elif not isinstance(chatterPreferredTtsPresenter, ChatterPreferredTtsPresenter):
            raise TypeError(f'chatterPreferredTtsPresenter argument is malformed: \"{chatterPreferredTtsPresenter}\"')
        elif not isinstance(chatterPreferredTtsRepository, ChatterPreferredTtsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsRepository argument is malformed: \"{chatterPreferredTtsRepository}\"')
        elif not isinstance(chatterPreferredTtsSettingsRepository, ChatterPreferredTtsSettingsRepositoryInterface):
            raise TypeError(f'chatterPreferredTtsSettingsRepository argument is malformed: \"{chatterPreferredTtsSettingsRepository}\"')
        elif not isinstance(chatterPreferredTtsUserMessageHelper, ChatterPreferredTtsUserMessageHelperInterface):
            raise TypeError(f'chatterPreferredTtsUserMessageHelper argument is malformed: \"{chatterPreferredTtsUserMessageHelper}\"')
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
        self.__chatterPreferredTtsPresenter: Final[ChatterPreferredTtsPresenter] = chatterPreferredTtsPresenter
        self.__chatterPreferredTtsRepository: Final[ChatterPreferredTtsRepositoryInterface] = chatterPreferredTtsRepository
        self.__chatterPreferredTtsSettingsRepository: Final[ChatterPreferredTtsSettingsRepositoryInterface] = chatterPreferredTtsSettingsRepository
        self.__chatterPreferredTtsUserMessageHelper: Final[ChatterPreferredTtsUserMessageHelperInterface] = chatterPreferredTtsUserMessageHelper
        self.__timber: Final[TimberInterface] = timber
        self.__ttsJsonMapper: Final[TtsJsonMapperInterface] = ttsJsonMapper
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensUtils: Final[TwitchTokensUtilsInterface] = twitchTokensUtils
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

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

        ttsProperties = await self.__chatterPreferredTtsUserMessageHelper.parseUserMessage(
            userMessage = ' '.join(splits[2:])
        )

        if ttsProperties is None:
            self.__timber.log('SetChatterPreferredTtsChatCommand', f'Failed to set preferred TTS properties given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle} ({lookupUser=}) ({ttsProperties=})')
            await self.__twitchUtils.safeSend(
                messageable = ctx,
                message = f'⚠ Unable to determine the preferred TTS properties for @{lookupUser.userName}! Please check your input and try again.',
                replyMessageId = await ctx.getMessageId()
            )
            return

        preferredTts = ChatterPreferredTts(
            properties = ttsProperties,
            chatterUserId = lookupUser.userId,
            twitchChannelId = await ctx.getTwitchChannelId()
        )

        await self.__chatterPreferredTtsRepository.set(
            preferredTts = preferredTts
        )

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
