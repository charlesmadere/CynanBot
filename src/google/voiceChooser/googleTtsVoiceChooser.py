import random

from .googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface
from ..models.googleVoicePreset import GoogleVoicePreset
from ..models.googleVoiceSelectionParams import GoogleVoiceSelectionParams


class GoogleTtsVoiceChooser(GoogleTtsVoiceChooserInterface):

    def __init__(
        self,
        voicePresets: frozenset[GoogleVoicePreset] = frozenset({
            GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_D,
            GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_F,
            GoogleVoicePreset.ENGLISH_AUSTRALIAN_CHIRP_O,
            GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_D,
            GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_F,
            GoogleVoicePreset.ENGLISH_GREAT_BRITAIN_CHIRP_O
        })
    ):
        if not isinstance(voicePresets, frozenset):
            raise TypeError(f'voicePresets argument is malformed: \"{voicePresets}\"')
        elif len(voicePresets) == 0:
            raise ValueError(f'voicePresets argument is empty: \"{voicePresets}\"')

        self.__voicePresets: frozenset[GoogleVoicePreset] = voicePresets

    async def choose(self) -> GoogleVoiceSelectionParams:
        voicePreset = random.choice(list(self.__voicePresets))

        return GoogleVoiceSelectionParams(
            gender = None,
            languageCode = voicePreset.languageCode,
            name = voicePreset.fullName
        )
