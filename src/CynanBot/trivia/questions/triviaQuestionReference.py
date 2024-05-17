from dataclasses import dataclass

from CynanBot.trivia.questions.triviaQuestionType import TriviaQuestionType
from CynanBot.trivia.questions.triviaSource import TriviaSource


@dataclass(frozen = True)
class TriviaQuestionReference():
    emote: str
    triviaId: str
    twitchChannel: str
    twitchChannelId: str
    originalTriviaSource: TriviaSource | None
    triviaSource: TriviaSource
    triviaType: TriviaQuestionType
