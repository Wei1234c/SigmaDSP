try:
    from ..cell import Cell

except:
    from cell import Cell



class StateMachine(Cell):
    LIMITS_PARAM = '1start'


    def set_limits(self, limit_low = None, limit_high = None, **kwargs):
        current_bytes = self.get_param(self.LIMITS_PARAM, **kwargs).bytes

        INT_FORMAT = self._dsp.DspNumber.INT_FORMAT

        bytes_down = self._dsp.DspNumber.to_bytes(limit_low, *INT_FORMAT) if limit_low is not None else \
            current_bytes[:self._dsp.N_BYTES_PER_PARAMETER]

        bytes_up = self._dsp.DspNumber.to_bytes(limit_high, *INT_FORMAT) if limit_high is not None else \
            current_bytes[self._dsp.N_BYTES_PER_PARAMETER:]

        self.set_param(b''.join([bytes_down, bytes_up]), param_name = self.LIMITS_PARAM, **kwargs)



class StateMachAlg(StateMachine):
    pass
