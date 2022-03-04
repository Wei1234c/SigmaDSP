try:
    from ..cell import Cell, LookUpTable

except:
    from cell import Cell, LookUpTable



class DynamicsProcessor(LookUpTable):
    TABLE_PARAM = None

    HOLD_PARAM = None
    DECAY_PARAM = None


    def set_hold_time(self, time_ms, **kwargs):
        self.set_param(int(time_ms * self._dsp.sample_rate / 1000),
                       param_name = self.HOLD_PARAM, **kwargs)


    def set_decay(self, dB_s, **kwargs):
        self.set_param(dB_s / (96 * self._dsp.sample_rate),
                       param_name = self.DECAY_PARAM, **kwargs)



class RMS(Cell):
    RMS_PARAM = 'RMS'


    def set_rms_tc(self, dB_s, **kwargs):  # todo: not sure this fits all needs.
        self.set_param(1 - dB_s / (10 * self._dsp.sample_rate),
                       param_name = self.RMS_PARAM, **kwargs)
