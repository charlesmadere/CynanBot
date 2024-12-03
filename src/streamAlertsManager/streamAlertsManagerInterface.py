from abc import ABC, abstractmethod

from .streamAlert import StreamAlert


class StreamAlertsManagerInterface(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    async def stopCurrentAlert(self):
        pass

    @abstractmethod
    def submitAlert(self, alert: StreamAlert):
        pass
