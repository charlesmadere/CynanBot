from typing import Any

from .triviaDifficultyParserInterface import TriviaDifficultyParserInterface
from ..triviaDifficulty import TriviaDifficulty
from ...misc import utils as utils


class TriviaDifficultyParser(TriviaDifficultyParserInterface):

    async def parse(
        self,
        triviaDifficulty: int | str | Any | None
    ) -> TriviaDifficulty:
        result: TriviaDifficulty | None = None

        if utils.isValidInt(triviaDifficulty):
            result = await self.__parseInt(triviaDifficulty)
        elif utils.isValidStr(triviaDifficulty):
            result = await self.__parseString(triviaDifficulty)

        if result is None:
            raise ValueError(f'Encountered unknown TriviaDifficulty: \"{triviaDifficulty}\"')

        return result

    async def __parseInt(self, triviaDifficulty: int) -> TriviaDifficulty | None:
        match triviaDifficulty:
            case 1: return TriviaDifficulty.EASY
            case 2: return TriviaDifficulty.MEDIUM
            case 3: return TriviaDifficulty.HARD
            case _: return TriviaDifficulty.UNKNOWN

    async def __parseString(self, triviaDifficulty: str) -> TriviaDifficulty | None:
        match triviaDifficulty:
            case 'easy': return TriviaDifficulty.EASY
            case 'medium': return TriviaDifficulty.MEDIUM
            case 'hard': return TriviaDifficulty.HARD
            case _: return TriviaDifficulty.UNKNOWN
