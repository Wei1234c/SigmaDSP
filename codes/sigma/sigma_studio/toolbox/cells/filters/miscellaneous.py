from math import pi, sin


try:
    from ..cell import Cell, LookUpTable

except:
    from cell import Cell, LookUpTable



class TrackFiltAlg(Cell):
    PARAMS = ['gainLin', 'mask', 'slope_1']



class StateVarQAlg(Cell):
    FREQ_PARAM = 'freq'


    def set_frequency(self, frequency, **kwargs):
        self.set_param(2 * sin(pi * frequency / self._dsp.sample_rate), param_name = self.FREQ_PARAM, **kwargs)



class StateVarAlg(StateVarQAlg):
    FREQ_PARAM = 'freq'
    Q_PARAM = 'oneoverq'


    def set_Q(self, Q, **kwargs):
        self.set_param(1 / Q, param_name = self.Q_PARAM, **kwargs)



class DC_Blocking(Cell):
    TARGET_PARAM = 'pole'



class Deemphasis(Cell):
    PARAMS = ['01', '11', '21']



class PinkFAlg(LookUpTable):
    TABLE_PARAM = 'coeff0a'
    INPUT_GAIN_PARAMS = 'input_gain'
    OUTPUT_GAIN_PARAMS = 'output_gain'
