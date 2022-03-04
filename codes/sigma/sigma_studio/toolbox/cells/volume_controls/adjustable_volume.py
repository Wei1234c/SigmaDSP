try:
    from ..cell import Cell, Slewer
    from ..basic_dsp.adjustable_gain import AdjustableGain

except:
    from cell import Cell, Slewer
    from adjustable_gain import AdjustableGain



class AdjustableVolume(AdjustableGain):
    GAIN_PARAM = None


    def set_volume(self, dB, **kwargs):
        super().set_dB(dB, **kwargs)



class SWGain1940DBAlg(AdjustableVolume, Slewer):
    GAIN_PARAM = 'target'
    SLEW_PARAM = 'step'



class ExtSWGainDB(AdjustableVolume, Slewer):
    GAIN_PARAM = None
    SLEW_PARAM = 'step'
