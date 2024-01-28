from abc import ABC, abstractmethod

from CynanBot.streamAlertsManager.streamAlert import StreamAlert


class StreamAlertsManagerInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def submitAlert(self, alert: StreamAlert):
        pass
