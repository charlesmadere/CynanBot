from src.emojiHelper.emojiRepository import EmojiRepository
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface


class FakeEmojiRepository(EmojiRepository):

    def __init__(
        self,
        timber: TimberInterface
    ):
        super().__init__(
            emojiJsonReader = JsonStaticReader(
                jsonContents = {
                    'emojis': [
                        {
                            'code': [
                                "1F600"
                            ],
                            'emoji': '😀',
                            'name': 'grinning face',
                            'category': 'Smileys & Emotion',
                            'subcategory': 'face-smiling',
                            'support': {
                                'apple': True,
                                'google': True,
                                'windows': True
                            }
                        },
                        {
                            'code': [
                                "1F988"
                            ],
                            'emoji': '🦈',
                            'name': 'shark',
                            'category': 'Animals & Nature',
                            'subcategory': 'animal-marine',
                            'support': {
                                'apple': True,
                                'google': True,
                                'windows': True
                            }
                        }
                    ]
                }
            ),
            timber = timber
        )
