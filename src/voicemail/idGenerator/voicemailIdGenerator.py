import re
import uuid
from typing import Pattern

from .voicemailIdGeneratorInterface import VoicemailIdGeneratorInterface


class VoicemailIdGenerator(VoicemailIdGeneratorInterface):

    def __init__(self):
        self.__idRegEx: Pattern = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateVoicemailId(self) -> str:
        voicemailId = str(uuid.uuid4())
        return self.__idRegEx.sub('', voicemailId)
