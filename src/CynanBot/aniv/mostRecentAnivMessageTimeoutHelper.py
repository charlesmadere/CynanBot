import traceback

import CynanBot.misc.utils as utils
from CynanBot.aniv.anivUserIdProviderInterface import \
    AnivUserIdProviderInterface
from CynanBot.aniv.mostRecentAnivMessageRepositoryInterface import \
    MostRecentAnivMessageRepositoryInterface
from CynanBot.aniv.mostRecentAnivMessageTimeoutHelperInterface import \
    MostRecentAnivMessageTimeoutHelperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.api.twitchModUser import TwitchModUser
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class MostRecentAnivMessageTimeoutHelper(MostRecentAnivMessageTimeoutHelperInterface):

    def __init__(
        self,
        anivUserIdProvider: AnivUserIdProviderInterface,
        mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        timeoutProbability: float = 0.5
    ):
        if not isinstance(anivUserIdProvider, AnivUserIdProviderInterface):
            raise TypeError(f'anivUserIdProvider argument is malformed: \"{anivUserIdProvider}\"')
        elif not isinstance(mostRecentAnivMessageRepository, MostRecentAnivMessageRepositoryInterface):
            raise TypeError(f'mostRecentAnivMessageRepository argument is malformed: \"{mostRecentAnivMessageRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not utils.isValidNum(timeoutProbability):
            raise TypeError(f'timeoutProbability argument is malformed: \"{timeoutProbability}\"')

        self.__anivUserIdProvider: AnivUserIdProviderInterface = anivUserIdProvider
        self.__mostRecentAnivMessageRepository: MostRecentAnivMessageRepositoryInterface = mostRecentAnivMessageRepository
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__timeoutProbability: float = timeoutProbability

    async def checkMessageAndMaybeTimeout(
        self,
        chatterUserId: str,
        chatterUserName: str,
        message: str | None,
        twitchChannelId: str,
        user: UserInterface
    ):
        if not user.isAnivMessageCopyTimeoutEnabled():
            return

        anivUserId = await self.__anivUserIdProvider.getAnivUserId()

        if not utils.isValidStr(anivUserId) or anivUserId == chatterUserId:
            return

        anivMessage = await self.__mostRecentAnivMessageRepository.get(
            twitchChannelId = twitchChannelId
        )

        if not utils.isValidStr(anivMessage):
            return

        # TODO
        pass

    async def __isMod(
        self,
        broadcasterUserId: str,
        twitchAccessToken: str,
        userIdToTimeout: str
    ) -> bool:
        if not utils.isValidStr(broadcasterUserId):
            raise TypeError(f'broadcasterUserId argument is malformed: \"{broadcasterUserId}\"')
        elif not utils.isValidStr(twitchAccessToken):
            raise TypeError(f'twitchAccessToken argument is malformed: \"{twitchAccessToken}\"')
        elif not utils.isValidStr(userIdToTimeout):
            raise TypeError(f'userIdToTimeout argument is malformed: \"{userIdToTimeout}\"')

        moderatorInfo: TwitchModUser | None = None

        try:
            moderatorInfo = await self.__twitchApiService.fetchModerator(
                broadcasterId = broadcasterUserId,
                twitchAccessToken = twitchAccessToken,
                userId = userIdToTimeout
            )
        except Exception as e:
            self.__timber.log('MostRecentAnivMessageTimeoutHelper', f'Failed to fetch Twitch moderator info ({broadcasterUserId=}) ({userIdToTimeout=}): {e}', e, traceback.format_exc())

        return moderatorInfo is not None
