import pytest

from src.trivia.questions.triviaQuestionType import TriviaQuestionType


class TestTriviaQuestionType():

    def test_fromStr_withEmptyString(self):
        result: TriviaQuestionType | None = None

        with pytest.raises(TypeError):
            result = TriviaQuestionType.fromStr('')

        assert result is None

    def test_fromStr_withMultipleChoiceStrings(self):
        strings: list[str] = [ 'multiple', 'multiple choice', 'multiple-choice', 'multiple_choice' ]

        for string in strings:
            result = TriviaQuestionType.fromStr(string)
            assert result is TriviaQuestionType.MULTIPLE_CHOICE

    def test_fromStr_withNone(self):
        result: TriviaQuestionType | None = None

        with pytest.raises(TypeError):
            result = TriviaQuestionType.fromStr(None) # type: ignore

        assert result is None

    def test_fromStr_withQuestionAnswerStrings(self):
        strings: list[str] = [ 'question answer', 'question-answer', 'question_answer' ]

        for string in strings:
            result = TriviaQuestionType.fromStr(string)
            assert result is TriviaQuestionType.QUESTION_ANSWER

    def test_fromStr_withTrueFalseStrings(self):
        strings: list[str] = [ 'bool', 'boolean', 'true false', 'true-false', 'true_false' ]

        for string in strings:
            result = TriviaQuestionType.fromStr(string)
            assert result is TriviaQuestionType.TRUE_FALSE

    def test_fromStr_withWhitespaceString(self):
        result: TriviaQuestionType | None = None

        with pytest.raises(TypeError):
            result = TriviaQuestionType.fromStr(' ')

        assert result is None

    def test_toStr_withMultipleChoice(self):
        result = TriviaQuestionType.MULTIPLE_CHOICE.toStr()
        assert result == 'multiple-choice'

    def test_toStr_withQuestionAnswer(self):
        result = TriviaQuestionType.QUESTION_ANSWER.toStr()
        assert result == 'question-answer'

    def test_toStr_withTrueFalse(self):
        result = TriviaQuestionType.TRUE_FALSE.toStr()
        assert result == 'true-false'
