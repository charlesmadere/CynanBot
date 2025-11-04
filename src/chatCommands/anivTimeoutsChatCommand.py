from typing import Final

from .absChatCommand import AbsChatCommand
from ..aniv.helpers.anivCopyMessageTimeoutScoreHelperInterface import AnivCopyMessageTimeoutScoreHelperInterface
from ..aniv.presenters.anivCopyMessageTimeoutScorePresenterInterface import \
    AnivCopyMessageTimeoutScorePresenterInterface
from ..aniv.settings.anivSettingsInterface import AnivSettingsInterface
from ..misc import utils as utils
from ..timber.timberInterface import TimberInterface
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class AnivTimeoutsChatCommand(AbsChatCommand):

    def __init__(
        self,
        anivCopyMessageTimeoutScoreHelper: AnivCopyMessageTimeoutScoreHelperInterface,
        anivCopyMessageTimeoutScorePresenter: AnivCopyMessageTimeoutScorePresenterInterface,
        anivSettings: AnivSettingsInterface,
        timber: TimberInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        usersRepository: UsersRepositoryInterface,
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
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__anivCopyMessageTimeoutScoreHelper: Final[AnivCopyMessageTimeoutScoreHelperInterface] = anivCopyMessageTimeoutScoreHelper
        self.__anivCopyMessageTimeoutScorePresenter: Final[AnivCopyMessageTimeoutScorePresenterInterface] = anivCopyMessageTimeoutScorePresenter
        self.__anivSettings: Final[AnivSettingsInterface] = anivSettings
        self.__timber: Final[TimberInterface] = timber
        self.__twitchChannelEditorsRepository: Final[TwitchChannelEditorsRepositoryInterface] = twitchChannelEditorsRepository
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__usersRepository: Final[UsersRepositoryInterface] = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        if not await self.__anivSettings.areCopyMessageTimeoutsEnabled():
            return

        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())

        if not user.isAnivMessageCopyTimeoutEnabled:
            return

        userId = ctx.getAuthorId()
        userName = ctx.getAuthorName()
        splits = utils.getCleanedSplits(ctx.getMessageContent())

        if len(splits) >= 2 and utils.strContainsAlphanumericCharacters(splits[1]):
            userName = utils.removePreceedingAt(splits[1])

        # this means that a user is querying for another user's timeout score
        if userName.casefold() != ctx.getAuthorName().casefold():
            userId = await self.__userIdsRepository.fetchUserId(userName = userName)

            if not utils.isValidStr(userId):
                self.__twitchChatMessenger.send(
                    text = f'⚠ Unable to find aniv timeout score for \"{userName}\"',
                    twitchChannelId = await ctx.getTwitchChannelId(),
                    replyMessageId = await ctx.getMessageId(),
                )
                return

        if await self.__twitchChannelEditorsRepository.isEditor(
            chatterUserId = userId,
            twitchChannelId =  await ctx.getTwitchChannelId(),
        ):
            printOut = await self.__anivCopyMessageTimeoutScorePresenter.getChannelEditorsCantPlayString(
                language = user.defaultLanguage,
            )

            self.__twitchChatMessenger.send(
                text = printOut,
                twitchChannelId = await ctx.getTwitchChannelId(),
                replyMessageId = await ctx.getMessageId(),
            )
            return

        preparedScore = await self.__anivCopyMessageTimeoutScoreHelper.getScore(
            chatterUserId = userId,
            twitchChannelId = await ctx.getTwitchChannelId(),
        )

        printOut = await self.__anivCopyMessageTimeoutScorePresenter.getScoreString(
            language = user.defaultLanguage,
            preparedScore = preparedScore,
        )

        self.__twitchChatMessenger.send(
            text = printOut,
            twitchChannelId = await ctx.getTwitchChannelId(),
            replyMessageId = await ctx.getMessageId(),
        )

        self.__timber.log('AnivTimeoutsChatCommand', f'Handled command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.handle}')
