from src.microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice


class TestMicrosoftTtsVoice:

    def test_apiValue(self):
        results: set[str] = set()

        for voice in MicrosoftTtsVoice:
            results.add(voice.apiValue)

        assert len(results) == len(MicrosoftTtsVoice)

    def test_apiValue_withCatherine(self):
        result = MicrosoftTtsVoice.CATHERINE.apiValue
        assert result == 'Microsoft Catherine Desktop'

    def test_apiValue_withDavid(self):
        result = MicrosoftTtsVoice.DAVID.apiValue
        assert result == 'Microsoft David Desktop'

    def test_apiValue_withHaruka(self):
        result = MicrosoftTtsVoice.HARUKA.apiValue
        assert result == 'Microsoft Haruka Desktop'

    def test_apiValue_withHortense(self):
        result = MicrosoftTtsVoice.HORTENSE.apiValue
        assert result == 'Microsoft Hortense Desktop'

    def test_apiValue_withZira(self):
        result = MicrosoftTtsVoice.ZIRA.apiValue
        assert result == 'Microsoft Zira Desktop'

    def test_humanName(self):
        results: set[str] = set()

        for voice in MicrosoftTtsVoice:
            results.add(voice.humanName)

        assert len(results) == len(MicrosoftTtsVoice)

    def test_humanName_withCatherine(self):
        result = MicrosoftTtsVoice.CATHERINE.humanName
        assert result == 'Catherine'

    def test_humanName_withDavid(self):
        result = MicrosoftTtsVoice.DAVID.humanName
        assert result == 'David'

    def test_humanName_withHaruka(self):
        result = MicrosoftTtsVoice.HARUKA.humanName
        assert result == 'Haruka'

    def test_humanName_withHortense(self):
        result = MicrosoftTtsVoice.HORTENSE.humanName
        assert result == 'Hortense'

    def test_humanName_withZira(self):
        result = MicrosoftTtsVoice.ZIRA.humanName
        assert result == 'Zira'
