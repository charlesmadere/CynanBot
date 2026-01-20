from dataclasses import dataclass


# This data is intended to correspond to the key and userId values that are sent via an HTTP Post
# request to the following URL: https://us-central1-tts-monster.cloudfunctions.net/generateTTS

@dataclass(frozen = True, slots = True)
class TtsMonsterTokens:
    key: str
    twitchChannelId: str
    userId: str
