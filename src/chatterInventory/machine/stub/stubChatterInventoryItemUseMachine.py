from ..chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ...listeners.chatterItemEventListener import ChatterItemEventListener
from ...models.absChatterItemAction import AbsChatterItemAction


class StubChatterInventoryItemUseMachine(ChatterInventoryItemUseMachineInterface):

    def setEventListener(self, listener: ChatterItemEventListener | None):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass

    def submitAction(self, action: AbsChatterItemAction):
        # this method is intentionally empty
        pass
