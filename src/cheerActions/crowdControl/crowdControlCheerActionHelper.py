from frozenlist import FrozenList

from .crowdControlCheerAction import CrowdControlCheerAction
from .crowdControlCheerActionHelperInterface import CrowdControlCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ...timber.timberInterface import TimberInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...users.userInterface import UserInterface


class CrowdControlCheerActionHelper(CrowdControlCheerActionHelperInterface):

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

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

        # TODO
        return False

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
