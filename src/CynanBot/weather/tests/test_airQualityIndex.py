from typing import Optional

from CynanBot.weather.airQualityIndex import AirQualityIndex


class TestAirQualityIndex():

    def test_fromInt_withNone(self):
        result: Optional[AirQualityIndex] = None
        exception: Optional[Exception] = None

        try:
            result = AirQualityIndex.fromInt(None)
        except Exception as e:
            exception = e

        assert result is None
        assert isinstance(exception, Exception)

    def test_fromInt_with0(self):
        result = AirQualityIndex.fromInt(0)
        assert result is AirQualityIndex.GOOD

    def test_fromInt_with1(self):
        result = AirQualityIndex.fromInt(1)
        assert result is AirQualityIndex.GOOD

    def test_fromInt_with2(self):
        result = AirQualityIndex.fromInt(2)
        assert result is AirQualityIndex.FAIR

    def test_fromInt_with3(self):
        result = AirQualityIndex.fromInt(3)
        assert result is AirQualityIndex.MODERATE

    def test_fromInt_with4(self):
        result = AirQualityIndex.fromInt(4)
        assert result is AirQualityIndex.POOR

    def test_fromInt_with5(self):
        result = AirQualityIndex.fromInt(5)
        assert result is AirQualityIndex.VERY_POOR

    def test_toStr_withFair(self):
        string = AirQualityIndex.FAIR.toStr()
        assert string == 'fair'

    def test_toStr_withGood(self):
        string = AirQualityIndex.GOOD.toStr()
        assert string == 'good'

    def test_toStr_withModerate(self):
        string = AirQualityIndex.MODERATE.toStr()
        assert string == 'moderate'

    def test_toStr_withPoor(self):
        string = AirQualityIndex.POOR.toStr()
        assert string == 'poor'

    def test_toStr_withVeryPoor(self):
        string = AirQualityIndex.VERY_POOR.toStr()
        assert string == 'very poor'
