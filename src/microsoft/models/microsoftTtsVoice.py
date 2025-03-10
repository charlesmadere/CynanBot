from enum import Enum, auto


class MicrosoftTtsVoice(Enum):

    DAVID = auto()
    HARUKA = auto()
    ZIRA = auto()

    @property
    def apiValue(self) -> str:
        match self:
            case MicrosoftTtsVoice.DAVID: return 'Microsoft David Desktop'
            case MicrosoftTtsVoice.HARUKA: return 'Microsoft Haruka Desktop'
            case MicrosoftTtsVoice.ZIRA: return 'Microsoft Zira Desktop'

    @property
    def jsonValue(self) -> str:
        match self:
            case MicrosoftTtsVoice.DAVID: return 'david'
            case MicrosoftTtsVoice.HARUKA: return 'haruka'
            case MicrosoftTtsVoice.ZIRA: return 'zira'

    @property
    def humanName(self) -> str:
        match self:
            case MicrosoftTtsVoice.DAVID: return 'David'
            case MicrosoftTtsVoice.HARUKA: return 'Haruka'
            case MicrosoftTtsVoice.ZIRA: return 'Zira'