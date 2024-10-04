from src.crowdControl.bizhawk.bizhawkKey import BizhawkKey


class TestBizhawkKey:

    def test_intValue_withKeyArrowDown(self):
        result = BizhawkKey.ARROW_DOWN.intValue
        assert result == 50

    def test_intValue_withKeyArrowLeft(self):
        result = BizhawkKey.ARROW_LEFT.intValue
        assert result == 76

    def test_intValue_withKeyArrowRight(self):
        result = BizhawkKey.ARROW_RIGHT.intValue
        assert result == 118

    def test_intValue_withKeyArrowUp(self):
        result = BizhawkKey.ARROW_UP.intValue
        assert result == 132

    def test_intValue_withKeyEnter(self):
        result = BizhawkKey.ENTER.intValue
        assert result == 117

    def test_intValue_withKeyF1(self):
        result = BizhawkKey.F1.intValue
        assert result == 54

    def test_intValue_withKeyF2(self):
        result = BizhawkKey.F2.intValue
        assert result == 55

    def test_intValue_withKeyF3(self):
        result = BizhawkKey.F3.intValue
        assert result == 56

    def test_intValue_withKeyF4(self):
        result = BizhawkKey.F4.intValue
        assert result == 57

    def test_intValue_withKeyF5(self):
        result = BizhawkKey.F5.intValue
        assert result == 58

    def test_intValue_withKeyF6(self):
        result = BizhawkKey.F6.intValue
        assert result == 59

    def test_intValue_withKeyF7(self):
        result = BizhawkKey.F7.intValue
        assert result == 60

    def test_intValue_withKeyF8(self):
        result = BizhawkKey.F8.intValue
        assert result == 61

    def test_intValue_withKeyF9(self):
        result = BizhawkKey.F9.intValue
        assert result == 62

    def test_intValue_withKeyF10(self):
        result = BizhawkKey.F10.intValue
        assert result == 63

    def test_intValue_withKeyF11(self):
        result = BizhawkKey.F11.intValue
        assert result == 64

    def test_intValue_withKeyF12(self):
        result = BizhawkKey.F12.intValue
        assert result == 65

    def test_intValue_withKeyF13(self):
        result = BizhawkKey.F13.intValue
        assert result == 66

    def test_intValue_withKeyF14(self):
        result = BizhawkKey.F14.intValue
        assert result == 67

    def test_intValue_withKeyF15(self):
        result = BizhawkKey.F15.intValue
        assert result == 68
