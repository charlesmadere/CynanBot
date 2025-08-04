from typing import Any

from .anivUserSettingsJsonParserInterface import AnivUserSettingsJsonParserInterface
from ...aniv.models.whichAnivUser import WhichAnivUser
from ...misc import utils as utils


class AnivUserSettingsJsonParser(AnivUserSettingsJsonParserInterface):

    def parseWhichAnivUser(
        self,
        whichAnivUser: str | Any | None,
    ) -> WhichAnivUser | None:
        if not utils.isValidStr(whichAnivUser):
            return None

        whichAnivUser = whichAnivUser.lower()

        match whichAnivUser:
            case 'acac': return WhichAnivUser.ACAC
            case 'aneev': return WhichAnivUser.ANEEV
            case 'aniv': return WhichAnivUser.ANIV
            case _: return None

    def requireWhichAnivUser(
        self,
        whichAnivUser: str | Any | None,
    ) -> WhichAnivUser:
        result = self.parseWhichAnivUser(whichAnivUser)

        if result is None:
            raise ValueError(f'Unable to parse \"{whichAnivUser}\" into WhichAnivUser value!')

        return result
