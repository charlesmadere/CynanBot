from src.cheerActions.wizards.stepResult import StepResult
from src.cheerActions.wizards.voicemail.voicemailStep import VoicemailStep
from src.cheerActions.wizards.voicemail.voicemailSteps import VoicemailSteps


class TestVoicemailSteps:

    def test_allSteps(self):
        steps = VoicemailSteps()
        assert steps.currentStep is VoicemailStep.BITS
        assert steps.stepForward() is StepResult.DONE
