from CynanBot.trivia.questions.triviaSource import TriviaSource


class TestTriviaSource():

    def test_fromStr_withEmptyString(self):
        result: TriviaSource = None
        exception: Exception = None

        try:
            result = TriviaSource.fromStr('')
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_fromStr_withNone(self):
        result: TriviaSource = None
        exception: Exception = None

        try:
            result = TriviaSource.fromStr(None)
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_fromStr_withBongoString(self):
        result = TriviaSource.fromStr('bongo')
        assert result is TriviaSource.BONGO

    def test_fromStr_withFuntoonString(self):
        result = TriviaSource.fromStr('funtoon')
        assert result is TriviaSource.FUNTOON

    def test_fromStr_withJServiceString(self):
        result = TriviaSource.fromStr('j_service')
        assert result is TriviaSource.J_SERVICE

    def test_fromStr_withLordOfTheRingsString(self):
        result = TriviaSource.fromStr('lord_of_the_rings')
        assert result is TriviaSource.LORD_OF_THE_RINGS

    def test_fromStr_withMillionaireString(self):
        result = TriviaSource.fromStr('millionaire')
        assert result is TriviaSource.MILLIONAIRE

    def test_fromStr_withOpenTriviaDatabaseString(self):
        result = TriviaSource.fromStr('open_trivia')
        assert result is TriviaSource.OPEN_TRIVIA_DATABASE

        result = TriviaSource.fromStr('open_trivia_database')
        assert result is TriviaSource.OPEN_TRIVIA_DATABASE

    def test_fromStr_withOpenTriviaQaString(self):
        result = TriviaSource.fromStr('open_trivia_qa')
        assert result is TriviaSource.OPEN_TRIVIA_QA

    def test_fromStr_withPokeApiString(self):
        result = TriviaSource.fromStr('poke_api')
        assert result is TriviaSource.POKE_API

    def test_fromStr_withQuizApiString(self):
        result = TriviaSource.fromStr('quiz_api')
        assert result is TriviaSource.QUIZ_API

    def test_fromStr_withTheQuestionCoString(self):
        result = TriviaSource.fromStr('the_question_co')
        assert result is TriviaSource.THE_QUESTION_CO

    def test_fromStr_withTriviaDatabaseString(self):
        result = TriviaSource.fromStr('trivia_database')
        assert result is TriviaSource.TRIVIA_DATABASE

    def test_fromStr_withWillFryTriviaString(self):
        result = TriviaSource.fromStr('will_fry_trivia')
        assert result is TriviaSource.WILL_FRY_TRIVIA

        result = TriviaSource.fromStr('will_fry_trivia_api')
        assert result is TriviaSource.WILL_FRY_TRIVIA

    def test_fromStr_withWwtbamString(self):
        result = TriviaSource.fromStr('wwtbam')
        assert result is TriviaSource.WWTBAM

    def test_fromStr_withWhitespaceString(self):
        result: TriviaSource = None
        exception: Exception = None

        try:
            result = TriviaSource.fromStr(' ')
        except Exception as e:
            exception = e

        assert result is None
        assert exception is not None
        assert isinstance(exception, ValueError)

    def test_toStr_withBongo(self):
        result = TriviaSource.BONGO.toStr()
        assert result == 'BONGO'

    def test_toStr_withFuntoon(self):
        result = TriviaSource.FUNTOON.toStr()
        assert result == 'FUNTOON'

    def test_toStr_withJService(self):
        result = TriviaSource.J_SERVICE.toStr()
        assert result == 'J_SERVICE'

    def test_toStr_withLordOfTheRings(self):
        result = TriviaSource.LORD_OF_THE_RINGS.toStr()
        assert result == 'LORD_OF_THE_RINGS'

    def test_toStr_withMillionaire(self):
        result = TriviaSource.MILLIONAIRE.toStr()
        assert result == 'MILLIONAIRE'

    def test_toStr_withOpenTriviaDatabase(self):
        result = TriviaSource.OPEN_TRIVIA_DATABASE.toStr()
        assert result == 'OPEN_TRIVIA_DATABASE'

    def test_toStr_withOpenTriviaQa(self):
        result = TriviaSource.OPEN_TRIVIA_QA.toStr()
        assert result == 'OPEN_TRIVIA_QA'

    def test_toStr_withPokeApi(self):
        result = TriviaSource.POKE_API.toStr()
        assert result == 'POKE_API'

    def test_toStr_withQuizApi(self):
        result = TriviaSource.QUIZ_API.toStr()
        assert result == 'QUIZ_API'

    def test_toStr_withTheQuestionCo(self):
        result = TriviaSource.THE_QUESTION_CO.toStr()
        assert result == 'THE_QUESTION_CO'

    def test_toStr_withWillFryTriviaApi(self):
        result = TriviaSource.WILL_FRY_TRIVIA.toStr()
        assert result == 'WILL_FRY_TRIVIA'

    def test_toStr_withWwtbam(self):
        result = TriviaSource.WWTBAM.toStr()
        assert result == 'WWTBAM'
