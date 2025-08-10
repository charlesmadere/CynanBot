from ..timeoutActionMachineInterface import TimeoutActionMachineInterface
from ...listener.timeoutEventListener import TimeoutEventListener
from ...models.actions.absTimeoutAction import AbsTimeoutAction


class StubTimeoutActionMachine(TimeoutActionMachineInterface):

    def setEventListener(self, listener: TimeoutEventListener | None):
        # this method is intentionally empty
        pass

    def start(self):
        # this method is intentionally empty
        pass

    def submitAction(self, action: AbsTimeoutAction):
        # this method is intentionally empty
        pass
