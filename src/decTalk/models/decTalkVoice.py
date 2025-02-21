from enum import Enum, auto


class DecTalkVoice(Enum):

    BETTY = auto()
    DENNIS = auto()
    FRANK = auto()
    HARRY = auto()
    KIT = auto()
    PAUL = auto()
    RITA = auto()
    URSULA = auto()
    WENDY = auto()

    @property
    def commandString(self) -> str:
        match self:
            case DecTalkVoice.BETTY: return '[:nb]'
            case DecTalkVoice.DENNIS: return '[:nd]'
            case DecTalkVoice.FRANK: return '[:nf]'
            case DecTalkVoice.HARRY: return '[:nh]'
            case DecTalkVoice.KIT: return '[:nk]'
            case DecTalkVoice.PAUL: return '[:np]'
            case DecTalkVoice.RITA: return '[:nr]'
            case DecTalkVoice.URSULA: return '[:nu]'
            case DecTalkVoice.WENDY: return '[:nw]'
            case _: raise RuntimeError(f'Unknown DecTalkVoice value: \"{self}\"')

    @property
    def humanName(self) -> str:
        match self:
            case DecTalkVoice.BETTY: return 'Betty'
            case DecTalkVoice.DENNIS: return 'Dennis'
            case DecTalkVoice.FRANK: return 'Frank'
            case DecTalkVoice.HARRY: return 'Harry'
            case DecTalkVoice.KIT: return 'Kit'
            case DecTalkVoice.PAUL: return 'Paul'
            case DecTalkVoice.RITA: return 'Rita'
            case DecTalkVoice.URSULA: return 'Ursula'
            case DecTalkVoice.WENDY: return 'Wendy'
            case _: raise RuntimeError(f'Unknown DecTalkVoice value: \"{self}\"')
