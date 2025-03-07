from src.microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice


class TestMicrosoftSamVoice:

    def test_apiValue_withAll(self):
        apiValues: list[str] = list()

        for voice in MicrosoftSamVoice:
            apiValues.append(voice.apiValue)

        assert len(apiValues) == len(list(MicrosoftSamVoice))

    def test_apiValue_withBonziBuddy(self):
        result = MicrosoftSamVoice.BONZI_BUDDY.apiValue
        assert result == 'Adult Male #2, American English (TruVoice)'

    def test_apiValue_withSam(self):
        result = MicrosoftSamVoice.SAM.apiValue
        assert result == 'Sam'

    def test_humanName_withAll(self):
        humanNames: list[str] = list()

        for voice in MicrosoftSamVoice:
            humanNames.append(voice.humanName)

        assert len(humanNames) == len(list(MicrosoftSamVoice))

    def test_humanName_withBonziBuddy(self):
        result = MicrosoftSamVoice.BONZI_BUDDY.humanName
        assert result == 'Bonzi Buddy'

    def test_humanName_withSam(self):
        result = MicrosoftSamVoice.SAM.humanName
        assert result == 'Sam'

    def test_jsonValue_withAll(self):
        jsonValues: list[str] = list()

        for voice in MicrosoftSamVoice:
            jsonValues.append(voice.jsonValue)

        assert len(jsonValues) == len(list(MicrosoftSamVoice))

    def test_pitch_withAll(self):
        pitchValues: list[int] = list()

        for voice in MicrosoftSamVoice:
            pitchValues.append(voice.pitch)

        assert len(pitchValues) == len(list(MicrosoftSamVoice))

    def test_speed_withAll(self):
        speedValues: list[int] = list()

        for voice in MicrosoftSamVoice:
            speedValues.append(voice.speed)

        assert len(speedValues) == len(list(MicrosoftSamVoice))
