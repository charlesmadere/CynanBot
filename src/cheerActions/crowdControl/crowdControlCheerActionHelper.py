from frozenlist import FrozenList

from .crowdControlCheerAction import CrowdControlCheerAction
from .crowdControlCheerActionHelperInterface import CrowdControlCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ...crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ...misc import utils as utils
from ...timber.timberInterface import TimberInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...users.userInterface import UserInterface


class CrowdControlCheerActionHelper(CrowdControlCheerActionHelperInterface):

    def __init__(
        self,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface,
        timber: TimberInterface
    ):
        if not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils argument is malformed: \"{crowdControlUserInputUtils}\"')
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface = crowdControlUserInputUtils
        self.__timber: TimberInterface = timber

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def handleCrowdControlCheerAction(
        self,
        actions: FrozenList[AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not user.areCheerActionsEnabled or not user.isCrowdControlEnabled:
            return False

        crowdControlAction: CrowdControlCheerAction | None = None

        for action in actions:
            if isinstance(action, CrowdControlCheerAction) and action.isEnabled and action.bits == bits:
                crowdControlAction = action
                break

        if crowdControlAction is None:
            return False

        return await self.__inputIntoCrowdControl(
            action = crowdControlAction,
            cheerUserId = cheerUserId,
            cheerUserName = cheerUserName,
            message = message,
            twitchChannelId = broadcasterUserId,
            user = user
        )

    async def __inputIntoCrowdControl(
        self,
        action: CrowdControlCheerAction,
        cheerUserId: str,
        cheerUserName: str,
        message: str | None,
        twitchChannelId: str,
        user: UserInterface
    ) -> bool:
        if not isinstance(action, CrowdControlCheerAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')
        elif not utils.isValidStr(cheerUserId):
            raise TypeError(f'cheerUserId argument is malformed: \"{cheerUserId}\"')
        elif not utils.isValidStr(cheerUserName):
            raise TypeError(f'cheerUserName argument is malformed: \"{cheerUserName}\"')
        elif message is not None and not isinstance(message, str):
            raise TypeError(f'message argument is malformed: \"{message}\"')
        elif not utils.isValidStr(twitchChannelId):
            raise TypeError(f'twitchChannelId argument is malformed: \"{twitchChannelId}\"')
        elif not isinstance(user, UserInterface):
            raise TypeError(f'user argument is malformed: \"{user}\"')

        button = await self.__crowdControlUserInputUtils.parseButtonFromUserInput(
            userInput = message
        )

        if button is None:
            return False

        # TODO
        return False

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
