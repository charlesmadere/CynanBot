from enum import Enum, auto


class MicrosoftTtsVoice(Enum):

    ANA = auto()
    ANDREW = auto()
    ANTOINE = auto()
    ARIA = auto()
    AVA = auto()
    BRIAN = auto()
    CHRISTOPHER = auto()
    CLARA = auto()
    DAVID = auto()
    EMMA = auto()
    ERIC = auto()
    FINN = auto()
    GUY = auto()
    HARUKA = auto()
    HORTENSE = auto()
    JEAN = auto()
    JENNY = auto()
    KEITA = auto()
    LIAM = auto()
    MICHELLE = auto()
    NANAMI = auto()
    NATASHA = auto()
    PERNILLE = auto()
    ROGER = auto()
    STEFFAN = auto()
    SYLVIE = auto()
    THIERRY = auto()
    WILLIAM = auto()
    ZIRA = auto()

    @property
    def apiValue(self) -> str:
        match self:
            case MicrosoftTtsVoice.ANA: return 'Microsoft Ana Online'
            case MicrosoftTtsVoice.ANDREW: return 'Microsoft AndrewMultilingual Online'
            case MicrosoftTtsVoice.ANTOINE: return 'Microsoft Antoine Online'
            case MicrosoftTtsVoice.ARIA: return 'Microsoft Aria Online'
            case MicrosoftTtsVoice.AVA: return 'Microsoft AvaMultilingual Online'
            case MicrosoftTtsVoice.BRIAN: return 'Microsoft BrianMultilingual Online'
            case MicrosoftTtsVoice.CHRISTOPHER: return 'Microsoft Christopher Online'
            case MicrosoftTtsVoice.CLARA: return 'Microsoft Clara Online'
            case MicrosoftTtsVoice.DAVID: return 'Microsoft David Desktop'
            case MicrosoftTtsVoice.EMMA: return 'Microsoft EmmaMultilingual Online'
            case MicrosoftTtsVoice.ERIC: return 'Microsoft Eric Online'
            case MicrosoftTtsVoice.FINN: return 'Microsoft Finn Online'
            case MicrosoftTtsVoice.GUY: return 'Microsoft Guy Online'
            case MicrosoftTtsVoice.HARUKA: return 'Microsoft Haruka Desktop'
            case MicrosoftTtsVoice.HORTENSE: return 'Microsoft Hortense Desktop'
            case MicrosoftTtsVoice.JEAN: return 'Microsoft Jean Online'
            case MicrosoftTtsVoice.JENNY: return 'Microsoft Jenny Online'
            case MicrosoftTtsVoice.KEITA: return 'Microsoft Keita Online'
            case MicrosoftTtsVoice.LIAM: return 'Microsoft Liam Online'
            case MicrosoftTtsVoice.MICHELLE: return 'Microsoft Michelle Online'
            case MicrosoftTtsVoice.NANAMI: return 'Microsoft Nanami Online'
            case MicrosoftTtsVoice.NATASHA: return 'Microsoft Natasha Online'
            case MicrosoftTtsVoice.PERNILLE: return 'Microsoft Pernille Online'
            case MicrosoftTtsVoice.ROGER: return 'Microsoft Roger Online'
            case MicrosoftTtsVoice.STEFFAN: return 'Microsoft Steffan Online'
            case MicrosoftTtsVoice.SYLVIE: return 'Microsoft Sylvie Online'
            case MicrosoftTtsVoice.THIERRY: return 'Microsoft Thierry Online'
            case MicrosoftTtsVoice.WILLIAM: return 'Microsoft William Online'
            case MicrosoftTtsVoice.ZIRA: return 'Microsoft Zira Desktop'
            case _: raise RuntimeError(f'Unknown MicrosoftTtsVoice value: \"{self}\"')

    @property
    def humanName(self) -> str:
        match self:
            case MicrosoftTtsVoice.ANA: return 'Ana'
            case MicrosoftTtsVoice.ANDREW: return 'Andrew'
            case MicrosoftTtsVoice.ANTOINE: return 'Antoine'
            case MicrosoftTtsVoice.ARIA: return 'Aria'
            case MicrosoftTtsVoice.AVA: return 'Ava'
            case MicrosoftTtsVoice.BRIAN: return 'Brian'
            case MicrosoftTtsVoice.CHRISTOPHER: return 'Christopher'
            case MicrosoftTtsVoice.CLARA: return 'Clara'
            case MicrosoftTtsVoice.DAVID: return 'David'
            case MicrosoftTtsVoice.EMMA: return 'Emma'
            case MicrosoftTtsVoice.ERIC: return 'Eric'
            case MicrosoftTtsVoice.FINN: return 'Finn'
            case MicrosoftTtsVoice.GUY: return 'Guy'
            case MicrosoftTtsVoice.HARUKA: return 'Haruka'
            case MicrosoftTtsVoice.HORTENSE: return 'Hortense'
            case MicrosoftTtsVoice.JEAN: return 'Jean'
            case MicrosoftTtsVoice.JENNY: return 'Jenny'
            case MicrosoftTtsVoice.KEITA: return 'Keita'
            case MicrosoftTtsVoice.LIAM: return 'Liam'
            case MicrosoftTtsVoice.MICHELLE: return 'Michelle'
            case MicrosoftTtsVoice.NANAMI: return 'Nanami'
            case MicrosoftTtsVoice.NATASHA: return 'Natasha'
            case MicrosoftTtsVoice.PERNILLE: return 'Pernille'
            case MicrosoftTtsVoice.ROGER: return 'Roger'
            case MicrosoftTtsVoice.STEFFAN: return 'Steffan'
            case MicrosoftTtsVoice.SYLVIE: return 'Sylvie'
            case MicrosoftTtsVoice.THIERRY: return 'Thierry'
            case MicrosoftTtsVoice.WILLIAM: return 'William'
            case MicrosoftTtsVoice.ZIRA: return 'Zira'
            case _: raise RuntimeError(f'Unknown MicrosoftTtsVoice value: \"{self}\"')
