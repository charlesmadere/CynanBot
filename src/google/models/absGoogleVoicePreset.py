class AbsGoogleVoicePreset:

    @property
    def fullName(self) -> str:
        # child classes must implement this method
        raise NotImplementedError()

    @property
    def languageCode(self) -> str:
        return '-'.join(self.fullName.split('-')[:2])
