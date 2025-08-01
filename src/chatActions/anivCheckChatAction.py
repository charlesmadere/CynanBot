import traceback
from typing import Final

from .absChatAction import AbsChatAction
from ..aniv.contentScanner.anivContentScannerInterface import AnivContentScannerInterface
from ..aniv.helpers.whichAnivUserHelperInterface import WhichAnivUserHelperInterface
from ..aniv.models.anivContentCode import AnivContentCode
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..twitch.api.models.twitchBanRequest import TwitchBanRequest
from ..twitch.api.twitchApiServiceInterface import TwitchApiServiceInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.timeout.twitchTimeoutHelperInterface import TwitchTimeoutHelperInterface
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface


class AnivCheckChatAction(AbsChatAction):

    def __init__(
        self,
        anivContentScanner: AnivContentScannerInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTimeoutHelper: TwitchTimeoutHelperInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        whichAnivUserHelper: WhichAnivUserHelperInterface,
        timeoutDurationSeconds: int = 30,
    ):
        if not isinstance(anivContentScanner, AnivContentScannerInterface):
            raise TypeError(f'anivContentScanner argument is malformed: \"{anivContentScanner}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise TypeError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTimeoutHelper, TwitchTimeoutHelperInterface):
            raise TypeError(f'twitchTimeoutHelper argument is malformed: \"{twitchTimeoutHelper}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not isinstance(whichAnivUserHelper, WhichAnivUserHelperInterface):
            raise TypeError(f'whichAnivUserHelper argument is malformed: \"{whichAnivUserHelper}\"')
        elif not utils.isValidInt(timeoutDurationSeconds):
            raise TypeError(f'timeoutDurationSeconds argument is malformed: \"{timeoutDurationSeconds}\"')
        elif timeoutDurationSeconds < 1 or timeoutDurationSeconds > 1209600:
            raise ValueError(f'timeoutDurationSeconds argument is out of bounds: {timeoutDurationSeconds}')

        self.__anivContentScanner: Final[AnivContentScannerInterface] = anivContentScanner
        self.__timber: Final[TimberInterface] = timber
        self.__twitchApiService: Final[TwitchApiServiceInterface] = twitchApiService
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTimeoutHelper: Final[TwitchTimeoutHelperInterface] = twitchTimeoutHelper
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__twitchUtils: Final[TwitchUtilsInterface] = twitchUtils
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__whichAnivUserHelper: Final[WhichAnivUserHelperInterface] = whichAnivUserHelper
        self.__timeoutDurationSeconds: Final[int] = timeoutDurationSeconds

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface,
    ) -> bool:
        if not user.isAnivContentScanningEnabled:
            return False

        anivUser = await self.__whichAnivUserHelper.getAnivUser(
            twitchChannelId = await message.getTwitchChannelId(),
            whichAnivUser = user.whichAnivUser,
        )

        if anivUser is None or anivUser.userId != message.getAuthorId():
            return False

        contentCode = await self.__anivContentScanner.scan(message.getContent())
        if contentCode is AnivContentCode.OK:
            return False

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        twitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)

        if not utils.isValidStr(twitchAccessToken):
            self.__timber.log('AnivCheckChatAction', f'Attempted to timeout {message.getAuthorName()} ({anivUser=}) for posting bad content (\"{message.getContent()}\") ({contentCode=}), but was unable to fetch a valid Twitch access token ({twitchAccessToken=}) for the bot user ({twitchHandle=})')
            return False

        twitchId = await self.__userIdsRepository.requireUserId(
            userName = twitchHandle,
            twitchAccessToken = twitchAccessToken,
        )

        banRequest = TwitchBanRequest(
            duration = self.__timeoutDurationSeconds,
            broadcasterUserId = await message.getTwitchChannelId(),
            moderatorUserId = twitchId,
            reason = f'{message.getAuthorName()} posted bad content ({contentCode})',
            userIdToBan = anivUser.userId,
        )

        try:
            await self.__twitchApiService.banUser(
                twitchAccessToken = twitchAccessToken,
                banRequest = banRequest,
            )
        except Exception as e:
            self.__timber.log('AnivCheckChatAction', f'Failed to timeout {message.getAuthorName()} ({anivUser=}) for posting bad content (\"{message.getContent()}\") ({contentCode=})', e, traceback.format_exc())
            return False

        await self.__twitchUtils.safeSend(
            messageable = message.getChannel(),
            message = f'ⓘ Timed out {message.getAuthorName()} for {self.__timeoutDurationSeconds} second(s) — {contentCode}',
        )

        self.__timber.log('AnivCheckChatAction', f'Timed out {message.getAuthorName()} ({anivUser=}) for {self.__timeoutDurationSeconds} second(s) due to posting bad content (\"{message.getContent()}\") ({contentCode=})')

        return True
