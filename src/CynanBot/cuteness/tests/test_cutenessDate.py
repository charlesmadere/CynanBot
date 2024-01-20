from CynanBot.cuteness.cutenessDate import CutenessDate


class TestCutenessDate():

    def test_constructWithDecember2021String(self):
        cd = CutenessDate('2021-12')
        assert cd.getDatabaseString() == '2021-12'
        assert cd.getHumanString() == 'Dec 2021'

    def test_constructWithJanuary2024String(self):
        cd = CutenessDate('2024-01')
        assert cd.getDatabaseString() == '2024-01'
        assert cd.getHumanString() == 'Jan 2024'
