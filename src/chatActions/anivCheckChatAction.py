import traceback

from .absChatAction import AbsChatAction
from ..aniv.anivContentCode import AnivContentCode
from ..aniv.anivContentScannerInterface import AnivContentScannerInterface
from ..aniv.anivUserIdProviderInterface import AnivUserIdProviderInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..twitch.api.twitchBanRequest import TwitchBanRequest
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface


class AnivCheckChatAction(AbsChatAction):

    def __init__(
        self,
        anivContentScanner: AnivContentScannerInterface,
        anivUserIdProvider: AnivUserIdProviderInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        timeoutDurationSeconds: int = 60
    ):
        if not isinstance(anivContentScanner, AnivContentScannerInterface):
            raise TypeError(f'anivContentScanner argument is malformed: \"{anivContentScanner}\"')
        elif not isinstance(anivUserIdProvider, AnivUserIdProviderInterface):
            raise TypeError(f'anivUserIdProvider argument is malformed: \"{anivUserIdProvider}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidInt(timeoutDurationSeconds):
            raise TypeError(f'timeoutDurationSeconds argument is malformed: \"{timeoutDurationSeconds}\"')
        elif timeoutDurationSeconds < 1 or timeoutDurationSeconds > 1209600:
            raise ValueError(f'timeoutDurationSeconds argument is out of bounds: {timeoutDurationSeconds}')

        self.__anivContentScanner: AnivContentScannerInterface = anivContentScanner
        self.__anivUserIdProvider: AnivUserIdProviderInterface = anivUserIdProvider
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__timeoutDurationSeconds: int = timeoutDurationSeconds

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        anivUserId = await self.__anivUserIdProvider.getAnivUserId()

        if not utils.isValidStr(anivUserId):
            return False
        if message.getAuthorId() != anivUserId:
            return False
        elif not user.isAnivContentScanningEnabled:
            return False

        contentCode = await self.__anivContentScanner.scan(message.getContent())
        if contentCode is AnivContentCode.OK:
            return False

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)

        if not utils.isValidStr(twitchAccessToken):
            self.__timber.log('AnivCheckChatAction', f'Attempted to timeout {message.getAuthorName()} (user ID \"{anivUserId}\") for posting bad content (\"{message.getContent()}\") ({contentCode=}), but was unable to fetch a valid Twitch access token (\"{twitchAccessToken}\") for the bot user ({twitchHandle})')
            return False

        twitchId = await self.__userIdsRepository.fetchUserId(
            userName = twitchHandle,
            twitchAccessToken = twitchAccessToken
        )

        if not utils.isValidStr(twitchId):
            self.__timber.log('AnivCheckChatAction', f'Attempted to timeout {message.getAuthorName()} (user ID \"{anivUserId}\") for posting bad content (\"{message.getContent()}\") ({contentCode=}), but was unable to fetch a valid user ID for the bot user ({twitchHandle})')
            return False

        channel = message.getChannel()

        banRequest = TwitchBanRequest(
            duration = self.__timeoutDurationSeconds,
            broadcasterUserId = await channel.getTwitchChannelId(),
            moderatorUserId = twitchId,
            reason = f'{message.getAuthorName()} posted bad content ({contentCode})',
            userIdToBan = anivUserId
        )

        try:
            await self.__twitchApiService.banUser(
                twitchAccessToken = twitchAccessToken,
                banRequest = banRequest
            )
        except Exception as e:
            self.__timber.log('AnivCheckChatAction', f'Failed to timeout {message.getAuthorName()}:{anivUserId} for posting bad content (\"{message.getContent()}\") ({contentCode=})', e, traceback.format_exc())
            return False

        await self.__twitchUtils.safeSend(channel, f'ⓘ Timed out {message.getAuthorName()} for {self.__timeoutDurationSeconds} second(s) — {contentCode}')
        self.__timber.log('AnivCheckChatAction', f'Timed out {message.getAuthorName()}:{anivUserId} for {self.__timeoutDurationSeconds} second(s) due to posting bad content (\"{message.getContent()}\") ({contentCode=})')

        return True
