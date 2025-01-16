from enum import auto

from typing_extensions import override

from ...misc import utils as utils
from ...misc.enumWithToFromStr import EnumWithToFromStr


class TriviaSource(EnumWithToFromStr):

    BONGO = auto()
    FUNTOON = auto()
    GLACIAL = auto()
    J_SERVICE = auto()
    LORD_OF_THE_RINGS = auto()
    MILLIONAIRE = auto()
    OPEN_TRIVIA_DATABASE = auto()
    OPEN_TRIVIA_QA = auto()
    POKE_API = auto()
    QUIZ_API = auto()
    THE_QUESTION_CO = auto()
    TRIVIA_DATABASE = auto()
    WILL_FRY_TRIVIA = auto()
    WWTBAM = auto()

    @override
    @classmethod
    def fromStr(cls, text: str):
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        match text:
            case 'open_trivia': return TriviaSource.OPEN_TRIVIA_DATABASE
            case 'will_fry_trivia_api': return TriviaSource.WILL_FRY_TRIVIA
            case _: return super().fromStr(text)

    def isLocal(self) -> bool:
        match self:
            case TriviaSource.BONGO: return False
            case TriviaSource.FUNTOON: return False
            case TriviaSource.GLACIAL: return True
            case TriviaSource.J_SERVICE: return False
            case TriviaSource.LORD_OF_THE_RINGS: return True
            case TriviaSource.MILLIONAIRE: return True
            case TriviaSource.OPEN_TRIVIA_DATABASE: return False
            case TriviaSource.OPEN_TRIVIA_QA: return True
            case TriviaSource.POKE_API: return False
            case TriviaSource.THE_QUESTION_CO: return True
            case TriviaSource.TRIVIA_DATABASE: return True
            case TriviaSource.WILL_FRY_TRIVIA: return False
            case TriviaSource.WWTBAM: return True
            case _: raise RuntimeError(f'unknown TriviaSource: \"{self}\"')

    @override
    def toStr(self) -> str:
        return super().toStr().upper()
