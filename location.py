class Location():

    def __init__(self, lat: float, lon: float, name: str):
        if lat == None:
            raise ValueError(f'lat argument is malformed: \"{lat}\"')
        elif lon == None:
            raise ValueError(f'lon argument is malformed: \"{lon}\"')
        elif name == None or len(name) == 0 or name.isspace():
            raise ValueError(f'name argument is malformed: \"{name}\"')

        self.__latitude = lat
        self.__longitude = lon
        self.__name = name

    def getLatitude(self):
        return self.__latitude

    def getLongitude(self):
        return self.__longitude

    def getName(self):
        return self.__name
