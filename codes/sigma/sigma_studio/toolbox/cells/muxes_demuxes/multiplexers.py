try:
    from ..cell import Cell, Slewer

except:
    from cell import Cell, Slewer



class Selector(Cell):

    def switch(self, idx_on, n_options, send_now = True, **kwargs):
        for i in range(n_options):
            self.set_param(1.0 if i == idx_on else 0.0, param_name = str(i), send_now = send_now, **kwargs)



class Multiplexer(Cell):
    pass



class DCinputmuxAlgSlew(Multiplexer, Slewer):
    SLEW_PARAM = 'step'


    @property
    def slew_rate(self):
        slew_bytes = self.get_param(self.SLEW_PARAM).bytes[:self._dsp.N_BYTES_PER_PARAMETER]
        slew = self._dsp.DspNumber.bytes_to_value(slew_bytes)
        return self._get_slew_rate_RC(slew)


    def set_slew_rate(self, slew_rate, **kwargs):
        slew, slew1 = self._get_slew(slew_rate)
        bytes_slew = self._dsp.DspNumber.to_bytes(slew)
        bytes_slew1 = self._dsp.DspNumber.to_bytes(slew1)
        self.set_param(b''.join([bytes_slew, bytes_slew1]), param_name = self.SLEW_PARAM, **kwargs)


    @staticmethod
    def _get_slew(slew_rate):
        slew_rate = int(slew_rate)
        assert 6 <= slew_rate <= 22

        return 1 / (2 ** slew_rate), 1 / (2 ** (23 - slew_rate))



class Switch(Multiplexer, Selector):

    def switch(self, idx_on, **kwargs):
        super().switch(idx_on, n_options = len(self._module._parameters), **kwargs)



class monomux1940ns(Switch):
    pass



class stereomux1940ns(monomux1940ns):
    pass



class monoMuxSwSlew(monomux1940ns):
    SWITCH_PARAM = 'coeffname'


    def __init__(self, module, dsp = None):
        super().__init__(module = module, dsp = dsp)
        self.get_param(param_name = self.SWITCH_PARAM).to_integer()  # cannot tell "0x00 0x00 0x00 0x00" a int for float


    def switch(self, idx_on, **kwargs):
        self.set_param(idx_on, self.SWITCH_PARAM, **kwargs)



class StMuxSwSlew(monoMuxSwSlew):
    pass



class SyncMultiplexAlg(Multiplexer):
    pass
