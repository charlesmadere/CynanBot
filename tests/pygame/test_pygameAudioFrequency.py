from src.pygame.pygameAudioFrequency import PygameAudioFrequency


class TestPygameAudioFrequency:

    def test_hzValue_withAll(self):
        results: set[int] = set()

        for audioFrequency in PygameAudioFrequency:
            results.add(audioFrequency.hzValue)

        assert len(results) == len(PygameAudioFrequency)

    def test_hzValue_withFortyFourKhz(self):
        result = PygameAudioFrequency.FORTY_FOUR_KHZ.hzValue
        assert result == 44100

    def test_hzValue_withFortyEightKhz(self):
        result = PygameAudioFrequency.FORTY_EIGHT_KHZ.hzValue
        assert result == 48000
