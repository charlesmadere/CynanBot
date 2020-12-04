import pytz


# A listing of pytz timezones can be found here:
# https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones

class TimeZoneRepository():

    def __init__(self):
        self.__timeZones = dict()

    def getTimeZone(self, timeZone: str):
        if timeZone is None or len(timeZone) == 0 or timeZone.isspace():
            return None
        elif timeZone in self.__timeZones:
            return self.__timeZones[timeZone]

        newTimeZone = pytz.timezone(timeZone)
        self.__timeZones[timeZone] = newTimeZone
        return newTimeZone
