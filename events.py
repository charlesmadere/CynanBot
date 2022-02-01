import asyncio
import locale
from abc import ABC, abstractmethod
from typing import Dict

from twitchio.channel import Channel

import CynanBotCommon.utils as utils
import twitchUtils
from authHelper import AuthHelper
from CynanBotCommon.timber.timber import Timber
from generalSettingsRepository import GeneralSettingsRepository
from users.user import User


class AbsEvent(ABC):

    @abstractmethod
    async def handleEvent(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        tags: Dict
    ) -> bool:
        pass


class RaidEvent(AbsEvent):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber

    async def handleEvent(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        tags: Dict
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif tags is None:
            raise ValueError(f'tags argument is malformed: \"{tags}\"')

        if not self.__generalSettingsRepository.isRaidLinkMessagingEnabled():
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

        if self.__generalSettingsRepository.isDebugLoggingEnabled():
            self.__timber.log('RaidEvent', f'Raid for {twitchUser.getHandle()} () from {raidedByName}')

        messageSuffix = f'😻 Raiders, if you could, I\'d really appreciate you clicking this link to watch the stream. It helps me on my path to partner. {twitchUser.getTwitchUrl()} Thank you! ✨'
        raidSize = utils.getIntFromDict(tags, 'msg-param-viewerCount', -1)

        message: str = None
        if raidSize >= 10:
            raidSizeStr = locale.format_string("%d", raidSize, grouping = True)
            message = f'Thank you for the raid of {raidSizeStr} {raidedByName}! {messageSuffix}'
        else:
            message = f'Thank you for the raid {raidedByName}! {messageSuffix}'

        asyncio.create_task(twitchUtils.waitThenSend(
            messageable = twitchChannel,
            delaySeconds = self.__generalSettingsRepository.getRaidLinkMessagingDelay(),
            message = message
        ))
        self.__timber.log('RaidEvent', f'{twitchUser.getHandle()} received raid of {raidSize} from {raidedByName}!')

        return True


class SubGiftThankingEvent(AbsEvent):

    def __init__(
        self,
        authHelper: AuthHelper,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber
    ):
        if authHelper is None:
            raise ValueError(f'authHelper argument is malformed: \"{authHelper}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif timber is None:
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__authHelper: AuthHelper = authHelper
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber

    async def handleEvent(
        self,
        twitchChannel: Channel,
        twitchUser: User,
        tags: Dict
    ) -> bool:
        if twitchChannel is None:
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif tags is None:
            raise ValueError(f'tags argument is malformed: \"{tags}\"')

        if not self.__generalSettingsRepository.isSubGiftThankingEnabled():
            return False
        elif not twitchUser.isSubGiftThankingEnabled():
            return False

        giftedByName: str = tags.get('display-name')
        if not utils.isValidStr(giftedByName):
            giftedByName = tags.get('login')

        giftedToName: str = tags.get('msg-param-recipient-display-name')
        if not utils.isValidStr(giftedToName):
            giftedToName = tags.get('msg-param-recipient-user-name')

        if giftedToName.lower() != self.__authHelper.requireNick().lower():
            return False
        elif not utils.isValidStr(giftedByName):
            return False
        elif giftedToName.lower() == giftedByName.lower():
            return False

        await twitchUtils.safeSend(
            messageable = twitchChannel,
            message = f'😻 Thank you for the gifted sub @{giftedByName}! ✨'
        )
        self.__timber.log('SubGiftThankingEvent', f'{self.__authHelper.requireNick()} received sub gift to {twitchUser.getHandle()} from {giftedByName}!')

        return True
