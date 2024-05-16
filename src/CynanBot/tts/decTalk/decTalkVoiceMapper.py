from CynanBot.tts.decTalk.decTalkVoice import DecTalkVoice
from CynanBot.tts.decTalk.decTalkVoiceMapperInterface import \
    DecTalkVoiceMapperInterface


class DecTalkVoiceMapper(DecTalkVoiceMapperInterface):

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

        raise RuntimeError(f'voice is an unknown value: \"{voice}\"')
