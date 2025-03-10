from enum import Enum, auto


class MicrosoftTtsVoice(Enum):

    DAVID = auto()
    HARUKA = auto()
    HORTENSE = auto()
    ZIRA = auto()

    @property
    def apiValue(self) -> str:
        match self:
            case MicrosoftTtsVoice.DAVID: return 'Microsoft David Desktop'
            case MicrosoftTtsVoice.HARUKA: return 'Microsoft Haruka Desktop'
            case MicrosoftTtsVoice.HORTENSE: return 'Microsoft Hortense Desktop'
            case MicrosoftTtsVoice.ZIRA: return 'Microsoft Zira Desktop'

    @property
    def jsonValue(self) -> str:
        match self:
            case MicrosoftTtsVoice.DAVID: return 'david'
            case MicrosoftTtsVoice.HARUKA: return 'haruka'
            case MicrosoftTtsVoice.HORTENSE: return 'hortense'
            case MicrosoftTtsVoice.ZIRA: return 'zira'

    @property
    def humanName(self) -> str:
        match self:
            case MicrosoftTtsVoice.DAVID: return 'David'
            case MicrosoftTtsVoice.HARUKA: return 'Haruka'
            case MicrosoftTtsVoice.HORTENSE: return 'Hortense'
            case MicrosoftTtsVoice.ZIRA: return 'Zira'