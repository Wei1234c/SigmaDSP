try:
    from ..cell import Cell
    from ..basic_dsp.adjustable_gain import AdjustableGain

except:
    from cell import Cell
    from adjustable_gain import AdjustableGain



class BasicDSP(Cell):
    pass



class DspReadback(BasicDSP):
    DATA_PARAM = ''


    @property
    def address(self):
        return self._module._algorithms[0].parameters[self.DATA_PARAM].address


    def readback(self):
        return self._dsp.readback(self.address)



class ReadBackAlg(DspReadback):
    pass



class RealTimeDisplay(DspReadback):
    pass



class Delay(BasicDSP):
    DELAY_PARAM = ''
    BUFFERSIZE_PARAM = None


    def set_max_buffer_size(self, n = 1, **kwargs):
        self.set_param(int(n), param_name = self.BUFFERSIZE_PARAM, **kwargs)


    def get_max_buffer_size(self, **kwargs):
        return self.get_param(param_name = self.BUFFERSIZE_PARAM, **kwargs).value


    def set_delayed_samples(self, n = 0, **kwargs):
        self.set_param(int(n), param_name = self.DELAY_PARAM, **kwargs)


    def get_delayed_samples(self, **kwargs):
        return self.get_param(param_name = self.DELAY_PARAM, **kwargs).value


    def set_delayed_ms(self, delayed_ms = 0, **kwargs):
        samples = int(self._dsp.sample_rate * delayed_ms / 1000)
        self.set_delayed_samples(samples, **kwargs)


    def get_delayed_ms(self, **kwargs):
        samples = self.get_delayed_samples(**kwargs)
        return samples * 1000 / self._dsp.sample_rate



class FractionalDelay(Delay):
    DELAY_PARAM = ''
    BUFFERSIZE_PARAM = 'Limit1buffersize'


    def set_delayed_percentage(self, percentage, **kwargs):
        assert 0 <= percentage <= 1, f'0 <= percentage ({percentage}) <= 1'
        self.set_param(percentage, param_name = self.DELAY_PARAM, **kwargs)


    def get_delayed_percentage(self, **kwargs):
        return self.get_param(param_name = self.DELAY_PARAM, **kwargs).value


    def set_delayed_ms(self, delayed_ms = 0, **kwargs):
        self.set_delayed_percentage(delayed_ms / self.max_delayed_ms, **kwargs)


    def get_delayed_ms(self, **kwargs):
        percentage = self.get_delayed_percentage(**kwargs)
        return self.max_delayed_ms * percentage


    @property
    def max_delayed_ms(self):
        samples_max = self.get_max_buffer_size()
        return samples_max / self._dsp.sample_rate * 1000


    def set_delayed_samples(self, *args, **kwargs):
        raise NotImplementedError


    def get_delayed_samples(self, **kwargs):
        raise NotImplementedError



class FractionalVoltageControlledDelayNoZip(FractionalDelay):
    pass



class MultiTapVoltageControlledDelay(Delay):
    DELAY_PARAM = ''
    BUFFERSIZE_PARAM = 'Limit1buffersize'


    def set_delayed_percentage(self, percentage, **kwargs):
        assert 0 <= percentage <= 1, f'0 <= percentage ({percentage}) <= 1'
        self.set_param(percentage, param_name = self.DELAY_PARAM, **kwargs)


    def set_delayed_samples(self, *args, **kwargs):
        raise NotImplementedError



class MultiTapMixerAlg(Delay, AdjustableGain):
    DELAY_PARAM = 'delay0'
    BUFFERSIZE_PARAM = 'buffersize'
    GAIN_PARAM = 'gain0'



class MulitTapGainAlg200_ADICtrls(Delay, AdjustableGain):
    DELAY_PARAM = 'CurrentReversedDelay1'
    BUFFERSIZE_PARAM = 'buffersize'
    GAIN_PARAM = 'LinearGain1'



class MultCtrlDelGrowAlg(Delay):
    pass



class MultCtrlFracDelGrowFixedAlg(FractionalDelay):
    pass



class VoltageControlledDelay1940NoZipAlgwLimit(Delay):
    BUFFERSIZE_PARAM = 'buffersize'
