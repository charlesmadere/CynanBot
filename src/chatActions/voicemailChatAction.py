from typing import Final

from .absChatAction import AbsChatAction
from ..misc import utils as utils
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..streamAlertsManager.streamAlert import StreamAlert
from ..streamAlertsManager.streamAlertsManagerInterface import StreamAlertsManagerInterface
from ..tts.models.ttsEvent import TtsEvent
from ..tts.models.ttsProvider import TtsProvider
from ..tts.models.ttsProviderOverridableStatus import TtsProviderOverridableStatus
from ..tts.provider.compositeTtsManagerProviderInterface import CompositeTtsManagerProviderInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.userInterface import UserInterface
from ..voicemail.helpers.voicemailHelperInterface import VoicemailHelperInterface
from ..voicemail.settings.voicemailSettingsRepositoryInterface import VoicemailSettingsRepositoryInterface


class VoicemailChatAction(AbsChatAction):

    def __init__(
        self,
        compositeTtsManagerProvider: CompositeTtsManagerProviderInterface,
        streamAlertsManager: StreamAlertsManagerInterface,
        voicemailHelper: VoicemailHelperInterface,
        voicemailSettingsRepository: VoicemailSettingsRepositoryInterface
    ):
        if not isinstance(compositeTtsManagerProvider, CompositeTtsManagerProviderInterface):
            raise TypeError(f'compositeTtsManagerProvider argument is malformed: \"{compositeTtsManagerProvider}\"')
        elif not isinstance(streamAlertsManager, StreamAlertsManagerInterface):
            raise TypeError(f'streamAlertsManager argument is malformed: \"{streamAlertsManager}\"')
        elif not isinstance(voicemailHelper, VoicemailHelperInterface):
            raise TypeError(f'voicemailHelper argument is malformed: \"{voicemailHelper}\"')
        elif not isinstance(voicemailSettingsRepository, VoicemailSettingsRepositoryInterface):
            raise TypeError(f'voicemailSettingsRepository argument is malformed: \"{voicemailSettingsRepository}\"')

        self.__compositeTtsManagerProvider: Final[CompositeTtsManagerProviderInterface] = compositeTtsManagerProvider
        self.__streamAlertsManager: Final[StreamAlertsManagerInterface] = streamAlertsManager
        self.__voicemailHelper: Final[VoicemailHelperInterface] = voicemailHelper
        self.__voicemailSettingsRepository: Final[VoicemailSettingsRepositoryInterface] = voicemailSettingsRepository

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.isVoicemailEnabled or not user.isTtsEnabled:
            return False

        # TODO notify the user of the number of voicemails that they have
        voicemails = await self.__voicemailHelper.getAllForTargetUser(
            targetUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        # TODO move the below into a command class
        voicemailData = await self.__voicemailHelper.getAndRemoveForTargetUser(
            targetUserId = message.getAuthorId(),
            twitchChannelId = await message.getTwitchChannelId()
        )

        if voicemailData is None:
            return False

        voicemailMessage = utils.cleanStr(voicemailData.message)
        if not utils.isValidStr(voicemailMessage):
            return False

        ttsProvider: TtsProvider
        if voicemailData.ttsProvider is not None:
            ttsProvider = voicemailData.ttsProvider
        else:
            ttsProvider = user.defaultTtsProvider

        ttsEvent = TtsEvent(
            message = voicemailMessage,
            twitchChannel = user.handle,
            twitchChannelId = await message.getTwitchChannelId(),
            userId = message.getAuthorId(),
            userName = message.getAuthorName(),
            donation = None,
            provider = ttsProvider,
            providerOverridableStatus = TtsProviderOverridableStatus.THIS_EVENT_DISABLED,
            raidInfo = None
        )

        if await self.__voicemailSettingsRepository.useMessageQueueing():
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
