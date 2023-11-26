from typing import Set

import misc.utils as utils


class EmojiInfo():

    def __init__(
        self,
        codes: Set[str],
        category: str,
        emoji: str,
        name: str,
        subCategory: str
    ):
        if not isinstance(codes, Set) or not utils.hasItems(codes):
            raise ValueError(f'codes argument is malformed: \"{codes}\"')
        elif not utils.isValidStr(category):
            raise ValueError(f'category argument is malformed: \"{category}\"')
        elif not utils.isValidStr(emoji):
            raise ValueError(f'emoji argument is malformed: \"{emoji}\"')
        elif not utils.isValidStr(name):
            raise ValueError(f'name argument is malformed: \"{name}\"')
        elif not utils.isValidStr(subCategory):
            raise ValueError(f'subCategory argument is malformed: \"{subCategory}\"')

        self.__codes: Set[str] = codes
        self.__category: str = category
        self.__emoji: str = emoji
        self.__name: str = name
        self.__subCategory: str = subCategory

    def getCategory(self) -> str:
        return self.__category

    def getCodes(self) -> Set[str]:
        return self.__codes

    def getEmoji(self) -> str:
        return self.__emoji

    def getName(self) -> str:
        return self.__name

    def getSubCategory(self) -> str:
        return self.__subCategory
