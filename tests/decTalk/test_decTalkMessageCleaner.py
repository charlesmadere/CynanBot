import pytest

from src.decTalk.decTalkMessageCleaner import DecTalkMessageCleaner
from src.decTalk.decTalkMessageCleanerInterface import DecTalkMessageCleanerInterface
from src.emojiHelper.emojiHelper import EmojiHelper
from src.emojiHelper.emojiHelperInterface import EmojiHelperInterface
from src.emojiHelper.emojiRepository import EmojiRepository
from src.emojiHelper.emojiRepositoryInterface import EmojiRepositoryInterface
from src.google.googleJsonMapper import GoogleJsonMapper
from src.google.googleJsonMapperInterface import GoogleJsonMapperInterface
from src.location.timeZoneRepository import TimeZoneRepository
from src.location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from src.storage.jsonStaticReader import JsonStaticReader
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.tts.ttsSettingsRepository import TtsSettingsRepository
from src.tts.ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface


class TestDecTalkMessageCleaner:

    timber: TimberInterface = TimberStub()

    timeZoneRepository: TimeZoneRepositoryInterface = TimeZoneRepository()

    emojiRepository: EmojiRepositoryInterface = EmojiRepository(
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

    emojiHelper: EmojiHelperInterface = EmojiHelper(
        emojiRepository = emojiRepository
    )

    googleJsonMapper: GoogleJsonMapperInterface = GoogleJsonMapper(
        timber = timber,
        timeZoneRepository = timeZoneRepository
    )

    ttsSettingsRepository: TtsSettingsRepositoryInterface = TtsSettingsRepository(
        googleJsonMapper = googleJsonMapper,
        settingsJsonReader = JsonStaticReader(dict())
    )

    cleaner: DecTalkMessageCleanerInterface = DecTalkMessageCleaner(
        emojiHelper = emojiHelper,
        timber = timber,
        ttsSettingsRepository = ttsSettingsRepository
    )

    @pytest.mark.asyncio
    async def test_clean_withEmptyString(self):
        result = await self.cleaner.clean('')
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withNone(self):
        result = await self.cleaner.clean(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_clean_withEmojiString(self):
        result = await self.cleaner.clean('shark 🦈 shark 😀 🤔')
        assert result == 'shark shark shark grinning face'

    @pytest.mark.asyncio
    async def test_clean_withOverlyLongMessage(self):
        result = await self.cleaner.clean('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac velit neque. Suspendisse sed scelerisque metus, eget ultrices mi. Quisque accumsan laoreet sapien, eget euismod ex hendrerit a. Ut mattis ipsum enim, eget ultrices nisl pulvinar at. Sed eu ornare neque. Quisque nec commodo enim. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas efficitur odio arcu, vel vestibulum metus porttitor ac. Mauris sollicitudin, velit in malesuada scelerisque, magna nisi posuere nisi, ac sodales dolor massa vitae ex. Sed fermentum purus vel purus efficitur varius id ut lacus. Duis eu neque dapibus, ornare mauris porta, placerat enim. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut et nisi mi. Donec efficitur sapien a bibendum tincidunt.')
        assert result == 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ac velit neque. Suspendisse sed scelerisque metus, eget ultrices mi. Quisque accumsan laoreet sapien, eget euismod ex hendrerit a. Ut mattis ipsum enim, eget ultrices nisl pulvinar at. Se'
        assert len(result) == await self.ttsSettingsRepository.getMaximumMessageSize()

    @pytest.mark.asyncio
    async def test_clean_withWhitespaceString(self):
        result = await self.cleaner.clean(' ')
        assert result is None
