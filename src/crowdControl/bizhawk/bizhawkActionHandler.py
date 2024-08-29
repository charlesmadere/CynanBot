from ..actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControlActionHandler import CrowdControlActionHandler
from ...timber.timberInterface import TimberInterface


class BizhawkActionHandler(CrowdControlActionHandler):

    def __init__(
        self,
        timber: TimberInterface
    ):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def handleButtonPressAction(self, action: ButtonPressCrowdControlAction) -> bool:
        if not isinstance(action, ButtonPressCrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        # TODO
        return False

    async def handleGameShuffleAction(self, action: GameShuffleCrowdControlAction) -> bool:
        if not isinstance(action, GameShuffleCrowdControlAction):
            raise TypeError(f'action argument is malformed: \"{action}\"')

        # TODO
        return False
