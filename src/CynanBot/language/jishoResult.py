import CynanBot.misc.utils as utils
from CynanBot.language.jishoVariant import JishoVariant


class JishoResult():

    def __init__(
        self,
        variants: list[JishoVariant],
        initialQuery: str
    ):
        if not utils.hasItems(variants):
            raise ValueError(f'variants argument is malformed: \"{variants}\"')
        elif not utils.isValidStr(initialQuery):
            raise ValueError(f'initialQuery argument is malformed: \"{initialQuery}\"')

        self.__variants: list[JishoVariant] = variants
        self.__initialQuery: str = initialQuery

    def getInitialQuery(self) -> str:
        return self.__initialQuery

    def getVariants(self) -> list[JishoVariant]:
        return self.__variants

    def toStrList(self, definitionDelimiter: str = ', ') -> list[str]:
        if not isinstance(definitionDelimiter, str):
            raise ValueError(f'definitionDelimiter argument is malformed: \"{definitionDelimiter}\"')

        strings: list[str] = list()
        for variant in self.__variants:
            strings.append(variant.toStr(definitionDelimiter))

        return strings
