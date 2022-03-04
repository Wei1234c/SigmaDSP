try:
    from .oscillators import Oscillator

except:
    from oscillators import Oscillator



class VCO(Oscillator):
    ENABLE_PARAM = None
    FREQ_PARAM = None
    FREQ_RATIO = None
    FREQ_MASK = 255



class QuadOutAlg(VCO):
    pass



class VCOAlg(VCO):
    pass



class VCOAlgReset(VCO):
    pass



class VCOFPAlg_(VCO):
    pass



class PulseAlg_withInputPin(VCO):
    ENABLE_PARAM = 'isRounded'
    FREQ_MASK = None


    def is_rounded(self, value = True):
        self.enable(value)
