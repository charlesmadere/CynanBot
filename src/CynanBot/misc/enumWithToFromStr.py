from enum import Enum

from typing_extensions import Self

from CynanBot.misc import utils


class EnumWithToFromStr(Enum):
    """_summary_

    Enum with `fromStr` and `toStr` methods attached.
    """

    @classmethod
    def fromStr(cls, text: str) -> Self:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: "{text}"')

        try:
            return cls[text.upper()]
        except KeyError:
            raise ValueError(f'unknown {cls.__name__}: "{text}"')

    def toStr(self) -> str:
        return self.name.lower()
