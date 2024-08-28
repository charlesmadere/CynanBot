import re
import uuid
from typing import Pattern

from .crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface


class CrowdControlIdGenerator(CrowdControlIdGeneratorInterface):

    def __init__(self):
        self.__idRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateActionId(self) -> str:
        randomUuid = str(uuid.uuid4())
        randomUuid = self.__idRegEx.sub('', randomUuid)
        return randomUuid.casefold()
