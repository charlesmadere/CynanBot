import locale
import random
from typing import List

import CynanBotCommon.utils as utils
from CynanBotCommon.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBotCommon.trivia.triviaScoreResult import TriviaScoreResult
from CynanBotCommon.trivia.triviaType import TriviaType


class TriviaUtils():

    def __init__(self):
        pass

    def getAnswerReveal(self, question: AbsTriviaQuestion, delimiter: str = '; ') -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'The correct answers are: {correctAnswersStr}'

    def getRandomTriviaEmote(self) -> str:
        triviaEmotes: List[str] = [ '🏫', '🖍️', '✏️', '🧑‍🎓', '👨‍🎓', '👩‍🎓', '🧑‍🏫', '👨‍🏫', '👩‍🏫' ]
        return random.choice(triviaEmotes)

    def getResults(self, userName: str, triviaResult: TriviaScoreResult) -> str:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif triviaResult is None:
            raise ValueError(f'triviaResult argument is malformed: \"{triviaResult}\"')

        if triviaResult.getTotal() <= 0:
            return f'{userName} has not played any trivia games 😿'

        gamesStr = 'games'
        if triviaResult.getTotal() == 1:
            gamesStr = 'game'

        winsStr = 'wins'
        if triviaResult.getTotalWins() == 1:
            winsStr = 'win'

        lossesStr = 'losses'
        if triviaResult.getTotalLosses() == 1:
            lossesStr = 'loss'

        ratioStr = f' ({triviaResult.getWinPercentStr()} wins)'

        streakStr = ''
        if triviaResult.getStreak() >= 3:
            streakStr = f'... and is on a {triviaResult.getAbsStreakStr()} game winning streak 😸'
        elif triviaResult.getStreak() <= -3:
            streakStr = f'... and is on a {triviaResult.getAbsStreakStr()} game losing streak 🙀'

        return f'{userName} has played {triviaResult.getTotalStr()} trivia {gamesStr}, with {triviaResult.getTotalWinsStr()} {winsStr} and {triviaResult.getTotalLossesStr()} {lossesStr}{ratioStr}{streakStr}'

    def getTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        delimiter: str = ' '
    ) -> str:
        if triviaQuestion is None:
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidNum(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1:
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidNum(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif points < 1:
            raise ValueError(f'points argument is out of bounds: {points}')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        triviaEmote = self.getRandomTriviaEmote()
        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)
        pointsStr = locale.format_string("%d", points, grouping = True)

        pointsPlurality: str = None
        if points == 1:
            pointsPlurality = 'point'
        else:
            pointsPlurality = 'points'

        questionPrompt: str = None
        if triviaQuestion.getTriviaType() is TriviaType.QUESTION_ANSWER and triviaQuestion.hasCategory():
            questionPrompt = f'(category is \"{triviaQuestion.getCategory()}\") — {triviaQuestion.getQuestion()}'
        else:
            questionPrompt = f'— {triviaQuestion.getPrompt(delimiter)}'

        return f'{triviaEmote} !answer in {delaySecondsStr}s for {pointsStr} {pointsPlurality} {questionPrompt}'
