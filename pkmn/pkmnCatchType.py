from enum import Enum, auto

try:
    import CynanBotCommon.utils as utils
except:
    from ...CynanBotCommon.utils import utils


class PkmnCatchType(Enum):

    GREAT = auto()
    NORMAL = auto()
    ULTRA = auto()

    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'great':
            return PkmnCatchType.GREAT
        elif text == 'normal':
            return PkmnCatchType.NORMAL
        elif text == 'ultra':
            return PkmnCatchType.ULTRA
        else:
            raise ValueError(f'unknown PkmnCatchType: \"{text}\"')

    def getSortOrder(self) -> int:
        if self is PkmnCatchType.GREAT:
            return 1
        elif self is PkmnCatchType.NORMAL:
            return 0
        elif self is PkmnCatchType.ULTRA:
            return 2
        else:
            raise RuntimeError(f'unknown PkmnCatchType: \"{self}\"')

    def toStr(self) -> str:
        if self is PkmnCatchType.GREAT:
            return 'great'
        elif self is PkmnCatchType.NORMAL:
            return 'normal'
        elif self is PkmnCatchType.ULTRA:
            return 'ultra'
        else:
            raise RuntimeError(f'unknown PkmnCatchType: \"{self}\"')
