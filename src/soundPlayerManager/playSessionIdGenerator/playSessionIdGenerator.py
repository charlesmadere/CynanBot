import re
import uuid
from typing import Pattern

from .playSessionIdGeneratorInterface import PlaySessionIdGeneratorInterface


class PlaySessionIdGenerator(PlaySessionIdGeneratorInterface):

    def __init__(self):
        self.__idRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generatePlaySessionId(self) -> str:
        playSessionId = str(uuid.uuid4())
        return self.__idRegEx.sub('', playSessionId)
