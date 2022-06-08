import locale
import random
from typing import List

import CynanBotCommon.utils as utils
from CynanBotCommon.cuteness.cutenessResult import CutenessResult
from CynanBotCommon.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBotCommon.trivia.triviaScoreResult import TriviaScoreResult
from CynanBotCommon.trivia.triviaType import TriviaType


class TriviaUtils():

    def __init__(self):
        pass

    def getCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        newCuteness: CutenessResult,
        userNameThatRedeemed: str,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif newCuteness is None:
            raise ValueError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        prefix = f'{self.getRandomTriviaEmote()} Congratulations @{userNameThatRedeemed}, that\'s correct!'
        infix = f'Your new cuteness is {newCuteness.getCutenessStr()}.'

        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} 🎉 {infix} ✨ The correct answer was: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} 🎉 {infix} ✨ The correct answers were: {correctAnswersStr}'

    def getIncorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        userNameThatRedeemed: str,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        prefix = f'{self.getRandomTriviaEmote()} Sorry @{userNameThatRedeemed}, that\'s incorrect. {utils.getRandomSadEmoji()}'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    def getOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        userNameThatRedeemed: str,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        prefix = f'{self.getRandomTriviaEmote()} Sorry @{userNameThatRedeemed}, you\'re out of time. {utils.getRandomSadEmoji()}'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    def getRandomTriviaEmote(self) -> str:
        triviaEmotes: List[str] = [ '🏫', '🖍️', '✏️', '🧑‍🎓', '👨‍🎓', '👩‍🎓', '🧑‍🏫', '👨‍🏫', '👩‍🏫' ]
        return random.choice(triviaEmotes)

    def getResults(self, userName: str, triviaResult: TriviaScoreResult) -> str:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif triviaResult is None:
            raise ValueError(f'triviaResult argument is malformed: \"{triviaResult}\"')

        if triviaResult.getTotal() <= 0:
            return f'@{userName} has not played any trivia games 😿'

        gamesStr: str = 'games'
        if triviaResult.getTotal() == 1:
            gamesStr = 'game'

        winsStr: str = 'wins'
        if triviaResult.getTotalWins() == 1:
            winsStr = 'win'

        superTriviaWinsStr: str = ''
        if triviaResult.getSuperTriviaWins() > 1:
            superTriviaWinsStr = f' ({triviaResult.getSuperTriviaWinsStr()} of which are super trivia wins)'
        elif triviaResult.getSuperTriviaWins() == 1:
            superTriviaWinsStr = f' ({triviaResult.getSuperTriviaWinsStr()} of which is a super trivia win)'

        lossesStr: str = 'losses'
        if triviaResult.getTotalLosses() == 1:
            lossesStr = 'loss'

        ratioStr: str = f' ({triviaResult.getWinPercentStr()} wins)'

        streakStr: str = ''
        if triviaResult.getStreak() >= 3:
            streakStr = f'… and is on a {triviaResult.getAbsStreakStr()} game winning streak 😸'
        elif triviaResult.getStreak() <= -3:
            streakStr = f'… and is on a {triviaResult.getAbsStreakStr()} game losing streak 🙀'

        return f'@{userName} has played {triviaResult.getTotalStr()} trivia {gamesStr}, with {triviaResult.getTotalWinsStr()} {winsStr}{superTriviaWinsStr} and {triviaResult.getTotalLossesStr()} {lossesStr}{ratioStr}{streakStr}'

    def getSuperTriviaCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        newCuteness: CutenessResult,
        multiplier: int,
        points: int,
        userName: str,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif newCuteness is None:
            raise ValueError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidNum(multiplier):
            raise ValueError(f'multiplier argument is malformed: \"{multiplier}\"')
        elif not utils.isValidNum(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        pointsStr = locale.format_string("%d", points, grouping = True)
        multiplierStr = locale.format_string("%d", multiplier, grouping = True)
        prefix = f'{self.getRandomTriviaEmote()} CONGRATULATIONS @{userName}, that\'s correct!'
        infix = f'You earned {pointsStr} cuteness ({multiplierStr}x multiplier), so your new cuteness is {newCuteness.getCutenessStr()}.'

        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} 🎉 {infix} ✨ The correct answer was: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} 🎉 {infix} ✨ The correct answers were: {correctAnswersStr}'

    def getSuperTriviaOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        multiplier: int,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidNum(multiplier):
            raise ValueError(f'multiplier argument is malformed: \"{multiplier}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        multiplierStr = locale.format_string("%d", multiplier, grouping = True)
        prefix = f'{self.getRandomTriviaEmote()} Sorry everyone, y\'all are out of time… {utils.getRandomSadEmoji()} Goodbye {multiplierStr}x multiplier 👋…'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    def getSuperTriviaQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        multiplier: int,
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
        elif not utils.isValidNum(multiplier):
            raise ValueError(f'multiplier argument is malformed: \"{multiplier}\"')
        elif multiplier < 1:
            raise ValueError(f'multiplier argument is out of bounds: {multiplier}')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        triviaEmote = self.getRandomTriviaEmote()
        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)
        pointsStr = locale.format_string("%d", points, grouping = True)
        multiplierStr = locale.format_string("%d", multiplier, grouping = True)

        questionPrompt: str = None
        if triviaQuestion.getTriviaType() is TriviaType.QUESTION_ANSWER and triviaQuestion.hasCategory():
            questionPrompt = f'— category is {triviaQuestion.getCategory()} — {triviaQuestion.getQuestion()}'
        else:
            questionPrompt = f'— {triviaQuestion.getPrompt(delimiter)}'

        return f'{triviaEmote} EVERYONE can play! !superanswer in {delaySecondsStr}s for {pointsStr} points ({multiplierStr}x multiplier ✨) {questionPrompt}'

    def getTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        userNameThatRedeemed: str,
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

        return f'{triviaEmote} @{userNameThatRedeemed} !answer in {delaySecondsStr}s for {pointsStr} {pointsPlurality} {questionPrompt}'
