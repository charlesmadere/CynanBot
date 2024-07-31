from datetime import datetime, timedelta

from src.misc.simpleDateTime import SimpleDateTime


class TestSimpleDateTime:

    def test_add(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate) + timedelta(hours = 1)
        assert sdt == (someDate + timedelta(hours = 1))

    def test_equals(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert someDate == sdt

    def test_getDayInt(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getDayInt() == 25

    def test_getDayStr(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getDayStr() == '25'

    def test_getHourInt(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getHourInt() == 4

    def test_getHourStr(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getHourStr() == '04'

    def test_getMinuteInt(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getMinuteInt() == 55

    def test_getMinuteStr(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getMinuteStr() == '55'

    def test_getSecondInt(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getSecondInt() == 21

    def test_getSecondStr(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getSecondStr() == '21'

    def test_getYearInt(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getYearInt() == 2023

    def test_getYearStr(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getYearStr() == '2023'

    def test_getYearMonthDayStr(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert sdt.getYearMonthDayStr() == '2023/08/25'

    def test__repr(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate)
        assert str(someDate) == str(sdt)

    def test_sub(self):
        someDate = datetime.fromisoformat('2023-08-25T04:55:21+00:00')
        sdt = SimpleDateTime(someDate) - timedelta(minutes = 30)
        assert sdt == (someDate - timedelta(minutes = 30))
