from typing import Final

from .absChatAction import AbsChatAction
from ..aniv.contentScanner.anivContentScannerInterface import AnivContentScannerInterface
from ..aniv.models.anivContentCode import AnivContentCode
from ..aniv.repositories.anivUserIdsRepositoryInterface import AnivUserIdsRepositoryInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..timber.timberInterface import TimberInterface
from ..timeout.idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ..timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from ..timeout.models.absTimeoutDuration import AbsTimeoutDuration
from ..timeout.models.actions.basicTimeoutAction import BasicTimeoutAction
from ..timeout.models.exactTimeoutDuration import ExactTimeoutDuration
from ..timeout.models.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..twitch.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface


class AnivCheckChatAction(AbsChatAction):

    def __init__(
        self,
        anivContentScanner: AnivContentScannerInterface,
        anivUserIdsRepository: AnivUserIdsRepositoryInterface,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
        timeoutDurationSeconds: int = 30,
    ):
        if not isinstance(anivContentScanner, AnivContentScannerInterface):
            raise TypeError(f'anivContentScanner argument is malformed: \"{anivContentScanner}\"')
        elif not isinstance(anivUserIdsRepository, AnivUserIdsRepositoryInterface):
            raise TypeError(f'anivUserIdsRepository argument is malformed: \"{anivUserIdsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif not isinstance(timeoutIdGenerator, TimeoutIdGeneratorInterface):
            raise TypeError(f'timeoutIdGenerator argument is malformed: \"{timeoutIdGenerator}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')
        elif not utils.isValidInt(timeoutDurationSeconds):
            raise TypeError(f'timeoutDurationSeconds argument is malformed: \"{timeoutDurationSeconds}\"')
        elif timeoutDurationSeconds < 1 or timeoutDurationSeconds > 1209600:
            raise ValueError(f'timeoutDurationSeconds argument is out of bounds: {timeoutDurationSeconds}')

        self.__anivContentScanner: Final[AnivContentScannerInterface] = anivContentScanner
        self.__anivUserIdsRepository: Final[AnivUserIdsRepositoryInterface] = anivUserIdsRepository
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository
        self.__timeoutDurationSeconds: Final[int] = timeoutDurationSeconds

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface,
    ) -> bool:
        if not user.isAnivContentScanningEnabled:
            return False
        elif message.getAuthorId() == await message.getTwitchChannelId():
            return False

        whichAnivUser = await self.__anivUserIdsRepository.determineAnivUser(
            chatterUserId = message.getAuthorId(),
        )

        if whichAnivUser is None:
            return False

        contentCode = await self.__anivContentScanner.scan(message.getContent())
        if contentCode is AnivContentCode.OK:
            return False

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        moderatorTwitchAccessToken = await self.__twitchTokensRepository.getAccessToken(twitchHandle)

        if not utils.isValidStr(moderatorTwitchAccessToken):
            self.__timber.log('AnivCheckChatAction', f'Attempted to timeout {message.getAuthorName()} ({whichAnivUser=}) for posting bad content (\"{message.getContent()}\") ({contentCode=}), but was unable to fetch a valid Twitch access token ({moderatorTwitchAccessToken=}) for the bot user ({twitchHandle=})')
            return False

        userTwitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = await message.getTwitchChannelId(),
        )

        if not utils.isValidStr(userTwitchAccessToken):
            self.__timber.log('AnivCheckChatAction', f'Attempted to timeout {message.getAuthorName()} ({whichAnivUser=}) for posting bad content (\"{message.getContent()}\") ({contentCode=}), but was unable to fetch a valid Twitch access token ({userTwitchAccessToken=}) for this Twitch channel ({user=})')
            return False

        moderatorUserId = await self.__userIdsRepository.requireUserId(
            userName = twitchHandle,
            twitchAccessToken = moderatorTwitchAccessToken,
        )

        timeoutDuration: AbsTimeoutDuration = ExactTimeoutDuration(
            seconds = self.__timeoutDurationSeconds,
        )

        self.__timeoutActionMachine.submitAction(BasicTimeoutAction(
            timeoutDuration = timeoutDuration,
            actionId = await self.__timeoutIdGenerator.generateActionId(),
            chatMessage = f'ⓘ Briefly timed out @{message.getAuthorName()} — {contentCode}',
            instigatorUserId = moderatorUserId,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            reason = f'Timed out for content code {contentCode}',
            targetUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId(),
            twitchChatMessageId = None,
            userTwitchAccessToken = userTwitchAccessToken,
            streamStatusRequirement = TimeoutStreamStatusRequirement.ANY,
            user = user,
        ))

        self.__timber.log('AnivCheckChatAction', f'Timed out {message.getAuthorName()} ({whichAnivUser=}) for {self.__timeoutDurationSeconds} second(s) due to posting bad content (\"{message.getContent()}\") ({contentCode=})')

        return True
