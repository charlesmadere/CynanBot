from abc import ABC, abstractmethod

from .streamAlert import StreamAlert
from ..misc.startable import Startable


class StreamAlertsManagerInterface(Startable, ABC):

    @abstractmethod
    def submitAlert(self, alert: StreamAlert):
        pass
