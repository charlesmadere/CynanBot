import re
import uuid
from typing import Final, Pattern

from .voicemailIdGeneratorInterface import VoicemailIdGeneratorInterface


class VoicemailIdGenerator(VoicemailIdGeneratorInterface):

    def __init__(self):
        self.__idRegEx: Final[Pattern] = re.compile(r'[^a-z0-9]', re.IGNORECASE)

    async def generateVoicemailId(self) -> str:
        voicemailId = str(uuid.uuid4())
        return self.__idRegEx.sub('', voicemailId)[:3].lower()
