from typing import Any

from .jsonReaderInterface import JsonReaderInterface


class JsonStaticReader(JsonReaderInterface):

    def __init__(self, jsonContents: dict[Any, Any] | None):
        self.__jsonContents: dict[Any, Any] | None = jsonContents
        self.__isDeleted: bool = False

    def deleteFile(self):
        self.__isDeleted = True

    async def deleteFileAsync(self):
        self.deleteFile()

    def fileExists(self) -> bool:
        return not self.__isDeleted

    async def fileExistsAsync(self) -> bool:
        return self.fileExists()

    def readJson(self) -> dict[Any, Any] | None:
        if self.__isDeleted:
            return None
        else:
            return self.__jsonContents

    async def readJsonAsync(self) -> dict[Any, Any] | None:
        return self.readJson()

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> dict[str, Any]:
        return {
            'isDeleted': self.__isDeleted,
            'jsonContents': self.__jsonContents,
        }
