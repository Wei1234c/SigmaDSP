try:
    from ..basic_dsp.adjustable_gain import AdjustableGain

except:
    from adjustable_gain import AdjustableGain



class Mixer(AdjustableGain):
    pass



class NxNMixer1940Alg(Mixer):

    @staticmethod
    def index_to_name(idx_input, idx_output = 0):
        return f'_{idx_output:02d}_{idx_input:02d}'



class SingleCtrlMixer(Mixer):
    GAIN_PARAM = ''



class SingleCtrlMixerNEW(SingleCtrlMixer):
    pass



class SingleCtrlMixerSLEW(SingleCtrlMixer):
    pass



class StereoMixerAlg(SingleCtrlMixer):

    @staticmethod
    def index_to_name(idx = 0):
        return str((idx + 1) * 2)



class StereoMixerAlgSlew(StereoMixerAlg):
    pass



class TwoChanXMixer1940Alg(Mixer):

    @staticmethod
    def index_to_name(idx_input, idx_output = 0):
        return f'{idx_output}{idx_input}'



class ThreeChanXMixer1940Alg(TwoChanXMixer1940Alg):
    pass



class EightChanXMixer1940Alg(TwoChanXMixer1940Alg):
    pass



class MultCtrlMixer1940Alg(Mixer):

    @staticmethod
    def index_to_name(idx = 0):
        return f'_{(idx + 2)}'



class MultCtrlMixerSlewAlg(MultCtrlMixer1940Alg):
    pass
