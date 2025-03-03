import pytest

from src.decTalk.decTalkVoiceChooser import DecTalkVoiceChooser
from src.decTalk.decTalkVoiceChooserInterface import DecTalkVoiceChooserInterface
from src.decTalk.models.decTalkVoice import DecTalkVoice


class TestDecTalkVoiceChooser:

    chooser: DecTalkVoiceChooserInterface = DecTalkVoiceChooser()

    @pytest.mark.asyncio
    async def test_choose_withEmptyString(self):
        result = await self.chooser.choose('')
        assert result is None

    @pytest.mark.asyncio
    async def test_choose_withNone(self):
        result = await self.chooser.choose(None)
        assert result is None

    @pytest.mark.asyncio
    async def test_choose_withWhitespace(self):
        result = await self.chooser.choose(' ')
        assert result is None

    @pytest.mark.asyncio
    async def test_choose_withVoiceBetty(self):
        await self.__assertChooseWithVoice(DecTalkVoice.BETTY)

    @pytest.mark.asyncio
    async def test_choose_withVoiceDennis(self):
        await self.__assertChooseWithVoice(DecTalkVoice.DENNIS)

    @pytest.mark.asyncio
    async def test_choose_withVoiceFrank(self):
        await self.__assertChooseWithVoice(DecTalkVoice.FRANK)

    @pytest.mark.asyncio
    async def test_choose_withVoiceHarry(self):
        await self.__assertChooseWithVoice(DecTalkVoice.HARRY)

    @pytest.mark.asyncio
    async def test_choose_withVoiceKit(self):
        await self.__assertChooseWithVoice(DecTalkVoice.KIT)

    @pytest.mark.asyncio
    async def test_choose_withVoicePaul(self):
        await self.__assertChooseWithVoice(DecTalkVoice.PAUL)

    @pytest.mark.asyncio
    async def test_choose_withVoiceRita(self):
        await self.__assertChooseWithVoice(DecTalkVoice.RITA)

    @pytest.mark.asyncio
    async def test_choose_withVoiceWendy(self):
        await self.__assertChooseWithVoice(DecTalkVoice.WENDY)

    @pytest.mark.asyncio
    async def test_choose_withVoiceUrsula(self):
        await self.__assertChooseWithVoice(DecTalkVoice.URSULA)

    @pytest.mark.asyncio
    async def __assertChooseWithVoice(self, voice: DecTalkVoice):
        for _ in range(100):
            voiceString = voice.commandString

            message = f'{voiceString} Hello, World!'
            updatedMessage = await self.chooser.choose(message)
            assert updatedMessage is None

            message = f'Hello,{voiceString}World!'
            updatedMessage = await self.chooser.choose(message)
            assert updatedMessage is None

            message = f'Hello, World!{voiceString}'
            updatedMessage = await self.chooser.choose(message)
            assert updatedMessage is None

    def test_sanity(self):
        assert self.chooser is not None
        assert isinstance(self.chooser, DecTalkVoiceChooser)
        assert isinstance(self.chooser, DecTalkVoiceChooserInterface)
