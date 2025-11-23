import re
from typing import Any, Collection, Final, Pattern

from frozendict import frozendict
from frozenlist import FrozenList

from .anivJsonMapperInterface import AnivJsonMapperInterface
from ..models.whichAnivUser import WhichAnivUser
from ...misc import utils as utils


class AnivJsonMapper(AnivJsonMapperInterface):

    def __init__(self):
        self.__whichAnivUserRegExes: Final[frozendict[WhichAnivUser, Collection[Pattern]]] = self.__buildWhichAnivUserRegExes()

    def __buildWhichAnivUserRegExes(self) -> frozendict[WhichAnivUser, Collection[Pattern]]:
        acac: FrozenList[Pattern] = FrozenList()
        acac.append(re.compile(r'^\s*a(?:\s+|_|-)?c(?:\s+|_|-)?a(?:\s+|_|-)?c\s*$', re.IGNORECASE))
        acac.freeze()

        albeeev: FrozenList[Pattern] = FrozenList()
        albeeev.append(re.compile(r'^\s*a(?:\s+|_|-)?l(?:\s+|_|-)?b(?:\s+|_|-)?e(?:\s+|_|-)?e(?:\s+|_|-)?e(?:\s+|_|-)?v\s*$', re.IGNORECASE))
        albeeev.freeze()

        aneev: FrozenList[Pattern] = FrozenList()
        aneev.append(re.compile(r'^\s*a(?:\s+|_|-)?n(?:\s+|_|-)?e(?:\s+|_|-)?e(?:\s+|_|-)?v\s*$', re.IGNORECASE))
        aneev.freeze()

        aniv: FrozenList[Pattern] = FrozenList()
        aniv.append(re.compile(r'^\s*a(?:\s+|_|-)?n(?:\s+|_|-)?i(?:\s+|_|-)?v\s*$', re.IGNORECASE))
        aniv.freeze()

        return frozendict({
            WhichAnivUser.ACAC: acac,
            WhichAnivUser.ALBEEEV: albeeev,
            WhichAnivUser.ANEEV: aneev,
            WhichAnivUser.ANIV: aniv,
        })

    def parseWhichAnivUser(
        self,
        string: str | Any | None,
    ) -> WhichAnivUser | None:
        if not utils.isValidStr(string):
            return None

        for whichAnivUser, regExes in self.__whichAnivUserRegExes.items():
            for regEx in regExes:
                if regEx.fullmatch(string) is not None:
                    return whichAnivUser

        return None

    def requireWhichAnivUser(
        self,
        string: str | Any | None,
    ) -> WhichAnivUser:
        result = self.parseWhichAnivUser(string)

        if result is None:
            raise ValueError(f'Unable to parse WhichAnivUser from string: \"{string}\"')

        return result
