from typing import Any

from .triviaSourceParserInterface import TriviaSourceParserInterface
from ..questions.triviaSource import TriviaSource
from ...misc import utils as utils


class TriviaSourceParser(TriviaSourceParserInterface):

    async def parse(self, triviaSource: str | Any | None) -> TriviaSource:
        if not utils.isValidStr(triviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        triviaSource = triviaSource.lower()

        match triviaSource:
            case 'bongo': return TriviaSource.BONGO
            case 'funtoon': return TriviaSource.FUNTOON
            case 'glacial': return TriviaSource.GLACIAL
            case 'j_service': return TriviaSource.J_SERVICE
            case 'lord_of_the_rings': return TriviaSource.LORD_OF_THE_RINGS
            case 'millionaire': return TriviaSource.MILLIONAIRE
            case 'open_trivia': return TriviaSource.OPEN_TRIVIA_DATABASE
            case 'open_trivia_database': return TriviaSource.OPEN_TRIVIA_DATABASE
            case 'open_trivia_qa': return TriviaSource.OPEN_TRIVIA_QA
            case 'poke_api': return TriviaSource.POKE_API
            case 'quiz_api': return TriviaSource.QUIZ_API
            case 'the_question_co': return TriviaSource.THE_QUESTION_CO
            case 'trivia_database': return TriviaSource.TRIVIA_DATABASE
            case 'will_fry_trivia': return TriviaSource.WILL_FRY_TRIVIA
            case 'will_fry_trivia_api': return TriviaSource.WILL_FRY_TRIVIA
            case 'wwtbam': return TriviaSource.WWTBAM
            case _: raise ValueError(f'Encountered unknown TriviaSource value: \"{triviaSource}\"')

    async def serialize(self, triviaSource: TriviaSource) -> str:
        if not isinstance(triviaSource, TriviaSource):
            raise TypeError(f'triviaSource argument is malformed: \"{triviaSource}\"')

        match triviaSource:
            case TriviaSource.BONGO: return 'bongo'
            case TriviaSource.FUNTOON: return 'funtoon'
            case TriviaSource.GLACIAL: return 'glacial'
            case TriviaSource.J_SERVICE: return 'j_service'
            case TriviaSource.LORD_OF_THE_RINGS: return 'lord_of_the_rings'
            case TriviaSource.MILLIONAIRE: return 'millionaire'
            case TriviaSource.OPEN_TRIVIA_DATABASE: return 'open_trivia_database'
            case TriviaSource.OPEN_TRIVIA_QA: return 'open_trivia_qa'
            case TriviaSource.POKE_API: return 'poke_api'
            case TriviaSource.QUIZ_API: return 'quiz_api'
            case TriviaSource.THE_QUESTION_CO: return 'the_question_co'
            case TriviaSource.TRIVIA_DATABASE: return 'trivia_database'
            case TriviaSource.WILL_FRY_TRIVIA: return 'will_fry_trivia'
            case TriviaSource.WWTBAM: return 'wwtbam'
            case _: raise ValueError(f'Encountered unknown TriviaSource: \"{triviaSource}\"')
