import locale
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.twitch.configuration.twitchChannel import TwitchChannel
from CynanBot.twitch.twitchHandleProviderInterface import \
    TwitchHandleProviderInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.users.user import User


class AbsEvent(ABC):

    @abstractmethod
    async def handleEvent(
        self,
        channel: TwitchChannel,
        user: User,
        tags: Dict[str, Any]
    ) -> bool:
        pass


class RaidLogEvent(AbsEvent):

    def __init__(
        self,
        chatLogger: ChatLoggerInterface,
        timber: TimberInterface
    ):
        assert isinstance(chatLogger, ChatLoggerInterface), f"malformed {chatLogger=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"

        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__timber: TimberInterface = timber

    async def handleEvent(self, channel: TwitchChannel, user: User, tags: Dict[str, Any]) -> bool:
        if not user.isChatLoggingEnabled():
            return False

        raidedByName: Optional[str] = tags.get('msg-param-displayName')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('display-name')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('login')

        if not utils.isValidStr(raidedByName):
            self.__timber.log('RaidLogEvent', f'{user.getHandle()} was raided, but the tags dictionary seems to have strange values: {tags}')
            return False

        raidSize = utils.getIntFromDict(tags, 'msg-param-viewerCount', 0)

        self.__chatLogger.logRaid(
            raidSize = raidSize,
            fromWho = raidedByName,
            twitchChannel = user.getHandle()
        )

        return True


class RaidThankEvent(AbsEvent):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def handleEvent(self, channel: TwitchChannel, user: User, tags: Dict[str, Any]) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isRaidLinkMessagingEnabled():
            return False
        elif not user.isRaidLinkMessagingEnabled():
            return False

        raidedByName: Optional[str] = tags.get('msg-param-displayName')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('display-name')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('login')

        if not utils.isValidStr(raidedByName):
            self.__timber.log('RaidEvent', f'{user.getHandle()} was raided, but the tags dictionary seems to have strange values: {tags}')
            return False

        messageSuffix = f'😻 Raiders, if you could, I\'d really appreciate you clicking this link to watch the stream. It helps me on my path to partner. {user.getTwitchUrl()} Thank you! 😻'
        raidSize = utils.getIntFromDict(tags, 'msg-param-viewerCount', -1)

        message: str = ''
        if raidSize >= 10:
            raidSizeStr = locale.format_string("%d", raidSize, grouping = True)
            message = f'Thank you for the raid of {raidSizeStr} {raidedByName}! {messageSuffix}'
        else:
            message = f'Thank you for the raid {raidedByName}! {messageSuffix}'

        await self.__twitchUtils.waitThenSend(
            messageable = channel,
            delaySeconds = generalSettings.getRaidLinkMessagingDelay(),
            message = message
        )

        self.__timber.log('RaidEvent', f'{user.getHandle()} received raid of {raidSize} from {raidedByName}!')
        return True


class SubGiftThankingEvent(AbsEvent):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: TimberInterface,
        twitchHandleProvider: TwitchHandleProviderInterface,
        twitchUtils: TwitchUtilsInterface
    ):
        assert isinstance(generalSettingsRepository, GeneralSettingsRepository), f"malformed {generalSettingsRepository=}"
        assert isinstance(timber, TimberInterface), f"malformed {timber=}"
        assert isinstance(twitchHandleProvider, TwitchHandleProviderInterface), f"malformed {twitchHandleProvider=}"
        assert isinstance(twitchUtils, TwitchUtilsInterface), f"malformed {twitchUtils=}"

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: TimberInterface = timber
        self.__twitchHandleProvider: TwitchHandleProviderInterface = twitchHandleProvider
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils

    async def handleEvent(self, channel: TwitchChannel, user: User, tags: Dict[str, Any]) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isSubGiftThankingEnabled():
            return False
        elif not user.isSubGiftThankingEnabled():
            return False

        giftedByName: Optional[str] = tags.get('display-name')
        if not utils.isValidStr(giftedByName):
            giftedByName = tags.get('login')

        giftedToName: Optional[str] = tags.get('msg-param-recipient-display-name')
        if not utils.isValidStr(giftedToName):
            giftedToName = tags.get('msg-param-recipient-user-name')

        if not utils.isValidStr(giftedByName) or not utils.isValidStr(giftedToName):
            self.__timber.log('SubGiftThankingEvent', f'A subscription was gifted, but the tags dictionary seems to have strange values: {tags}')
            return False

        twitchHandle = await self.__twitchHandleProvider.getTwitchHandle()

        if giftedToName.lower() != twitchHandle.lower():
            return False
        elif giftedByName.lower() == twitchHandle.lower():
            # prevent thanking if the gifter is someone signed in as the bot itself
            return False

        await self.__twitchUtils.waitThenSend(
            messageable = channel,
            delaySeconds = generalSettings.getSubGiftThankMessagingDelay(),
            message = f'😻 Thank you for the gifted sub @{giftedByName}! ✨'
        )

        self.__timber.log('SubGiftThankingEvent', f'{twitchHandle} received sub gift in {user.getHandle()} from {giftedByName}! Thank you!')
        return True


class StubEvent(AbsEvent):

    def __init__(self):
        pass

    async def handleEvent(self, channel: TwitchChannel, user: User, tags: Dict[str, Any]) -> bool:
        return False
