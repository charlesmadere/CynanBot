from typing import Final

from frozendict import frozendict

from .timeoutCheerAction import TimeoutCheerAction
from .timeoutCheerActionHelperInterface import TimeoutCheerActionHelperInterface
from .timeoutCheerActionTargetType import TimeoutCheerActionTargetType
from ..absCheerAction import AbsCheerAction
from ..cheerActionStreamStatusRequirement import CheerActionStreamStatusRequirement
from ...chatterInventory.helpers.useChatterItemHelperInterface import UseChatterItemHelperInterface
from ...chatterInventory.idGenerator.chatterInventoryIdGeneratorInterface import ChatterInventoryIdGeneratorInterface
from ...chatterInventory.models.chatterItemType import ChatterItemType
from ...chatterInventory.models.useChatterItemRequest import UseChatterItemRequest
from ...chatterInventory.models.useChatterItemResult import UseChatterItemResult
from ...chatterInventory.settings.chatterInventorySettingsInterface import ChatterInventorySettingsInterface
from ...misc import utils as utils
from ...timeout.models.timeoutStreamStatusRequirement import TimeoutStreamStatusRequirement
from ...users.userInterface import UserInterface


class TimeoutCheerActionHelper(TimeoutCheerActionHelperInterface):

    def __init__(
        self,
        chatterInventoryIdGenerator: ChatterInventoryIdGeneratorInterface,
        chatterInventorySettings: ChatterInventorySettingsInterface,
        useChatterItemHelper: UseChatterItemHelperInterface,
    ):
        if not isinstance(chatterInventoryIdGenerator, ChatterInventoryIdGeneratorInterface):
            raise TypeError(f'chatterInventoryIdGenerator argument is malformed: \"{chatterInventoryIdGenerator}\"')
        elif not isinstance(chatterInventorySettings, ChatterInventorySettingsInterface):
            raise TypeError(f'chatterInventorySettings argument is malformed: \"{chatterInventorySettings}\"')
        elif not isinstance(useChatterItemHelper, UseChatterItemHelperInterface):
            raise TypeError(f'useChatterItemHelper argument is malformed: \"{useChatterItemHelper}\"')

        self.__chatterInventoryIdGenerator: Final[ChatterInventoryIdGeneratorInterface] = chatterInventoryIdGenerator
        self.__chatterInventorySettings: Final[ChatterInventorySettingsInterface] = chatterInventorySettings
        self.__useChatterItemHelper: Final[UseChatterItemHelperInterface] = useChatterItemHelper

    async def handleTimeoutCheerAction(
        self,
        actions: frozendict[int, AbsCheerAction],
        bits: int,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        twitchChannelId: str,
        twitchChatMessageId: str | None,
        userTwitchAccessToken: str,
        user: UserInterface,
    ) -> bool:
        if not isinstance(actions, frozendict):
            raise TypeError(f'actions argument is malformed: \"{actions}\"')
        elif not utils.isValidInt(bits):
            raise TypeError(f'bits argument is malformed: \"{bits}\"')
        elif bits < 1 or bits > utils.getIntMaxSafeSize():
            raise ValueError(f'bits argument is out of bounds: {bits}')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif not utils.isValidStr(message):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(moderatorTwitchAccessToken):
            raise TypeError(f'moderatorTwitchAccessToken argument is malformed: \"{moderatorTwitchAccessToken}\"')
        elif not utils.isValidStr(moderatorUserId):
            raise TypeError(f'moderatorUserId argument is malformed: \"{moderatorUserId}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif twitchChatMessageId is not None and not isinstance(twitchChatMessageId, str):
            raise TypeError(f'twitchChatMessageId argument is malformed: \"{twitchChatMessageId}\"')
        elif not utils.isValidStr(userTwitchAccessToken):
            raise TypeError(f'userTwitchAccessToken argument is malformed: \"{userTwitchAccessToken}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        action = actions.get(bits, None)

        if not isinstance(action, TimeoutCheerAction) or not action.isEnabled:
            return False

        itemType: ChatterItemType

        if action.targetType is TimeoutCheerActionTargetType.SPECIFIC_TARGET_ONLY:
            itemType = ChatterItemType.BANANA
        else:
            itemType = ChatterItemType.GRENADE

        result = await self.__useChatterItemHelper.useItem(UseChatterItemRequest(
            ignoreInventory = True,
            itemType = itemType,
            chatMessage = message,
            chatterUserId = cheerUserId,
            requestId = await self.__chatterInventoryIdGenerator.generateRequestId(),
            twitchChannelId = twitchChannelId,
            twitchChatMessageId = twitchChatMessageId,
            user = user,
        ))

        return result is UseChatterItemResult.OK

    async def __mapStreamStatusRequirement(
        self,
        streamStatusRequirement: CheerActionStreamStatusRequirement,
    ) -> TimeoutStreamStatusRequirement:
        match streamStatusRequirement:
            case CheerActionStreamStatusRequirement.ANY:
                return TimeoutStreamStatusRequirement.ANY

            case CheerActionStreamStatusRequirement.ONLINE:
                return TimeoutStreamStatusRequirement.ONLINE

            case CheerActionStreamStatusRequirement.OFFLINE:
                return TimeoutStreamStatusRequirement.OFFLINE

            case _:
                raise ValueError(f'Encountered unknown CheerActionStreamStatusRequirement value: \"{streamStatusRequirement}\"')
