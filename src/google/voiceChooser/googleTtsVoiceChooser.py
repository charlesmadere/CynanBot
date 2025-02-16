import random

from frozendict import frozendict

from .googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface
from ..models.googleVoiceSelectionParams import GoogleVoiceSelectionParams


class GoogleTtsVoiceChooser(GoogleTtsVoiceChooserInterface):

    def __init__(
        self,
        languageCodeToNames: frozendict[str, frozenset[str]] = frozendict({
            'en-AU': frozenset({ 'en-AU-Neural2-A', 'en-AU-Neural2-B', 'en-AU-Neural2-C', 'en-AU-Neural2-D' }),
            'en-GB': frozenset({ 'en-GB-Neural2-A', 'en-GB-Neural2-B', 'en-GB-Neural2-C', 'en-GB-Neural2-D', 'en-GB-Neural2-F' }),
            'en-US': frozenset({ 'en-US-Casual-K', 'en-US-Journey-F', 'en-US-Studio-O', 'en-US-Studio-Q' }),
            'fr-CA': frozenset({ 'fr-CA-Neural2-A', 'fr-CA-Neural2-B', 'fr-CA-Neural2-C', 'fr-CA-Neural2-D' })
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
