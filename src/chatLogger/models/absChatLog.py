from abc import ABC, abstractmethod
from datetime import datetime


class AbsChatLog(ABC):

    @abstractmethod
    def getDateTime(self) -> datetime:
        pass

    def getDateAndTimeStr(self) -> str:
        dateStr = f'{self.getYearStr()}/{self.getMonthStr()}/{self.getDayStr()}'
        timeStr = f'{self.getHoursStr()}:{self.getMinutesStr()}:{self.getSecondsStr()}.{self.getMillisStr()}'
        return f'{dateStr} {timeStr}'

    def getDayStr(self) -> str:
        return self.getDateTime().strftime('%d')

    def getHoursStr(self) -> str:
        return self.getDateTime().strftime('%H')

    def getMillisStr(self) -> str:
        return self.getDateTime().strftime('%f')[:-3]

    def getMinutesStr(self) -> str:
        return self.getDateTime().strftime('%M')

    def getMonthStr(self) -> str:
        return self.getDateTime().strftime('%m')

    def getSecondsStr(self) -> str:
        return self.getDateTime().strftime('%S')

    @abstractmethod
    def getTwitchChannel(self) -> str:
        pass

    @abstractmethod
    def getTwitchChannelId(self) -> str:
        pass

    def getYearStr(self) -> str:
        return self.getDateTime().strftime('%Y')
