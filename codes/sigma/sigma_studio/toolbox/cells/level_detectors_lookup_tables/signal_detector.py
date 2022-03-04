try:
    from ..basic_dsp.adjustable_gain import AdjustableGain
    from .level_detectors import LevelDetector

except:
    from adjustable_gain import AdjustableGain
    from level_detectors import LevelDetector



class SignalDetector(LevelDetector, AdjustableGain):
    THRESHOLD_PARAM = 'threshold'
    TRIG_TIME_PARAM = 'time_constant'


    def set_threshold(self, dB, **kwargs):
        assert -150 <= dB <= 0

        self.set_param(self.dB_to_gain(dB), self.THRESHOLD_PARAM, **kwargs)


    def set_trig_time(self, seconds, **kwargs):
        assert 2 <= seconds <= 200

        step = 1000 / seconds
        time_constant = 1 - (step / (1 << 23))
        self.set_param(time_constant, self.TRIG_TIME_PARAM, **kwargs)



class SignalDetectAlg(SignalDetector):
    pass
