import random

from frozendict import frozendict

from .googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface
from ..models.googleVoiceSelectionParams import GoogleVoiceSelectionParams


class GoogleTtsVoiceChooser(GoogleTtsVoiceChooserInterface):

    def __init__(
        self,
        languageCodeToNames: frozendict[str, frozenset[str]] = frozendict({
            'en-AU': frozenset({ 'en-AU-Chirp-HD-D', 'en-AU-Chirp-HD-F', 'en-AU-Chirp-HD-O' }),
            'en-GB': frozenset({ 'en-GB-Chirp-HD-D', 'en-GB-Chirp-HD-F', 'en-GB-Chirp-HD-O' })
        })
    ):
        if not isinstance(languageCodeToNames, frozendict):
            raise TypeError(f'languageCodeToVoiceNames argument is malformed: \"{languageCodeToNames}\"')
        elif len(languageCodeToNames) == 0:
            raise ValueError(f'languageCodeToNames argument is empty: \"{languageCodeToNames}\"')

        self.__languageCodeToNames: frozendict[str, frozenset[str]] = languageCodeToNames

    async def choose(self) -> GoogleVoiceSelectionParams:
        languageCodes = self.__languageCodeToNames.keys()
        languageCode = random.choice(list(languageCodes))

        names = self.__languageCodeToNames[languageCode]
        name = random.choice(list(names))

        return GoogleVoiceSelectionParams(
            gender = None,
            languageCode = languageCode,
            name = name
        )
