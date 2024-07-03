from .linesReaderInterface import LinesReaderInterface


class LinesStaticReader(LinesReaderInterface):

    def __init__(self, lines: list[str] | None):
        self.__lines: list[str] | None = lines

    def readLines(self) -> list[str] | None:
        return self.__lines

    async def readLinesAsync(self) -> list[str] | None:
        return self.__lines
