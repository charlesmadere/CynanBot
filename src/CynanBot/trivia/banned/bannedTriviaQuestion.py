from dataclasses import dataclass

from CynanBot.trivia.questions.triviaSource import TriviaSource


@dataclass(frozen = True)
class BannedTriviaQuestion():
    triviaId: str
    userId: str
    userName: str
    triviaSource: TriviaSource
