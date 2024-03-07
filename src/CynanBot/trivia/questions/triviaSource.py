from enum import auto

from typing_extensions import override

import CynanBot.misc.utils as utils
from CynanBot.misc.enumWithToFromStr import EnumWithToFromStr


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
            raise ValueError(f'text argument is malformed: \"{text}\"')

        text = text.lower()

        if text == 'open_trivia':
            return TriviaSource.OPEN_TRIVIA_DATABASE
        elif text == 'will_fry_trivia_api':
            return TriviaSource.WILL_FRY_TRIVIA
        return super().fromStr(text)

    def isLocal(self) -> bool:
        if self is TriviaSource.BONGO:
            return False
        elif self is TriviaSource.FUNTOON:
            return False
        elif self is TriviaSource.GLACIAL:
            return True
        elif self is TriviaSource.J_SERVICE:
            return False
        elif self is TriviaSource.LORD_OF_THE_RINGS:
            return True
        elif self is TriviaSource.MILLIONAIRE:
            return True
        elif self is TriviaSource.OPEN_TRIVIA_DATABASE:
            return False
        elif self is TriviaSource.OPEN_TRIVIA_QA:
            return True
        elif self is TriviaSource.POKE_API:
            return False
        elif self is TriviaSource.THE_QUESTION_CO:
            return True
        elif self is TriviaSource.TRIVIA_DATABASE:
            return True
        elif self is TriviaSource.WILL_FRY_TRIVIA:
            return False
        elif self is TriviaSource.WWTBAM:
            return True
        else:
            raise RuntimeError(f'unknown TriviaSource: \"{self}\"')

    @override
    def toStr(self) -> str:
        return super().toStr().upper()
