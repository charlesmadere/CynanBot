import pytest

from src.chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelper import ChatterPreferredTtsUserMessageHelper
from src.chatterPreferredTts.helper.chatterPreferredTtsUserMessageHelperInterface import \
    ChatterPreferredTtsUserMessageHelperInterface
from src.chatterPreferredTts.models.commodoreSam.commodoreSamTtsProperties import CommodoreSamTtsProperties
from src.chatterPreferredTts.models.decTalk.decTalkTtsProperties import DecTalkTtsProperties
from src.chatterPreferredTts.models.google.googleTtsProperties import GoogleTtsProperties
from src.chatterPreferredTts.models.halfLife.halfLifeTtsProperties import HalfLifeTtsProperties
from src.chatterPreferredTts.models.microsoft.microsoftTtsTtsProperties import MicrosoftTtsTtsProperties
from src.chatterPreferredTts.models.microsoftSam.microsoftSamTtsProperties import MicrosoftSamTtsProperties
from src.chatterPreferredTts.models.randoTts.randoTtsTtsProperties import RandoTtsTtsProperties
from src.chatterPreferredTts.models.streamElements.streamElementsTtsProperties import StreamElementsTtsProperties
from src.chatterPreferredTts.models.ttsMonster.ttsMonsterTtsProperties import TtsMonsterTtsProperties
from src.decTalk.mapper.decTalkVoiceMapper import DecTalkVoiceMapper
from src.decTalk.mapper.decTalkVoiceMapperInterface import DecTalkVoiceMapperInterface
from src.decTalk.models.decTalkVoice import DecTalkVoice
from src.halfLife.models.halfLifeVoice import HalfLifeVoice
from src.halfLife.parser.halfLifeVoiceParser import HalfLifeVoiceParser
from src.halfLife.parser.halfLifeVoiceParserInterface import HalfLifeVoiceParserInterface
from src.language.languageEntry import LanguageEntry
from src.language.languagesRepository import LanguagesRepository
from src.language.languagesRepositoryInterface import LanguagesRepositoryInterface
from src.microsoft.models.microsoftTtsVoice import MicrosoftTtsVoice
from src.microsoft.parser.microsoftTtsJsonParser import MicrosoftTtsJsonParser
from src.microsoft.parser.microsoftTtsJsonParserInterface import MicrosoftTtsJsonParserInterface
from src.microsoftSam.models.microsoftSamVoice import MicrosoftSamVoice
from src.microsoftSam.parser.microsoftSamJsonParser import MicrosoftSamJsonParser
from src.microsoftSam.parser.microsoftSamJsonParserInterface import MicrosoftSamJsonParserInterface
from src.streamElements.models.streamElementsVoice import StreamElementsVoice
from src.streamElements.parser.streamElementsJsonParser import StreamElementsJsonParser
from src.streamElements.parser.streamElementsJsonParserInterface import StreamElementsJsonParserInterface
from src.timber.timberInterface import TimberInterface
from src.timber.timberStub import TimberStub
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapper import TtsMonsterPrivateApiJsonMapper
from src.ttsMonster.mapper.ttsMonsterPrivateApiJsonMapperInterface import TtsMonsterPrivateApiJsonMapperInterface
from src.ttsMonster.models.ttsMonsterVoice import TtsMonsterVoice


