from dataclasses import dataclass
from datetime import datetime
from typing import Collection

from .messageMethod import MessageMethod


@dataclass(frozen = True, slots = True)
class SentMessage:
    successfullySent: bool
    exceptions: Collection[Exception] | None
    dateTime: datetime
    numberOfSendAttempts: int
    messageMethod: MessageMethod
    msg: str
    twitchChannel: str
    twitchChannelId: str

    def getDateAndTimeStr(self) -> str:
        dateStr = f'{self.getYearStr()}/{self.getMonthStr()}/{self.getDayStr()}'
        timeStr = f'{self.getHoursStr()}:{self.getMinutesStr()}:{self.getSecondsStr()}.{self.getMillisStr()}'
        return f'{dateStr} {timeStr}'

    def getDayStr(self) -> str:
        return self.dateTime.strftime('%d')

    def getHoursStr(self) -> str:
        return self.dateTime.strftime('%H')

    def getMillisStr(self) -> str:
        return self.dateTime.strftime('%f')[:-3]

    def getMinutesStr(self) -> str:
        return self.dateTime.strftime('%M')

    def getMonthStr(self) -> str:
        return self.dateTime.strftime('%m')

    def getSecondsStr(self) -> str:
        return self.dateTime.strftime('%S')

    def getYearStr(self) -> str:
        return self.dateTime.strftime('%Y')
