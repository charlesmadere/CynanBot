from src.decTalk.models.decTalkVoice import DecTalkVoice


class TestDecTalkVoice:

    def test_all_commandString(self):
        commandStrings: set[str] = set()

        for voice in DecTalkVoice:
            commandStrings.add(voice.commandString)

        assert len(commandStrings) == len(DecTalkVoice)

    def test_all_humanName(self):
        humanNames: set[str] = set()

        for voice in DecTalkVoice:
            humanNames.add(voice.humanName)

        assert len(humanNames) == len(DecTalkVoice)

    def test_betty_commandString(self):
        result = DecTalkVoice.BETTY.commandString
        assert result == '[:nb]'

    def test_betty_humanName(self):
        result = DecTalkVoice.BETTY.humanName
        assert result == 'Betty'

    def test_dennis_commandString(self):
        result = DecTalkVoice.DENNIS.commandString
        assert result == '[:nd]'

    def test_dennis_humanName(self):
        result = DecTalkVoice.DENNIS.humanName
        assert result == 'Dennis'

    def test_frank_commandString(self):
        result = DecTalkVoice.FRANK.commandString
        assert result == '[:nf]'

    def test_frank_humanName(self):
        result = DecTalkVoice.FRANK.humanName
        assert result == 'Frank'

    def test_kit_commandString(self):
        result = DecTalkVoice.KIT.commandString
        assert result == '[:nk]'

    def test_kit_humanName(self):
        result = DecTalkVoice.KIT.humanName
        assert result == 'Kit'

    def test_harry_commandString(self):
        result = DecTalkVoice.HARRY.commandString
        assert result == '[:nh]'

    def test_harry_humanName(self):
        result = DecTalkVoice.HARRY.humanName
        assert result == 'Harry'

    def test_paul_commandString(self):
        result = DecTalkVoice.PAUL.commandString
        assert result == '[:np]'

    def test_paul_humanName(self):
        result = DecTalkVoice.PAUL.humanName
        assert result == 'Paul'

    def test_rita_commandString(self):
        result = DecTalkVoice.RITA.commandString
        assert result == '[:nr]'

    def test_rita_humanName(self):
        result = DecTalkVoice.RITA.humanName
        assert result == 'Rita'

    def test_ursula_commandString(self):
        result = DecTalkVoice.URSULA.commandString
        assert result == '[:nu]'

    def test_ursula_humanName(self):
        result = DecTalkVoice.URSULA.humanName
        assert result == 'Ursula'

    def test_wendy_commandString(self):
        result = DecTalkVoice.WENDY.commandString
        assert result == '[:nw]'

    def test_wendy_humanName(self):
        result = DecTalkVoice.WENDY.humanName
        assert result == 'Wendy'
