from .beanChanceCheerActionHelperInterface import BeanChanceCheerActionHelperInterface
from ..absCheerAction import AbsCheerAction
from ..beanChanceCheerAction import BeanChanceCheerAction
from ...timber.timberInterface import TimberInterface
from ...twitch.configuration.twitchChannelProvider import TwitchChannelProvider
from ...users.userInterface import UserInterface


class BeanChanceCheerActionHelper(BeanChanceCheerActionHelperInterface):

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

        self.__twitchChannelProvider: TwitchChannelProvider | None = None

    async def handleBeanChanceCheerAction(
        self,
        bits: int,
        actions: list[AbsCheerAction],
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        if not user.areCheerActionsEnabled or not user.areBeanChancesEnabled:
            return False

        beanAction: BeanChanceCheerAction | None = None

        for action in actions:
            if isinstance(action, BeanChanceCheerAction) and action.isEnabled and action.bits == bits:
                beanAction = action
                break

        if beanAction is None:
            return False

        # TODO
        return False

    def setTwitchChannelProvider(self, provider: TwitchChannelProvider | None):
        if provider is not None and not isinstance(provider, TwitchChannelProvider):
            raise TypeError(f'provider argument is malformed: \"{provider}\"')

        self.__twitchChannelProvider = provider
