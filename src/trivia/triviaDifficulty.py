from __future__ import annotations

from enum import Enum, auto

from ..misc import utils as utils


class TriviaDifficulty(Enum):

    EASY = auto()
    HARD = auto()
    MEDIUM = auto()
    UNKNOWN = auto()

    @classmethod
    def fromInt(cls, number: int | None) -> TriviaDifficulty:
        if not utils.isValidInt(number):
            return TriviaDifficulty.UNKNOWN

        match number:
            case 1: return TriviaDifficulty.EASY
            case 2: return TriviaDifficulty.MEDIUM
            case 3: return TriviaDifficulty.HARD
            case _: return TriviaDifficulty.UNKNOWN

    @classmethod
    def fromStr(cls, text: str | None):
        if not utils.isValidStr(text):
            return TriviaDifficulty.UNKNOWN

        text = text.lower()

        match text:
            case 'easy': return TriviaDifficulty.EASY
            case 'hard': return TriviaDifficulty.HARD
            case 'medium': return TriviaDifficulty.MEDIUM
            case _: return TriviaDifficulty.UNKNOWN

    def toInt(self) -> int:
        match self:
            case TriviaDifficulty.EASY: return 1
            case TriviaDifficulty.MEDIUM: return 2
            case TriviaDifficulty.HARD: return 3
            case TriviaDifficulty.UNKNOWN: return 0
            case _: raise RuntimeError(f'unknown TriviaDifficulty: \"{self}\"')

    def toStr(self) -> str:
        match self:
            case TriviaDifficulty.EASY: return 'easy'
            case TriviaDifficulty.HARD: return 'hard'
            case TriviaDifficulty.MEDIUM: return 'medium'
            case TriviaDifficulty.UNKNOWN: return 'unknown'
            case _: raise RuntimeError(f'unknown TriviaDifficulty: \"{self}\"')
