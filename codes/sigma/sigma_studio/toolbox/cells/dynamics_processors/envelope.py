try:
    from .dynamics_processors import DynamicsProcessor, RMS

except:
    from dynamics_processors import DynamicsProcessor, RMS



class Envelope(DynamicsProcessor):
    HOLD_PARAM = None
    DECAY_PARAM = None



class MonoEnvelopePeakExtDecayAlg(Envelope):
    HOLD_PARAM = 'hold'


    def set_decay(self, dB_s, **kwargs):
        raise NotImplementedError('Decay is externally controlled.')



class MonoEnvelopePeakAlg(Envelope):
    pass



class MonoEnvelopeAccuratePeakAlg(Envelope):
    pass



class MonoRunAvgDetectAlg(Envelope, RMS):
    # https://wiki.analog.com/resources/tools-software/sigmastudio/toolbox/dynamicsprocessors/runningaverage

    RMS_PARAM = 'RMS'
    HOLD_PARAM = 'hold'
    DECAY_PARAM = 'decay'



class MonoEnvelopeDetectAlg(MonoRunAvgDetectAlg):
    pass
