from src.recurringActions.actions.recurringActionType import RecurringActionType


class TestRecurringActionType:

    def test_defaultRecurringActionTimingMinutes(self):
        timingMinutes: list[int] = list()

        for actionType in RecurringActionType:
            timingMinutes.append(actionType.defaultRecurringActionTimingMinutes)

        assert len(timingMinutes) == len(RecurringActionType)

    def test_humanReadableString(self):
        strings: set[str] = set()

        for actionType in RecurringActionType:
            strings.add(actionType.humanReadableString)

        assert len(strings) == len(RecurringActionType)

    def test_humanReadableString_withCuteness(self):
        result = RecurringActionType.CUTENESS.humanReadableString
        assert result == 'Cuteness'

    def test_humanReadableString_withSuperTrivia(self):
        result = RecurringActionType.SUPER_TRIVIA.humanReadableString
        assert result == 'Super Trivia'

    def test_humanReadableString_withWeather(self):
        result = RecurringActionType.WEATHER.humanReadableString
        assert result == 'Weather'

    def test_humanReadableString_withWordOfTheDay(self):
        result = RecurringActionType.WORD_OF_THE_DAY.humanReadableString
        assert result == 'Word of the Day'

    def test_minimumRecurringActionTimingMinutes(self):
        timingMinutes: list[int] = list()

        for actionType in RecurringActionType:
            timingMinutes.append(actionType.minimumRecurringActionTimingMinutes)

        assert len(timingMinutes) == len(RecurringActionType)
