import re
import traceback
from typing import Collection, Final, Pattern

from .absChatCommand import AbsChatCommand
from .chatCommandResult import ChatCommandResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..soundPlayerManager.soundAlert import SoundAlert
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..timber.timberInterface import TimberInterface
from ..timeout.idGenerator.timeoutIdGeneratorInterface import TimeoutIdGeneratorInterface
from ..timeout.machine.timeoutActionMachineInterface import TimeoutActionMachineInterface
from ..timeout.models.actions.basicTimeoutAction import BasicTimeoutAction
from ..timeout.models.exactTimeoutDuration import ExactTimeoutDuration
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..twitch.channelEditors.twitchChannelEditorsRepositoryInterface import TwitchChannelEditorsRepositoryInterface
from ..twitch.channelInformationHelper.exceptions import RequiredTwitchAuthorizationIsMissingException
from ..twitch.channelInformationHelper.twitchChannelInformationHelperInterface import \
    TwitchChannelInformationHelperInterface
from ..twitch.chatMessenger.twitchChatMessengerInterface import TwitchChatMessengerInterface
from ..twitch.exceptions import TwitchStatusCodeException
from ..twitch.friends.twitchFriendsUserIdRepositoryInterface import TwitchFriendsUserIdRepositoryInterface
from ..twitch.handleProvider.twitchHandleProviderInterface import TwitchHandleProviderInterface
from ..twitch.localModels.twitchChatMessage import TwitchChatMessage
from ..twitch.moderator.twitchModeratorHelperInterface import TwitchModeratorHelperInterface
from ..twitch.tokens.twitchTokensRepositoryInterface import TwitchTokensRepositoryInterface
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface
from ..users.userInterface import UserInterface


class UpdateStreamTitleChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        timber: TimberInterface,
        timeoutActionMachine: TimeoutActionMachineInterface,
        timeoutIdGenerator: TimeoutIdGeneratorInterface,
        twitchChannelEditorsRepository: TwitchChannelEditorsRepositoryInterface,
        twitchChannelInformationHelper: TwitchChannelInformationHelperInterface,
        twitchChatMessenger: TwitchChatMessengerInterface,
        twitchFriendsUserIdRepository: TwitchFriendsUserIdRepositoryInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchModeratorHelper: TwitchModeratorHelperInterface,
        twitchTokensRepository: TwitchTokensRepositoryInterface,
        userIdsRepository: UserIdsRepositoryInterface,
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeoutActionMachine, TimeoutActionMachineInterface):
            raise TypeError(f'timeoutActionMachine argument is malformed: \"{timeoutActionMachine}\"')
        elif not isinstance(timeoutIdGenerator, TimeoutIdGeneratorInterface):
            raise TypeError(f'timeoutIdGenerator argument is malformed: \"{timeoutIdGenerator}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchChannelEditorsRepository, TwitchChannelEditorsRepositoryInterface):
            raise TypeError(f'twitchChannelEditorsRepository argument is malformed: \"{twitchChannelEditorsRepository}\"')
        elif not isinstance(twitchChannelInformationHelper, TwitchChannelInformationHelperInterface):
            raise TypeError(f'twitchChannelInformationHelper argument is malformed: \"{twitchChannelInformationHelper}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessengerInterface):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')
        elif not isinstance(twitchFriendsUserIdRepository, TwitchFriendsUserIdRepositoryInterface):
            raise TypeError(f'twitchFriendsUserIdRepository argument is malformed: \"{twitchFriendsUserIdRepository}\"')
        elif not isinstance(twitchHandleProvider, TwitchHandleProviderInterface):
            raise TypeError(f'twitchHandleProvider argument is malformed: \"{twitchHandleProvider}\"')
        elif not isinstance(twitchModeratorHelper, TwitchModeratorHelperInterface):
            raise TypeError(f'twitchModeratorHelper argument is malformed: \"{twitchModeratorHelper}\"')
        elif not isinstance(twitchTokensRepository, TwitchTokensRepositoryInterface):
            raise TypeError(f'twitchTokensRepository argument is malformed: \"{twitchTokensRepository}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__administratorProvider: Final[AdministratorProviderInterface] = administratorProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__timber: Final[TimberInterface] = timber
        self.__timeoutActionMachine: Final[TimeoutActionMachineInterface] = timeoutActionMachine
        self.__timeoutIdGenerator: Final[TimeoutIdGeneratorInterface] = timeoutIdGenerator
        self.__twitchChannelEditorsRepository: Final[TwitchChannelEditorsRepositoryInterface] = twitchChannelEditorsRepository
        self.__twitchChannelInformationHelper: Final[TwitchChannelInformationHelperInterface] = twitchChannelInformationHelper
        self.__twitchChatMessenger: Final[TwitchChatMessengerInterface] = twitchChatMessenger
        self.__twitchFriendsUserIdRepository: Final[TwitchFriendsUserIdRepositoryInterface] = twitchFriendsUserIdRepository
        self.__twitchHandleProvider: Final[TwitchHandleProviderInterface] = twitchHandleProvider
        self.__twitchModeratorHelper: Final[TwitchModeratorHelperInterface] = twitchModeratorHelper
        self.__twitchTokensRepository: Final[TwitchTokensRepositoryInterface] = twitchTokensRepository
        self.__userIdsRepository: Final[UserIdsRepositoryInterface] = userIdsRepository

        self.__commandPatterns: Final[Collection[Pattern]] = frozenset({
            re.compile(r'^\s*!set(?:stream)?title\b', re.IGNORECASE),
            re.compile(r'^\s*!update(?:stream)?title\b', re.IGNORECASE),
        })

        self.__wasPranked: bool = False

    @property
    def commandName(self) -> str:
        return 'UpdateStreamTitleChatCommand'

    @property
    def commandPatterns(self) -> Collection[Pattern]:
        return self.__commandPatterns

    async def handleChatCommand(self, chatMessage: TwitchChatMessage) -> ChatCommandResult:
        if not await self.__hasPermissions(chatMessage):
            return ChatCommandResult.IGNORED

        splits = utils.getCleanedSplits(chatMessage.text)
        if len(splits) < 2:
            self.__timber.log(self.commandName, f'No title argument specified ({splits=}) ({chatMessage=})')
            return ChatCommandResult.IGNORED

        newTitle = ' '.join(splits[1:])
        if not utils.isValidStr(newTitle):
            self.__timber.log(self.commandName, f'Title argument is empty ({newTitle=}) ({splits=}) ({chatMessage=})')
            return ChatCommandResult.IGNORED

        if chatMessage.twitchUser.arePranksEnabled and await self.__stopForPrank(
            chatterUserId = chatMessage.chatterUserId,
            chatterUserName = chatMessage.chatterUserName,
            twitchChannelId = chatMessage.twitchChannelId,
            twitchChatMessageId = chatMessage.twitchChatMessageId,
            twitchUser = chatMessage.twitchUser,
        ):
            return ChatCommandResult.IGNORED

        try:
            updatedTitle = await self.__twitchChannelInformationHelper.setTitle(
                title = newTitle,
                twitchChannelId = chatMessage.twitchChannelId,
            )
        except RequiredTwitchAuthorizationIsMissingException as e:
            self.__timber.log(self.commandName, f'Can\'t update stream title as required Twitch authorization is missing ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.CONSUMED
        except TwitchStatusCodeException as e:
            self.__timber.log(self.commandName, f'Can\'t update stream title as we encountered a Twitch status code error ({chatMessage=})', e, traceback.format_exc())
            return ChatCommandResult.CONSUMED
        except Exception as e:
            self.__timber.log(self.commandName, f'Failed to update stream title ({newTitle=}) ({splits=}) ({chatMessage=})', e, traceback.format_exc())

            self.__twitchChatMessenger.send(
                text = '⚠ Failed to update stream title',
                twitchChannelId = chatMessage.twitchChannelId,
                replyMessageId = chatMessage.twitchChatMessageId,
            )

            return ChatCommandResult.CONSUMED

        self.__twitchChatMessenger.send(
            text = f'ⓘ Updated stream title — {updatedTitle}',
            twitchChannelId = chatMessage.twitchChannelId,
            replyMessageId = chatMessage.twitchChatMessageId,
        )

        self.__timber.log(self.commandName, f'Consumed ({updatedTitle=}) ({newTitle=}) ({chatMessage=})')
        return ChatCommandResult.CONSUMED

    async def __hasPermissions(self, chatMessage: TwitchChatMessage) -> bool:
        isStreamer = chatMessage.chatterUserId == chatMessage.twitchChannelId

        isAdministrator = chatMessage.chatterUserId == await self.__administratorProvider.getAdministratorUserId()

        isEditor = await self.__twitchChannelEditorsRepository.isEditor(
            chatterUserId = chatMessage.chatterUserId,
            twitchChannelId = chatMessage.twitchChannelId,
        )

        isModerator = await self.__twitchModeratorHelper.isModerator(
            request = TwitchModeratorHelperInterface.Request(
                chatterUserId = chatMessage.chatterUserId,
                twitchChannelId = chatMessage.twitchChannelId
            ),
        )

        return isStreamer or isAdministrator or isEditor or isModerator

    async def __stopForPrank(
        self,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        twitchUser: UserInterface,
    ) -> bool:
        if self.__wasPranked:
            return False

        harleyHardtUserId = await self.__twitchFriendsUserIdRepository.getHarleyHardtUserId()
        if not utils.isValidStr(harleyHardtUserId) or chatterUserId != harleyHardtUserId:
            return False

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()
        moderatorUserId = await self.__userIdsRepository.fetchUserId(twitchHandle)

        if not utils.isValidStr(moderatorUserId):
            return False

        moderatorTwitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = moderatorUserId,
        )

        userTwitchAccessToken = await self.__twitchTokensRepository.getAccessTokenById(
            twitchChannelId = twitchChannelId,
        )

        if not utils.isValidStr(moderatorTwitchAccessToken) or not utils.isValidStr(userTwitchAccessToken):
            return False

        self.__wasPranked = True

        self.__streamAlertsManager.submitAlert(StreamAlert(
            soundAlert = SoundAlert.MEGA_GRENADE,
            twitchChannel = twitchUser.handle,
            twitchChannelId = twitchChannelId,
            ttsEvent = TtsEvent(
                message = f'Harley, get fucked',
                twitchChannel = twitchUser.handle,
                twitchChannelId = twitchChannelId,
                userId = harleyHardtUserId,
                userName = chatterUserName,
                donation = None,
                provider = twitchUser.defaultTtsProvider,
                providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE,
                raidInfo = None,
            ),
        ))

        self.__timeoutActionMachine.submitAction(BasicTimeoutAction(
            timeoutDuration = ExactTimeoutDuration(
                seconds = 300,
            ),
            actionId = await self.__timeoutIdGenerator.generateActionId(),
            chatMessage = None,
            instigatorUserId = harleyHardtUserId,
            moderatorTwitchAccessToken = moderatorTwitchAccessToken,
            moderatorUserId = moderatorUserId,
            reason = None,
            targetUserId = harleyHardtUserId,
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = None,
            userTwitchAccessToken = userTwitchAccessToken,
            streamStatusRequirement = None,
            user = twitchUser,
        ))

        self.__twitchChatMessenger.send(
            text = f'@{chatterUserName} gloverGape gloverGape gloverGape gloverGape gloverGape gloverGape',
            twitchChannelId = twitchChannelId,
            replyMessageId = twitchChatMessageId,
        )

        return True
