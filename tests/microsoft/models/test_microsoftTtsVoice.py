from src.microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice


class TestMicrosoftTtsVoice:

    def test_apiValue(self):
        results: set[str] = set()

        for voice in MicrosoftTtsVoice:
            results.add(voice.apiValue)

        assert len(results) == len(MicrosoftTtsVoice)

    def test_apiValue_withAna(self):
        result = MicrosoftTtsVoice.ANA.apiValue
        assert result == 'Microsoft Ana Online'

    def test_apiValue_withAndrew(self):
        result = MicrosoftTtsVoice.ANDREW.apiValue
        assert result == 'Microsoft AndrewMultilingual Online'

    def test_apiValue_withAntoine(self):
        result = MicrosoftTtsVoice.ANTOINE.apiValue
        assert result == 'Microsoft Antoine Online'

    def test_apiValue_withAria(self):
        result = MicrosoftTtsVoice.ARIA.apiValue
        assert result == 'Microsoft Aria Online'

    def test_apiValue_withAva(self):
        result = MicrosoftTtsVoice.AVA.apiValue
        assert result == 'Microsoft AvaMultilingual Online'

    def test_apiValue_withBrian(self):
        result = MicrosoftTtsVoice.BRIAN.apiValue
        assert result == 'Microsoft BrianMultilingual Online'

    def test_apiValue_withChristopher(self):
        result = MicrosoftTtsVoice.CHRISTOPHER.apiValue
        assert result == 'Microsoft Christopher Online'

    def test_apiValue_withClara(self):
        result = MicrosoftTtsVoice.CLARA.apiValue
        assert result == 'Microsoft Clara Online'

    def test_apiValue_withDavid(self):
        result = MicrosoftTtsVoice.DAVID.apiValue
        assert result == 'Microsoft David Desktop'

    def test_apiValue_withEmma(self):
        result = MicrosoftTtsVoice.EMMA.apiValue
        assert result == 'Microsoft EmmaMultilingual Online'

    def test_apiValue_withEric(self):
        result = MicrosoftTtsVoice.ERIC.apiValue
        assert result == 'Microsoft Eric Online'

    def test_apiValue_withFinn(self):
        result = MicrosoftTtsVoice.FINN.apiValue
        assert result == 'Microsoft Finn Online'

    def test_apiValue_withGuy(self):
        result = MicrosoftTtsVoice.GUY.apiValue
        assert result == 'Microsoft Guy Online'

    def test_apiValue_withHaruka(self):
        result = MicrosoftTtsVoice.HARUKA.apiValue
        assert result == 'Microsoft Haruka Desktop'

    def test_apiValue_withHortense(self):
        result = MicrosoftTtsVoice.HORTENSE.apiValue
        assert result == 'Microsoft Hortense Desktop'

    def test_apiValue_withJean(self):
        result = MicrosoftTtsVoice.JEAN.apiValue
        assert result == 'Microsoft Jean Online'

    def test_apiValue_withJenny(self):
        result = MicrosoftTtsVoice.JENNY.apiValue
        assert result == 'Microsoft Jenny Online'

    def test_apiValue_withKeita(self):
        result = MicrosoftTtsVoice.KEITA.apiValue
        assert result == 'Microsoft Keita Online'

    def test_apiValue_withLiam(self):
        result = MicrosoftTtsVoice.LIAM.apiValue
        assert result == 'Microsoft Liam Online'

    def test_apiValue_withMichelle(self):
        result = MicrosoftTtsVoice.MICHELLE.apiValue
        assert result == 'Microsoft Michelle Online'

    def test_apiValue_withNanami(self):
        result = MicrosoftTtsVoice.NANAMI.apiValue
        assert result == 'Microsoft Nanami Online'

    def test_apiValue_withNatasha(self):
        result = MicrosoftTtsVoice.NATASHA.apiValue
        assert result == 'Microsoft Natasha Online'

    def test_apiValue_withPernille(self):
        result = MicrosoftTtsVoice.PERNILLE.apiValue
        assert result == 'Microsoft Pernille Online'

    def test_apiValue_withRoger(self):
        result = MicrosoftTtsVoice.ROGER.apiValue
        assert result == 'Microsoft Roger Online'

    def test_apiValue_withSteffan(self):
        result = MicrosoftTtsVoice.STEFFAN.apiValue
        assert result == 'Microsoft Steffan Online'

    def test_apiValue_withSylvie(self):
        result = MicrosoftTtsVoice.SYLVIE.apiValue
        assert result == 'Microsoft Sylvie Online'

    def test_apiValue_withThierry(self):
        result = MicrosoftTtsVoice.THIERRY.apiValue
        assert result == 'Microsoft Thierry Online'

    def test_apiValue_withWilliam(self):
        result = MicrosoftTtsVoice.WILLIAM.apiValue
        assert result == 'Microsoft William Online'

    def test_apiValue_withZira(self):
        result = MicrosoftTtsVoice.ZIRA.apiValue
        assert result == 'Microsoft Zira Desktop'

    def test_humanName(self):
        results: set[str] = set()

        for voice in MicrosoftTtsVoice:
            results.add(voice.humanName)

        assert len(results) == len(MicrosoftTtsVoice)

    def test_humanName_withAna(self):
        result = MicrosoftTtsVoice.ANA.humanName
        assert result == 'Ana'

    def test_humanName_withAndrew(self):
        result = MicrosoftTtsVoice.ANDREW.humanName
        assert result == 'Andrew'

    def test_humanName_withAntoine(self):
        result = MicrosoftTtsVoice.ANTOINE.humanName
        assert result == 'Antoine'

    def test_humanName_withAria(self):
        result = MicrosoftTtsVoice.ARIA.humanName
        assert result == 'Aria'

    def test_humanName_withAva(self):
        result = MicrosoftTtsVoice.AVA.humanName
        assert result == 'Ava'

    def test_humanName_withBrian(self):
        result = MicrosoftTtsVoice.BRIAN.humanName
        assert result == 'Brian'

    def test_humanName_withChristopher(self):
        result = MicrosoftTtsVoice.CHRISTOPHER.humanName
        assert result == 'Christopher'

    def test_humanName_withClara(self):
        result = MicrosoftTtsVoice.CLARA.humanName
        assert result == 'Clara'

    def test_humanName_withDavid(self):
        result = MicrosoftTtsVoice.DAVID.humanName
        assert result == 'David'

    def test_humanName_withEmma(self):
        result = MicrosoftTtsVoice.EMMA.humanName
        assert result == 'Emma'

    def test_humanName_withEric(self):
        result = MicrosoftTtsVoice.ERIC.humanName
        assert result == 'Eric'

    def test_humanName_withFinn(self):
        result = MicrosoftTtsVoice.FINN.humanName
        assert result == 'Finn'

    def test_humanName_withGuy(self):
        result = MicrosoftTtsVoice.GUY.humanName
        assert result == 'Guy'

    def test_humanName_withHaruka(self):
        result = MicrosoftTtsVoice.HARUKA.humanName
        assert result == 'Haruka'

    def test_humanName_withHortense(self):
        result = MicrosoftTtsVoice.HORTENSE.humanName
        assert result == 'Hortense'

    def test_humanName_withJean(self):
        result = MicrosoftTtsVoice.JEAN.humanName
        assert result == 'Jean'

    def test_humanName_withJenny(self):
        result = MicrosoftTtsVoice.JENNY.humanName
        assert result == 'Jenny'

    def test_humanName_withKeita(self):
        result = MicrosoftTtsVoice.KEITA.humanName
        assert result == 'Keita'

    def test_humanName_withLiam(self):
        result = MicrosoftTtsVoice.LIAM.humanName
        assert result == 'Liam'

    def test_humanName_withMichelle(self):
        result = MicrosoftTtsVoice.MICHELLE.humanName
        assert result == 'Michelle'

    def test_humanName_withNanami(self):
        result = MicrosoftTtsVoice.NANAMI.humanName
        assert result == 'Nanami'

    def test_humanName_withNatasha(self):
        result = MicrosoftTtsVoice.NATASHA.humanName
        assert result == 'Natasha'

    def test_humanName_withPernille(self):
        result = MicrosoftTtsVoice.PERNILLE.humanName
        assert result == 'Pernille'

    def test_humanName_withRoger(self):
        result = MicrosoftTtsVoice.ROGER.humanName
        assert result == 'Roger'

    def test_humanName_withSteffan(self):
        result = MicrosoftTtsVoice.STEFFAN.humanName
        assert result == 'Steffan'

    def test_humanName_withSylvie(self):
        result = MicrosoftTtsVoice.SYLVIE.humanName
        assert result == 'Sylvie'

    def test_humanName_withThierry(self):
        result = MicrosoftTtsVoice.THIERRY.humanName
        assert result == 'Thierry'

    def test_humanName_withWilliam(self):
        result = MicrosoftTtsVoice.WILLIAM.humanName
        assert result == 'William'

    def test_humanName_withZira(self):
        result = MicrosoftTtsVoice.ZIRA.humanName
        assert result == 'Zira'
