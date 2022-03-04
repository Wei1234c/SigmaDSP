try:
    from ..cell import Cell

except:
    from cell import Cell



class Clip(Cell):
    CLIP_PARAM = None



class HardClipNewAlg(Clip):
    CLIP_PARAM = 'up'


    def set_thresholds(self, threshold_low = None, threshold_high = None, **kwargs):
        if (threshold_low is not None) and (threshold_high is not None):
            assert threshold_low < threshold_high, f'Must down < up : {threshold_low} < {threshold_high}'

        bytes_up = self._dsp.DspNumber.to_bytes(threshold_high) if threshold_high is not None else b''
        bytes_down = self._dsp.DspNumber.to_bytes(threshold_low) if threshold_low is not None else b''

        self.set_param(b''.join([bytes_up, bytes_down]), param_name = self.CLIP_PARAM, **kwargs)



class SoftClipAlgG(Clip):

    def set_alpha(self, alpha, **kwargs):
        assert 0 < alpha <= 10, '0 < alpha <= 10'

        for param_name, value in zip(['alpha', 'alpham1', 'onethird', ], [alpha, 1 / alpha, 1 / 3]):
            self.set_param(value, param_name, send_now = False, **kwargs)

        self.set_param(2 / 3, 'twothird', send_now = True, **kwargs)



Cubic = SoftClipAlgG
