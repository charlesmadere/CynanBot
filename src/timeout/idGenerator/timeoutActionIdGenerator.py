import re
import uuid
from typing import Final, Pattern

from .timeoutActionIdGeneratorInterface import TimeoutActionIdGeneratorInterface


class TimeoutActionIdGenerator(TimeoutActionIdGeneratorInterface):

    def __init__(self):
        self.__idRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateActionId(self) -> str:
        actionId = str(uuid.uuid4())
        return self.__idRegEx.sub('', actionId)
