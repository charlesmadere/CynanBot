import json
from location import Location
import os

class LocationsRepository():

    def __init__(
        self,
        locationsFile: str = 'locationsRepository.json'
    ):
        if locationsFile == None or len(locationsFile) == 0 or locationsFile.isspace():
            raise ValueError(f'locationsFile argument is malformed: \"{locationsFile}\"')

        self.__locationsFile = locationsFile

    def getLocation(self, location: str):
        if location == None or len(location) == 0 or location.isspace():
            raise ValueError(f'location argument is malformed: \"{location}\"')

        if not os.path.exists(self.__locationsFile):
            raise FileNotFoundError(f'Locations file not found: \"{self.__locationsFile}\"')

        with open(self.__locationsFile, 'r') as file:
            jsonContents = json.load(file)

        if jsonContents == None:
            raise IOError(f'Error reading from locations file: \"{self.__locationsFile}\"')

        # TODO
