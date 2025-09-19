from ..actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControlActionHandleResult import CrowdControlActionHandleResult
from ..crowdControlActionHandler import CrowdControlActionHandler


class StubCrowdControlActionHandler(CrowdControlActionHandler):

    async def handleButtonPressAction(
        self,
        action: ButtonPressCrowdControlAction
    ) -> CrowdControlActionHandleResult:
        # this method is intentionally empty
        return CrowdControlActionHandleResult.ABANDON

    async def handleGameShuffleAction(
        self,
        action: GameShuffleCrowdControlAction
    ) -> CrowdControlActionHandleResult:
        # this method is intentionally empty
        return CrowdControlActionHandleResult.ABANDON
