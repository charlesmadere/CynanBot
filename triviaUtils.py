from CynanBotCommon.trivia.absTriviaQuestion import AbsTriviaQuestion


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
