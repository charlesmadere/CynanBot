from .absChatAction import AbsChatAction
from ..accessLevelChecking.accessLevelCheckingHelperInterface import AccessLevelCheckingHelperInterface
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ..ttsChatter.repository.ttsChatterRepositoryInterface import TtsChatterRepositoryInterface
from ..ttsChatter.settings.ttsChatterSettingsRepositoryInterface import TtsChatterSettingsRepositoryInterface
from ..twitch.api.models.twitchSubscriberTier import TwitchSubscriberTier
from ..twitch.absTwitchSubscriptionHandler import AbsTwitchSubscriptionHandler
from ..twitch.chatMessenger.twitchChatMessenger import TwitchChatMessenger
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.accessLevel.accessLevel import AccessLevel
from ..users.userInterface import UserInterface


class TtsChatterChatAction(AbsChatAction):

    def __init__(
        self,
        accessLevelCheckingHelper: AccessLevelCheckingHelperInterface,
        compositeTtsManagerProvider: CompositeTtsManagerProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        ttsChatterRepository: TtsChatterRepositoryInterface,
        ttsChatterSettingsRepository: TtsChatterSettingsRepositoryInterface,
        twitchChatMessenger: TwitchChatMessenger
    ):
        if not isinstance(accessLevelCheckingHelper, AccessLevelCheckingHelperInterface):
            raise TypeError(f'accessLevelCheckingHelper argument is malformed: \"{accessLevelCheckingHelper}\"')
        elif not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(ttsChatterRepository, TtsChatterRepositoryInterface):
            raise TypeError(f'ttsChatterRepository argument is malformed: \"{ttsChatterRepository}\"')
        elif not isinstance(ttsChatterSettingsRepository, TtsChatterSettingsRepositoryInterface):
            raise TypeError(f'ttsChatterSettingsRepository argument is malformed: \"{ttsChatterSettingsRepository}\"')
        elif not isinstance(twitchChatMessenger, TwitchChatMessenger):
            raise TypeError(f'twitchChatMessenger argument is malformed: \"{twitchChatMessenger}\"')

        self.__accessLevelCheckingHelper: AccessLevelCheckingHelperInterface = accessLevelCheckingHelper
        self.__compositeTtsManagerProvider: CompositeTtsManagerProviderInterface = compositeTtsManagerProvider
        self.__streamAlertsManager: StreamAlertsManagerInterface = streamAlertsManager
        self.__ttsChatterRepository: TtsChatterRepositoryInterface = ttsChatterRepository
        self.__ttsChatterSettingsRepository: TtsChatterSettingsRepositoryInterface = ttsChatterSettingsRepository
        self.__twitchChatMessenger: TwitchChatMessenger = twitchChatMessenger
        self.__subscriptionCounter: int = 0
        self.__remainder: int = 0

    async def __checkTtsThresholdMet(self) -> bool:
        return self.__subscriptionCounter >= await self.__ttsChatterSettingsRepository.ttsOnThreshold()

    async def decrementTtsSubCount(
        self,
        bits,
        twitchChannelId,
    ):
        count = utils.math.floor((bits + self.__remainder) / await self.__ttsChatterSettingsRepository.ttsOffThreshold())
        self.__subscriptionCounter -= count
        self.__remainder = (bits + self.__remainder) % await self.__ttsChatterSettingsRepository.ttsOffThreshold()
        await self.reportStatusToChat(twitchChannelId)


    async def incrementTtsSubCount(
        self,
        subscriptionData: AbsTwitchSubscriptionHandler.SubscriptionData
    ):
        user = subscriptionData.user

        if not user.isTtsEnabled:
            return

        total = subscriptionData.total
        multiplier: int = 1

        if total is None and subscriptionData.communitySubGift is not None:
            total = subscriptionData.communitySubGift.total

        if total is None:
            return

        match subscriptionData.tier:
            case TwitchSubscriberTier.TIER_TWO:
                multiplier = 2
            case TwitchSubscriberTier.TIER_THREE:
                multiplier = 5

        self.__subscriptionCounter += total * multiplier

        await self.reportStatusToChat(subscriptionData.twitchChannelId)

    async def reportStatusToChat(
        self,
        twitchChannelId
    ):
        message: str
        if await self.__checkTtsThresholdMet():
            left = (self.__subscriptionCounter * await self.__ttsChatterSettingsRepository.ttsOffThreshold()) - self.__remainder
            message = f'{left} bits remaining to turn off TTS'
        else:
            # x = 1 - 0
            left = await self.__ttsChatterSettingsRepository.ttsOnThreshold() - self.__subscriptionCounter
            message = f'{left} subs remaining to turn on TTS'

        self.__twitchChatMessenger.send(
            text = message,
            twitchChannelId = twitchChannelId,
            delaySeconds = 1
        )


    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.areTtsChattersEnabled or not user.isTtsEnabled:
            return False

        if await self.__ttsChatterSettingsRepository.useThreshold() and not await self.__checkTtsThresholdMet():
            return False

        if not await self.__ttsChatterRepository.isTtsChatter(
            chatterUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        ):
            return False

        chatMessage = utils.cleanStr(message.getContent())
        if not utils.isValidStr(chatMessage):
            return False

        if chatMessage.startswith('!'):
            return False

        if await self.__ttsChatterSettingsRepository.subscriberOnly() and not await self.__accessLevelCheckingHelper.checkStatus(AccessLevel.SUBSCRIBER, message):

            return False

        providerOverridableStatus: TtsProviderOverridableStatus

        if user.isChatterPreferredTtsEnabled:
            providerOverridableStatus = TtsProviderOverridableStatus.CHATTER_OVERRIDABLE
        else:
            providerOverridableStatus = TtsProviderOverridableStatus.TWITCH_CHANNEL_DISABLED

        ttsEvent = TtsEvent(
            message = chatMessage,
            twitchChannel = user.handle,
            twitchChannelId = await message.getTwitchChannelId(),
            userId = message.getAuthorId(),
            userName = message.getAuthorName(),
            donation = None,
            provider = user.defaultTtsProvider,
            providerOverridableStatus = providerOverridableStatus,
            raidInfo = None
        )

        if await self.__ttsChatterSettingsRepository.useMessageQueueing():
            self.__streamAlertsManager.submitAlert(StreamAlert(
                soundAlert = None,
                twitchChannel = user.handle,
                twitchChannelId = await message.getTwitchChannelId(),
                ttsEvent = ttsEvent
            ))

            return True
        else:
            compositeTtsManager = self.__compositeTtsManagerProvider.constructNewInstance(
                useSharedSoundPlayerManager = False
            )

            return await compositeTtsManager.playTtsEvent(ttsEvent)
