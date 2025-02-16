from datetime import timedelta
from typing import Collection

from .absChatAction import AbsChatAction
from ..accessLevelChecking.accessLevelCheckingHelperInterface import AccessLevelCheckingHelperInterface
from ..misc import utils as utils
from ..misc.timedDict import TimedDict
from ..mostRecentChat.mostRecentChat import MostRecentChat
from ..soundPlayerManager.provider.soundPlayerManagerProviderInterface import SoundPlayerManagerProviderInterface
from ..soundPlayerManager.randomizerHelper.soundPlayerRandomizerHelperInterface import \
    SoundPlayerRandomizerHelperInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchMessage import TwitchMessage
from ..users.accessLevel.accessLevel import AccessLevel
from ..users.chatSoundAlert.absChatSoundAlert import AbsChatSoundAlert
from ..users.chatSoundAlert.chatSoundAlertQualifier import ChatSoundAlertQualifer
from ..users.chatSoundAlert.directoryPathChatSoundAlert import DirectoryPathChatSoundAlert
from ..users.chatSoundAlert.filePathChatSoundAlert import FilePathChatSoundAlert
from ..users.chatSoundAlert.soundAlertChatSoundAlert import SoundAlertChatSoundAlert
from ..users.userInterface import UserInterface


class SoundAlertChatAction(AbsChatAction):

    def __init__(
        self,
        accessLevelCheckingHelper: AccessLevelCheckingHelperInterface,
        soundPlayerManagerProvider: SoundPlayerManagerProviderInterface,
        soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface,
        timber: TimberInterface,
        cooldown: timedelta = timedelta(minutes = 1)
    ):
        if not isinstance(accessLevelCheckingHelper, AccessLevelCheckingHelperInterface):
            raise TypeError(f'accessLevelCheckingHelper argument is malformed: \"{accessLevelCheckingHelper}\"')
        elif not isinstance(soundPlayerManagerProvider, SoundPlayerManagerProviderInterface):
            raise TypeError(f'soundPlayerManagerProvider argument is malformed: \"{soundPlayerManagerProvider}\"')
        elif not isinstance(soundPlayerRandomizerHelper, SoundPlayerRandomizerHelperInterface):
            raise TypeError(f'soundPlayerRandomizerHelper argument is malformed: \"{soundPlayerRandomizerHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(cooldown, timedelta):
            raise TypeError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__accessLevelCheckingHelper: AccessLevelCheckingHelperInterface = accessLevelCheckingHelper
        self.__soundPlayerManagerProvider: SoundPlayerManagerProviderInterface = soundPlayerManagerProvider
        self.__soundPlayerRandomizerHelper: SoundPlayerRandomizerHelperInterface = soundPlayerRandomizerHelper
        self.__timber: TimberInterface = timber
        self.__lastMessageTimes: dict[str, TimedDict] = dict()
        self.__cooldown: timedelta = cooldown

    async def __determineSoundAlertFromMessage(
        self,
        chatSoundAlerts: Collection[AbsChatSoundAlert],
        chatMessage: str
    ) -> AbsChatSoundAlert | None:
        for chatSoundAlert in chatSoundAlerts:
            match chatSoundAlert.qualifier:
                case ChatSoundAlertQualifer.CONTAINS:
                    if chatSoundAlert.message.casefold() in chatMessage.casefold():
                        return chatSoundAlert
                case ChatSoundAlertQualifer.EXACT:
                    if chatSoundAlert.message.casefold() == chatMessage.casefold():
                        return chatSoundAlert

        return None

    async def handleChat(
        self,
        mostRecentChat: MostRecentChat | None,
        message: TwitchMessage,
        user: UserInterface
    ) -> bool:
        if not user.areSoundAlertsEnabled or not user.areChatSoundAlertsEnabled:
            return False

        chatSoundAlerts = user.chatSoundAlerts
        chatMessage = utils.cleanStr(message.getContent())

        if chatSoundAlerts is None or len(chatSoundAlerts) == 0 or not utils.isValidStr(chatMessage):
            return False

        chatSoundAlert = await self.__determineSoundAlertFromMessage(
            chatSoundAlerts = chatSoundAlerts,
            chatMessage = chatMessage
        )

        if chatSoundAlert is None:
            return False

        if not await self.__accessLevelCheckingHelper.checkStatus(AccessLevel.SUBSCRIBER, message):
            return False

        if self.__lastMessageTimes.get(chatMessage) is None:
            self.__lastMessageTimes[chatMessage] = TimedDict(self.__cooldown)

        if not  self.__lastMessageTimes[chatMessage].isReadyAndUpdate(user.handle):
            return False

        if await self.__playChatSoundAlert(chatSoundAlert):
            self.__timber.log('SoundAlertChatAction', f'Successfully played chatSoundAlert ({message=}) ({chatSoundAlert=})')
            return True
        else:
            return False

    async def __playChatSoundAlert(self, chatSoundAlert: AbsChatSoundAlert) -> bool:
        if isinstance(chatSoundAlert, DirectoryPathChatSoundAlert):
            return await self.__playDirectoryPathChatSoundAlert(
                chatSoundAlert = chatSoundAlert
            )
        elif isinstance(chatSoundAlert, FilePathChatSoundAlert):
            return await self.__playFilePathChatSoundAlert(
                chatSoundAlert = chatSoundAlert
            )
        elif isinstance(chatSoundAlert, SoundAlertChatSoundAlert):
            return await self.__playSoundAlertChatSoundAlert(
                chatSoundAlert = chatSoundAlert
            )
        else:
            raise ValueError(f'Encountered unknown AbsChatSoundAlert: \"{chatSoundAlert}\"')

    async def __playDirectoryPathChatSoundAlert(self, chatSoundAlert: DirectoryPathChatSoundAlert) -> bool:
        soundAlert = await self.__soundPlayerRandomizerHelper.chooseRandomFromDirectorySoundAlert(
            directoryPath = chatSoundAlert.directoryPath
        )

        if not utils.isValidStr(soundAlert):
            return False

        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()

        return await soundPlayerManager.playSoundFile(
            filePath = soundAlert,
            volume = chatSoundAlert.volume
        )

    async def __playFilePathChatSoundAlert(self, chatSoundAlert: FilePathChatSoundAlert) -> bool:
        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()

        return await soundPlayerManager.playSoundFile(
            filePath = chatSoundAlert.filePath,
            volume = chatSoundAlert.volume
        )

    async def __playSoundAlertChatSoundAlert(self, chatSoundAlert: SoundAlertChatSoundAlert) -> bool:
        soundPlayerManager = self.__soundPlayerManagerProvider.constructNewSoundPlayerManagerInstance()

        return await soundPlayerManager.playSoundAlert(
            alert = chatSoundAlert.soundAlert,
            volume = chatSoundAlert.volume
        )
