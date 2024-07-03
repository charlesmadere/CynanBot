from dataclasses import dataclass

from .triviaQuestionType import TriviaQuestionType
from .triviaSource import TriviaSource


@dataclass(frozen = True)
class TriviaQuestionReference():
    emote: str
    triviaId: str
    twitchChannel: str
    twitchChannelId: str
    triviaSource: TriviaSource
    triviaType: TriviaQuestionType
