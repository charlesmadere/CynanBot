from typing import List

from CynanBot.trivia.triviaType import TriviaType


class TestTriviaType():

    def test_fromStr_withEmptyString(self):
        result: TriviaType = None
        exception: Exception = None

        try:
            result = TriviaType.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_fromStr_withMultipleChoiceStrings(self):
        strings: List[str] = [ 'multiple', 'multiple choice', 'multiple-choice', 'multiple_choice' ]

        for string in strings:
            result = TriviaType.fromStr(string)
            assert result is TriviaType.MULTIPLE_CHOICE

    def test_fromStr_withNone(self):
        result: TriviaType = None
        exception: Exception = None

        try:
            result = TriviaType.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_fromStr_withQuestionAnswerStrings(self):
        strings: List[str] = [ 'question answer', 'question-answer', 'question_answer' ]

        for string in strings:
            result = TriviaType.fromStr(string)
            assert result is TriviaType.QUESTION_ANSWER

    def test_fromStr_withTrueFalseStrings(self):
        strings: List[str] = [ 'bool', 'boolean', 'true false', 'true-false', 'true_false' ]

        for string in strings:
            result = TriviaType.fromStr(string)
            assert result is TriviaType.TRUE_FALSE

    def test_fromStr_withWhitespaceString(self):
        result: TriviaType = None
        exception: Exception = None

        try:
            result = TriviaType.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_toStr_withMultipleChoice(self):
        result = TriviaType.MULTIPLE_CHOICE.toStr()
        assert result == 'multiple-choice'

    def test_toStr_withQuestionAnswer(self):
        result = TriviaType.QUESTION_ANSWER.toStr()
        assert result == 'question-answer'

    def test_toStr_withTrueFalse(self):
        result = TriviaType.TRUE_FALSE.toStr()
        assert result == 'true-false'
