from ..streamAlert import StreamAlert
from ..streamAlertsManagerInterface import StreamAlertsManagerInterface


class StubStreamAlertsManager(StreamAlertsManagerInterface):

    def start(self):
        # this method is intentionally empty
        pass

    def submitAlert(self, alert: StreamAlert):
        # this method is intentionally empty
        pass
