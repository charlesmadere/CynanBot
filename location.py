import math
from datetime import tzinfo


class Location():

    def __init__(self, lat: float, lon: float, id_: str, name: str, timeZone: tzinfo):
        if lat is None or not math.isfinite(lat):
            raise ValueError(f'lat argument is malformed: \"{lat}\"')
        elif lon is None or not math.isfinite(lon):
            raise ValueError(f'lon argument is malformed: \"{lon}\"')
        elif id_ is None or len(id_) == 0 or id_.isspace():
            raise ValueError(f'id_ argument is malformed: \"{id_}\"')
        elif name is None or len(name) == 0 or name.isspace():
            raise ValueError(f'name argument is malformed: \"{name}\"')
        elif timeZone is None:
            raise ValueError(f'timeZone argument is malformed: \"{timeZone}\"')

        self.__id_ = id_
        self.__latitude = lat
        self.__longitude = lon
        self.__name = name
        self.__timeZone = timeZone

    def getId(self):
        return self.__id_

    def getLatitude(self):
        return self.__latitude

    def getLongitude(self):
        return self.__longitude

    def getName(self):
        return self.__name

    def getTimeZone(self):
        return self.__timeZone
