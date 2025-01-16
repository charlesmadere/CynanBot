from .decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from .models.decTalkVoice import DecTalkVoice
from ..misc import utils as utils


class DecTalkVoiceMapper(DecTalkVoiceMapperInterface):

    async def fromString(self, voice: str) -> DecTalkVoice:
        if not utils.isValidStr(voice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case 'betty': return DecTalkVoice.BETTY
            case 'dennis': return DecTalkVoice.DENNIS
            case 'frank': return DecTalkVoice.FRANK
            case 'harry': return DecTalkVoice.HARRY
            case 'kit': return DecTalkVoice.KIT
            case 'paul': return DecTalkVoice.PAUL
            case 'rita': return DecTalkVoice.RITA
            case 'ursula': return DecTalkVoice.URSULA
            case 'wendy': return DecTalkVoice.WENDY
            case _: raise RuntimeError(f'voice is an unknown value: \"{voice}\"')

    async def toString(self, voice: DecTalkVoice) -> str:
        if not isinstance(voice, DecTalkVoice):
            raise TypeError(f'voice argument is malformed: \"{voice}\"')

        match voice:
            case DecTalkVoice.BETTY: return '[:nb]'
            case DecTalkVoice.DENNIS: return '[:nd]'
            case DecTalkVoice.FRANK: return '[:nf]'
            case DecTalkVoice.HARRY: return '[:nh]'
            case DecTalkVoice.KIT: return '[:nk]'
            case DecTalkVoice.PAUL: return '[:np]'
            case DecTalkVoice.RITA: return '[:nr]'
            case DecTalkVoice.URSULA: return '[:nu]'
            case DecTalkVoice.WENDY: return '[:nw]'
            case _: raise RuntimeError(f'voice is an unknown value: \"{voice}\"')
