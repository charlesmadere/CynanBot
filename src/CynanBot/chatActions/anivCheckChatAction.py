import traceback
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.chatActions.absChatAction import AbsChatAction
from CynanBot.contentScanner.aniv.anivContentCode import AnivContentCode
from CynanBot.contentScanner.aniv.anivContentScannerInterface import \
    AnivContentScannerInterface
from CynanBot.mostRecentChat.mostRecentChat import MostRecentChat
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.api.twitchApiServiceInterface import \
    TwitchApiServiceInterface
from CynanBot.twitch.configuration.twitchMessage import TwitchMessage
from CynanBot.twitch.twitchBanRequest import TwitchBanRequest
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface
from CynanBot.twitch.twitchTokensRepositoryInterface import \
    TwitchTokensRepositoryInterface
from CynanBot.twitch.twitchUtils import TwitchUtils
from CynanBot.users.userIdsRepositoryInterface import \
    UserIdsRepositoryInterface
from CynanBot.users.userInterface import UserInterface


class AnivCheckChatAction(AbsChatAction):

    def __init__(
        self,
        anivContentScanner: AnivContentScannerInterface,
        timber: TimberInterface,
        twitchApiService: TwitchApiServiceInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        twitchUtils: TwitchUtils,
        userIdsRepository: UserIdsRepositoryInterface,
        timeoutDurationSeconds: int = 60,
        anivUserId: str = '749050409'
    ):
        if not isinstance(anivContentScanner, AnivContentScannerInterface):
            raise ValueError(f'anivContentScanner argument is malformed: \"{anivContentScanner}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchApiService, TwitchApiServiceInterface):
            raise ValueError(f'twitchApiService argument is malformed: \"{twitchApiService}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise ValueError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise ValueError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidInt(timeoutDurationSeconds):
            raise ValueError(f'timeoutDurationSeconds argument is malformed: \"{timeoutDurationSeconds}\"')
        elif timeoutDurationSeconds < 1 or timeoutDurationSeconds > 1209600:
            raise ValueError(f'timeoutDurationSeconds argument is out of bounds: {timeoutDurationSeconds}')
        elif not utils.isValidStr(anivUserId):
            raise ValueError(f'anivUserId argument is malformed: \"{anivUserId}\"')

        self.__anivContentScanner: AnivContentScannerInterface = anivContentScanner
        self.__timber: TimberInterface = timber
        self.__twitchApiService: TwitchApiServiceInterface = twitchApiService
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchTokensRepository: TwitchTokensRepositoryInterface = twitchTokensRepository
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository
        self.__timeoutDurationSeconds: int = timeoutDurationSeconds
        self.__anivUserId: str = anivUserId

    async def handleChat(
        self,
        mostRecentChat: Optional[MostRecentChat],
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if message.getAuthorId() != self.__anivUserId:
            return False
        elif not user.isAnivContentScanningEnabled():
            return False

        contentCode = await self.__anivContentScanner.scan(message.getContent())
        if contentCode is AnivContentCode.OK:
            return False

        moderatorUserName = await self.__twitchHandleProvider.getTwitchHandle()
        if not await self.__twitchTokensRepository.hasAccessToken(moderatorUserName):
            self.__timber.log('AnivCheckChatAction', f'Attempted to timeout {message.getAuthorName()} (user ID \"{self.__anivUserId}\") for posting bad content (\"{message.getContent()}\") ({contentCode=}), but the bot user ({moderatorUserName}) does not have an available Twitch token')
            return False

        await self.__twitchTokensRepository.validateAndRefreshAccessToken(moderatorUserName)
        twitchToken = await self.__twitchTokensRepository.getAccessToken(moderatorUserName)

        if not utils.isValidStr(twitchToken):
            self.__timber.log('AnivCheckChatAction', f'Attempted to timeout {message.getAuthorName()} (user ID \"{self.__anivUserId}\") for posting bad content (\"{message.getContent()}\") ({contentCode=}), but was unable to fetch a valid Twitch token (\"{twitchToken}\") for the bot user ({moderatorUserName})')
            return False

        moderatorUserId = await self.__userIdsRepository.fetchUserId(
            userName = moderatorUserName,
            twitchAccessToken = twitchToken
        )

        if not utils.isValidStr(moderatorUserId):
            self.__timber.log('AnivCheckChatAction', f'Attempted to timeout {message.getAuthorName()} (user ID \"{self.__anivUserId}\") for posting bad content (\"{message.getContent()}\") ({contentCode=}), but was unable to fetch user ID for the bot user ({moderatorUserName})')
            return False

        channel = message.getChannel()

        banRequest = TwitchBanRequest(
            duration = self.__timeoutDurationSeconds,
            broadcasterUserId = await channel.getTwitchChannelId(),
            moderatorUserId = moderatorUserId,
            reason = f'{message.getAuthorName()} posted bad content',
            userIdToBan = self.__anivUserId
        )

        try:
            await self.__twitchApiService.banUser(
                twitchAccessToken = twitchToken,
                banRequest = banRequest
            )
        except Exception as e:
            self.__timber.log('AnivCheckChatAction', f'Failed to timeout {message.getAuthorName()}:{self.__anivUserId} for posting bad content (\"{message.getContent()}\") ({contentCode=})', e, traceback.format_exc())
            return False

        await self.__twitchUtils.safeSend(channel, f'ⓘ Timed out {message.getAuthorName()} for {self.__timeoutDurationSeconds} second(s) — {contentCode}')
        self.__timber.log('AnivCheckChatAction', f'Timed out {message.getAuthorName()}:{self.__anivUserId} for {self.__timeoutDurationSeconds} second(s) due to posting bad content (\"{message.getContent()}\") ({contentCode=})')

        return True