class TestChatterPreferredTtsUserMessageHelper:

    decTalkVoiceMapper: DecTalkVoiceMapperInterface = DecTalkVoiceMapper()

    languagesRepository: LanguagesRepositoryInterface = LanguagesRepository()

    halfLifeVoiceParser: HalfLifeVoiceParserInterface = HalfLifeVoiceParser()

    microsoftSamJsonParser: MicrosoftSamJsonParserInterface = MicrosoftSamJsonParser()

    microsoftTtsJsonParser: MicrosoftTtsJsonParserInterface = MicrosoftTtsJsonParser()

    streamElementsJsonParser: StreamElementsJsonParserInterface = StreamElementsJsonParser()

    timber: TimberInterface = TimberStub()

    ttsMonsterPrivateApiJsonMapper: TtsMonsterPrivateApiJsonMapperInterface = TtsMonsterPrivateApiJsonMapper(
        timber = timber
    )

    helper: ChatterPreferredTtsUserMessageHelperInterface = ChatterPreferredTtsUserMessageHelper(
        decTalkVoiceMapper = decTalkVoiceMapper,
        halfLifeVoiceParser = halfLifeVoiceParser,
        languagesRepository = languagesRepository,
        microsoftSamJsonParser = microsoftSamJsonParser,
        microsoftTtsJsonParser = microsoftTtsJsonParser,
        streamElementsJsonParser = streamElementsJsonParser,
        timber = timber,
        ttsMonsterPrivateApiJsonMapper = ttsMonsterPrivateApiJsonMapper
    )

    @pytest.mark.asyncio
    async def test_parseUserMessage_withCommodoreSamStrings(self):
        result = await self.helper.parseUserMessage('commodoresam')
        assert isinstance(result, CommodoreSamTtsProperties)

        result = await self.helper.parseUserMessage('commodore sam')
        assert isinstance(result, CommodoreSamTtsProperties)

        result = await self.helper.parseUserMessage('commodore_sam')
        assert isinstance(result, CommodoreSamTtsProperties)

        result = await self.helper.parseUserMessage('commodore-sam')
        assert isinstance(result, CommodoreSamTtsProperties)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDecTalkStrings(self):
        result = await self.helper.parseUserMessage('dectalk')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('dec talk')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('dec_talk')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('dec-talk')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDecTalkAndHarry(self):
        result = await self.helper.parseUserMessage('dectalk harry')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.HARRY

        result = await self.helper.parseUserMessage('dec talk harry')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.HARRY

        result = await self.helper.parseUserMessage('dec_talk harry')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.HARRY

        result = await self.helper.parseUserMessage('dec-talk harry')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.HARRY

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDecTalkAndPaul(self):
        result = await self.helper.parseUserMessage('dectalk paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dectalk: paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec talk paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec talk: paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec_talk paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec_talk perfect paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec_talk: paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec_talk: perfect paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec-talk paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

        result = await self.helper.parseUserMessage('dec-talk: paul')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.PAUL

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDecTalkAndWendy(self):
        result = await self.helper.parseUserMessage('dectalk wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

        result = await self.helper.parseUserMessage('dectalk: wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

        result = await self.helper.parseUserMessage('dec talk wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

        result = await self.helper.parseUserMessage('dec talk: wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

        result = await self.helper.parseUserMessage('dec_talk wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

        result = await self.helper.parseUserMessage('dec_talk: wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

        result = await self.helper.parseUserMessage('dec_talk whispering wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

        result = await self.helper.parseUserMessage('dec_talk: whispering wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

        result = await self.helper.parseUserMessage('dec-talk wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

        result = await self.helper.parseUserMessage('dec-talk: wendy')
        assert isinstance(result, DecTalkTtsProperties)
        assert result.voice is DecTalkVoice.WENDY

    @pytest.mark.asyncio
    async def test_parseUserMessage_withDutch(self):
        result = await self.helper.parseUserMessage('dutch')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.DUTCH

    @pytest.mark.asyncio
    async def test_parseUserMessage_withEmptyString(self):
        result = await self.helper.parseUserMessage('')
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGerman(self):
        result = await self.helper.parseUserMessage('german')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.GERMAN

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleStrings(self):
        result = await self.helper.parseUserMessage('goog')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is None

        result = await self.helper.parseUserMessage('googl')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is None

        result = await self.helper.parseUserMessage('google')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndEnglish(self):
        result = await self.helper.parseUserMessage('goog english')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.ENGLISH

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndGarbledText(self):
        result = await self.helper.parseUserMessage('google fdsiklahfkldsajlfdklsflad')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndJapanese(self):
        result = await self.helper.parseUserMessage('googl ja')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.JAPANESE

        result = await self.helper.parseUserMessage('googl: japan')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.JAPANESE

        result = await self.helper.parseUserMessage('googl japanese')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.JAPANESE

        result = await self.helper.parseUserMessage('google jp')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.JAPANESE

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndKorea(self):
        result = await self.helper.parseUserMessage('goog korea')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.KOREAN

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndSpanish(self):
        result = await self.helper.parseUserMessage('google: spanish')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.SPANISH

    @pytest.mark.asyncio
    async def test_parseUserMessage_withGoogleAndSwedish(self):
        result = await self.helper.parseUserMessage('google sweden')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.SWEDISH

        result = await self.helper.parseUserMessage('google swedish')
        assert isinstance(result, GoogleTtsProperties)
        assert result.languageEntry is LanguageEntry.SWEDISH

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeStrings(self):
        result = await self.helper.parseUserMessage('halflife')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('halflife:')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('half life')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('half life:')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('half_life')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('half_life:')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('half-life')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('half-life:')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeAndGarbledText(self):
        result = await self.helper.parseUserMessage('half life fdsiklahfkldsajlfdklsflad')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeAndBarney(self):
        result = await self.helper.parseUserMessage('half life barney')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is HalfLifeVoice.BARNEY

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeAndPolice(self):
        result = await self.helper.parseUserMessage('half life police')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is HalfLifeVoice.POLICE

        result = await self.helper.parseUserMessage('half life: police')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is HalfLifeVoice.POLICE

    @pytest.mark.asyncio
    async def test_parseUserMessage_withHalfLifeAndScientist(self):
        result = await self.helper.parseUserMessage('half life scientist')
        assert isinstance(result, HalfLifeTtsProperties)
        assert result.voice is HalfLifeVoice.SCIENTIST

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftStrings(self):
        result = await self.helper.parseUserMessage('microsoft')
        assert isinstance(result, MicrosoftTtsTtsProperties)

        result = await self.helper.parseUserMessage('ms')
        assert isinstance(result, MicrosoftTtsTtsProperties)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftAndDavid(self):
        result = await self.helper.parseUserMessage('microsoft david')
        assert isinstance(result, MicrosoftTtsTtsProperties)
        assert result.voice is MicrosoftTtsVoice.DAVID

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftAndHaruka(self):
        result = await self.helper.parseUserMessage('microsoft haruka')
        assert isinstance(result, MicrosoftTtsTtsProperties)
        assert result.voice is MicrosoftTtsVoice.HARUKA

        result = await self.helper.parseUserMessage('ms haruka')
        assert isinstance(result, MicrosoftTtsTtsProperties)
        assert result.voice is MicrosoftTtsVoice.HARUKA

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftAndZira(self):
        result = await self.helper.parseUserMessage('microsoft zira')
        assert isinstance(result, MicrosoftTtsTtsProperties)
        assert result.voice is MicrosoftTtsVoice.ZIRA

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftSamStrings(self):
        result = await self.helper.parseUserMessage('microsoftsam')
        assert isinstance(result, MicrosoftSamTtsProperties)

        result = await self.helper.parseUserMessage('microsoft sam')
        assert isinstance(result, MicrosoftSamTtsProperties)

        result = await self.helper.parseUserMessage('microsoft_sam')
        assert isinstance(result, MicrosoftSamTtsProperties)

        result = await self.helper.parseUserMessage('microsoft-sam')
        assert isinstance(result, MicrosoftSamTtsProperties)

        result = await self.helper.parseUserMessage('ms sam')
        assert isinstance(result, MicrosoftSamTtsProperties)

        result = await self.helper.parseUserMessage('ms_sam')
        assert isinstance(result, MicrosoftSamTtsProperties)

        result = await self.helper.parseUserMessage('ms-sam')
        assert isinstance(result, MicrosoftSamTtsProperties)

        result = await self.helper.parseUserMessage('mssam')
        assert isinstance(result, MicrosoftSamTtsProperties)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftSamAndBonziBuddy(self):
        result = await self.helper.parseUserMessage('microsoft sam bonzi_buddy')
        assert isinstance(result, MicrosoftSamTtsProperties)
        assert result.voice is MicrosoftSamVoice.BONZI_BUDDY

        result = await self.helper.parseUserMessage('microsoft sam bonzi buddy')
        assert isinstance(result, MicrosoftSamTtsProperties)
        assert result.voice is MicrosoftSamVoice.BONZI_BUDDY

    @pytest.mark.asyncio
    async def test_parseUserMessage_withMicrosoftSamAndMaryInSpace(self):
        result = await self.helper.parseUserMessage('microsoft sam mary_in_space')
        assert isinstance(result, MicrosoftSamTtsProperties)
        assert result.voice is MicrosoftSamVoice.MARY_SPACE

        result = await self.helper.parseUserMessage('microsoft sam mary-in-space')
        assert isinstance(result, MicrosoftSamTtsProperties)
        assert result.voice is MicrosoftSamVoice.MARY_SPACE

        result = await self.helper.parseUserMessage('microsoft sam mary in space')
        assert isinstance(result, MicrosoftSamTtsProperties)
        assert result.voice is MicrosoftSamVoice.MARY_SPACE

        result = await self.helper.parseUserMessage('microsoft sam mary_space')
        assert isinstance(result, MicrosoftSamTtsProperties)
        assert result.voice is MicrosoftSamVoice.MARY_SPACE

        result = await self.helper.parseUserMessage('microsoft sam mary-space')
        assert isinstance(result, MicrosoftSamTtsProperties)
        assert result.voice is MicrosoftSamVoice.MARY_SPACE

        result = await self.helper.parseUserMessage('microsoft sam mary space')
        assert isinstance(result, MicrosoftSamTtsProperties)
        assert result.voice is MicrosoftSamVoice.MARY_SPACE

    @pytest.mark.asyncio
    async def test_parseUserMessage_withRandoTtsStrings(self):
        result = await self.helper.parseUserMessage('rando')
        assert isinstance(result, RandoTtsTtsProperties)

        result = await self.helper.parseUserMessage('random')
        assert isinstance(result, RandoTtsTtsProperties)

        result = await self.helper.parseUserMessage('rando_tts')
        assert isinstance(result, RandoTtsTtsProperties)

        result = await self.helper.parseUserMessage('random_tts')
        assert isinstance(result, RandoTtsTtsProperties)

        result = await self.helper.parseUserMessage('rando-tts')
        assert isinstance(result, RandoTtsTtsProperties)

        result = await self.helper.parseUserMessage('random-tts')
        assert isinstance(result, RandoTtsTtsProperties)

        result = await self.helper.parseUserMessage('rando tts')
        assert isinstance(result, RandoTtsTtsProperties)

        result = await self.helper.parseUserMessage('random tts')
        assert isinstance(result, RandoTtsTtsProperties)

        result = await self.helper.parseUserMessage('randotts')
        assert isinstance(result, RandoTtsTtsProperties)

        result = await self.helper.parseUserMessage('randomtts')
        assert isinstance(result, RandoTtsTtsProperties)

    @pytest.mark.asyncio
    async def test_parseUserMessage_withStreamElementsStrings(self):
        result = await self.helper.parseUserMessage('streamelements')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('streamElements')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('stream elements')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('stream-elements')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('stream_elements')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withStreamElementsAndJoey(self):
        result = await self.helper.parseUserMessage('streamelements: joey')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is StreamElementsVoice.JOEY

        result = await self.helper.parseUserMessage('streamElements: joey')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is StreamElementsVoice.JOEY

        result = await self.helper.parseUserMessage('stream elements joey')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is StreamElementsVoice.JOEY

        result = await self.helper.parseUserMessage('stream-elements joe')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is StreamElementsVoice.JOEY

        result = await self.helper.parseUserMessage('stream_elements joey')
        assert isinstance(result, StreamElementsTtsProperties)
        assert result.voice is StreamElementsVoice.JOEY

    @pytest.mark.asyncio
    async def test_parseUserMessage_withTtsMonsterStrings(self):
        result = await self.helper.parseUserMessage('ttsmonster')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('ttsmonster:')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('ttsMonster')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('ttsMonster:')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('tts_monster')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('tts_monster:')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('tts-monster')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('tts-monster:')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('tts monster')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

        result = await self.helper.parseUserMessage('tts monster:')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withTtsMonsterAndShadow(self):
        result = await self.helper.parseUserMessage('tts monster shadow')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is TtsMonsterVoice.SHADOW

        result = await self.helper.parseUserMessage('tts monster: shadow')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is TtsMonsterVoice.SHADOW

        result = await self.helper.parseUserMessage('tts_monster shadow')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is TtsMonsterVoice.SHADOW

        result = await self.helper.parseUserMessage('tts_monster: shadow')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is TtsMonsterVoice.SHADOW

        result = await self.helper.parseUserMessage('tts-monster shadow')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is TtsMonsterVoice.SHADOW

        result = await self.helper.parseUserMessage('tts-monster: shadow')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is TtsMonsterVoice.SHADOW

    @pytest.mark.asyncio
    async def test_parseUserMessage_withTtsMonsterAndZeroTwo(self):
        result = await self.helper.parseUserMessage('tts monster zerotwo')
        assert isinstance(result, TtsMonsterTtsProperties)
        assert result.voice is TtsMonsterVoice.ZERO_TWO

    @pytest.mark.asyncio
    async def test_parseUserMessage_withNone(self):
        result = await self.helper.parseUserMessage(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_parseUserMessage_withWhitespaceString(self):
        result = await self.helper.parseUserMessage(' ')
        assert result is None

    def test_sanity(self):
        assert self.helper is not None
        assert isinstance(self.helper, ChatterPreferredTtsUserMessageHelper)
        assert isinstance(self.helper, ChatterPreferredTtsUserMessageHelperInterface)
