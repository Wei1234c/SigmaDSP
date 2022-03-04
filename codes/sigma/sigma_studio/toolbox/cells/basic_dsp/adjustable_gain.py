from math import log10


try:
    from ..cell import Cell

except:
    from cell import Cell



class AdjustableGain(Cell):
    GAIN_PARAM = None


    @staticmethod
    def dB_to_gain(dB):
        return 10 ** (dB / 20)


    @staticmethod
    def gain_to_dB(gain):
        return log10(gain) * 20


    def set_gain(self, gain, param_name = None, **kwargs):
        param_name = self.GAIN_PARAM if param_name is None else param_name
        self.set_param(gain, param_name = param_name, **kwargs)


    def set_dB(self, dB, param_name = None, **kwargs):
        self.set_gain(self.dB_to_gain(dB), param_name = param_name, **kwargs)


    def get_gain(self, param_name = None, **kwargs):
        param_name = self.GAIN_PARAM if param_name is None else param_name
        return self.get_param(param_name = param_name, **kwargs).value


    def get_dB(self, param_name = None, **kwargs):
        gain = self.get_gain(param_name = param_name, **kwargs)
        return self.gain_to_dB(gain)



class Gain1940AlgNS(AdjustableGain):
    GAIN_PARAM = ''
