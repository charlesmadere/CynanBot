from ..chatterInventoryItemUseMachineInterface import ChatterInventoryItemUseMachineInterface
from ...listeners.useChatterItemEventListener import UseChatterItemEventListener
from ...models.useChatterItemAction import UseChatterItemAction


class StubChatterInventoryItemUseMachine(ChatterInventoryItemUseMachineInterface):

    def setEventListener(self, listener: UseChatterItemEventListener | None):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass

    def submitAction(self, action: UseChatterItemAction):
        # this method is intentionally empty
        pass
