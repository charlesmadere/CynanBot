from typing import List

import CynanBot.misc.utils as utils
from CynanBot.language.jishoVariant import JishoVariant


class JishoResult():

    def __init__(
        self,
        variants: List[JishoVariant],
        initialQuery: str
    ):
        if not utils.hasItems(variants):
            raise ValueError(f'variants argument is malformed: \"{variants}\"')
        if not utils.isValidStr(initialQuery):
            raise ValueError(f'initialQuery argument is malformed: \"{initialQuery}\"')

        self.__variants: List[JishoVariant] = variants
        self.__initialQuery: str = initialQuery

    def getInitialQuery(self) -> str:
        return self.__initialQuery

    def getVariants(self) -> List[JishoVariant]:
        return self.__variants

    def toStrList(self, definitionDelimiter: str = ', ') -> List[str]:
        assert isinstance(definitionDelimiter, str), f"malformed {definitionDelimiter=}"

        strings: List[str] = list()
        for variant in self.__variants:
            strings.append(variant.toStr(definitionDelimiter))

        return strings
