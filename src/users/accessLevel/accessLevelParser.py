from typing import Any

from .accessLevel import AccessLevel
from .accessLevelParserInterface import AccessLevelJsonParserInterface
from ...misc import utils as utils


class AccessLevelJsonParser(AccessLevelJsonParserInterface):

    def parseAccessLevel(self,
        defaultTtsChatterAccessLevel: AccessLevel,
        accessLevelStr: str | Any | None
    ) -> AccessLevel:

        if utils.isValidStr(accessLevelStr) and accessLevelStr is not None:
            for accessLevel in AccessLevel:
                if accessLevelStr.casefold() == accessLevel.name.casefold():
                    return accessLevel

        return defaultTtsChatterAccessLevel