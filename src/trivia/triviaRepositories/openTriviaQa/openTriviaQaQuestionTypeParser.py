from typing import Any

from .exceptions import UnknownOpenTriviaQaQuestionTypeException
from .openTriviaQaQuestionType import OpenTriviaQaQuestionType
from .openTriviaQaQuestionTypeParserInterface import OpenTriviaQaQuestionTypeParserInterface
from ....misc import utils as utils
from ....timber.timberInterface import TimberInterface


class OpenTriviaQaQuestionTypeParser(OpenTriviaQaQuestionTypeParserInterface):

    def __init__(self, timber: TimberInterface):
        if not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')

        self.__timber: TimberInterface = timber

    async def parse(
        self,
        questionType: str | Any | None
    ) -> OpenTriviaQaQuestionType | None:
        if not utils.isValidStr(questionType):
            return None

        questionType = questionType.lower()

        match questionType:
            case 'multiple-choice': return OpenTriviaQaQuestionType.MULTIPLE_CHOICE
            case 'true-false': return OpenTriviaQaQuestionType.BOOLEAN
            case _:
                self.__timber.log('OpenTriviaQaQuestionTypeParser', f'Encountered unknown OpenTriviaQaQuestionType: \"{questionType}\"')
                return None

    async def require(
        self,
        questionType: str | Any | None
    ) -> OpenTriviaQaQuestionType:
        result = await self.parse(questionType)

        if result is None:
            raise UnknownOpenTriviaQaQuestionTypeException(f'Unable to parse \"{questionType}\" into OpenTriviaQaQuestionType value!')

        return result
