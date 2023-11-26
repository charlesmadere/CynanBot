from typing import List, Optional

from CynanBot.storage.linesReaderInterface import LinesReaderInterface


class LinesStaticReader(LinesReaderInterface):

    def __init__(self, lines: Optional[List[str]]):
        self.__lines: Optional[List[str]] = lines

    def readLines(self) -> Optional[List[str]]:
        return self.__lines

    async def readLinesAsync(self) -> Optional[List[str]]:
        return self.__lines
