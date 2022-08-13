import locale
from abc import ABC, abstractmethod
from asyncio import AbstractEventLoop
from typing import Any, Dict

from twitchio.channel import Channel

import CynanBotCommon.utils as utils
import twitch.twitchUtils as twitchUtils
from authRepository import AuthRepository
from CynanBotCommon.chatLogger.chatLogger import ChatLogger
from CynanBotCommon.timber.timber import Timber
from generalSettingsRepository import GeneralSettingsRepository
from users.user import User


class AbsEvent(ABC):

    @abstractmethod
    async def handleEvent(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        tags: Dict[str, Any]
    ) -> bool:
        pass


class RaidLogEvent(AbsEvent):

    def __init__(
        self,
        chatLogger: ChatLogger,
        timber: Timber
    ):
        if chatLogger is None:
            raise ValueError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__chatLogger: ChatLogger = chatLogger
        self.__timber: Timber = timber

    async def handleEvent(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        tags: Dict[str, Any]
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif tags is None:
            raise ValueError(f'tags argument is malformed: \"{tags}\"')

        if not twitchUser.isChatLoggingEnabled():
            return False

        raidedByName = tags.get('msg-param-displayName')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('display-name')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('login')

        if not utils.isValidStr(raidedByName):
            self.__timber.log('RaidLogEvent', f'{twitchUser.getHandle()} was raided, but the tags dictionary seems to have strange values: {tags}')
            return False

        raidSize = utils.getIntFromDict(tags, 'msg-param-viewerCount', 0)

        self.__chatLogger.logRaid(
            raidSize = raidSize,
            fromWho = raidedByName,
            twitchChannel = twitchChannel
        )

        return True


class RaidThankEvent(AbsEvent):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber
    ):
        if eventLoop is None:
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber

    async def handleEvent(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        tags: Dict[str, Any]
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif tags is None:
            raise ValueError(f'tags argument is malformed: \"{tags}\"')

        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isRaidLinkMessagingEnabled():
            return False
        elif not twitchUser.isRaidLinkMessagingEnabled():
            return False

        raidedByName = tags.get('msg-param-displayName')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('display-name')
        if not utils.isValidStr(raidedByName):
            raidedByName = tags.get('login')

        if not utils.isValidStr(raidedByName):
            self.__timber.log('RaidEvent', f'{twitchUser.getHandle()} was raided, but the tags dictionary seems to have strange values: {tags}')
            return False

        messageSuffix = f'😻 Raiders, if you could, I\'d really appreciate you clicking this link to watch the stream. It helps me on my path to partner. {twitchUser.getTwitchUrl()} Thank you! ✨'
        raidSize = utils.getIntFromDict(tags, 'msg-param-viewerCount', -1)

        message: str = None
        if raidSize >= 10:
            raidSizeStr = locale.format_string("%d", raidSize, grouping = True)
            message = f'Thank you for the raid of {raidSizeStr} {raidedByName}! {messageSuffix}'
        else:
            message = f'Thank you for the raid {raidedByName}! {messageSuffix}'

        delaySeconds = generalSettings.getRaidLinkMessagingDelay()

        self.__eventLoop.create_task(twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = delaySeconds,
            message = message
        ))

        self.__timber.log('RaidEvent', f'{twitchUser.getHandle()} received raid of {raidSize} from {raidedByName}!')
        return True


class SubGiftThankingEvent(AbsEvent):

    def __init__(
        self,
        eventLoop: AbstractEventLoop,
        authRepository: AuthRepository,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber
    ):
        if eventLoop is None:
            raise ValueError(f'eventLoop argument is malformed: \"{eventLoop}\"')
        elif authRepository is None:
            raise ValueError(f'authRepository argument is malformed: \"{authRepository}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__eventLoop: AbstractEventLoop = eventLoop
        self.__authRepository: AuthRepository = authRepository
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber

    async def handleEvent(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        tags: Dict[str, Any]
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif tags is None:
            raise ValueError(f'tags argument is malformed: \"{tags}\"')

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        authSnapshot = await self.__authRepository.getAllAsync()

        if not generalSettings.isSubGiftThankingEnabled():
            return False
        elif not twitchUser.isSubGiftThankingEnabled():
            return False

        giftedByName: str = tags.get('display-name')
        if not utils.isValidStr(giftedByName):
            giftedByName = tags.get('login')

        giftedToName: str = tags.get('msg-param-recipient-display-name')
        if not utils.isValidStr(giftedToName):
            giftedToName = tags.get('msg-param-recipient-user-name')

        if giftedToName.lower() != authSnapshot.requireNick().lower():
            return False
        elif not utils.isValidStr(giftedByName):
            return False
        elif giftedToName.lower() == giftedByName.lower():
            return False

        self.__eventLoop.create_task(twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = 5,
            message = f'😻 Thank you for the gifted sub @{giftedByName}! ✨'
        ))

        self.__timber.log('SubGiftThankingEvent', f'{authSnapshot.requireNick()} received sub gift to {twitchUser.getHandle()} from {giftedByName}!')
        return True


class StubEvent(AbsEvent):

    def __init__(self):
        pass

    async def handleEvent(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        tags: Dict[str, Any]
    ) -> bool:
        return False
