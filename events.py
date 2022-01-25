import asyncio
import locale
from abc import ABC, abstractmethod
from typing import Dict

from twitchio.channel import Channel

import CynanBotCommon.utils as utils
import twitchUtils
from authHelper import AuthHelper
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
        generalSettingsRepository: GeneralSettingsRepository
    ):
        if generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository

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
            print(f'{twitchUser.getHandle()} was raided, but the tags dictionary seems to have strange values: {tags}')
            return False

        if self.__generalSettingsRepository.isDebugLoggingEnabled():
            print(f'Raid for {twitchUser.getHandle()} () from {raidedByName} ({utils.getNowTimeText()})')

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

        return True


class SubGiftEvent(AbsEvent):

    def __init__(
        self,
        authHelper: AuthHelper,
        generalSettingsRepository: GeneralSettingsRepository
    ):
        if authHelper is None:
            raise ValueError(f'authHelper argument is malformed: \"{authHelper}\"')
        elif generalSettingsRepository is None:
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')

        self.__authHelper: AuthHelper = authHelper
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository

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

        # TODO DELETE
        print(f'Sub gift tags ({utils.getNowTimeText(includeSeconds = True)}): {tags}')

        if not self.__generalSettingsRepository.isSubGiftThankingEnabled():
            return False
        elif not twitchUser.isSubGiftThankingEnabled():
            return False

        # TODO check to ensure that self.__nick is receiving the sub gift

        if not utils.getBoolFromDict(tags, 'msg-param-was-gifted', False):
            return False

        giftedByName = tags.get('msg-param-was-gifted')
        if not utils.isValidStr(giftedByName):
            giftedByName = tags.get('display-name')
        if not utils.isValidStr(giftedByName):
            giftedByName = tags.get('login')

        # TODO add thank you message

        return True
