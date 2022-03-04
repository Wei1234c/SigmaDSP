try:
    from .source import Source
    from ..basic_dsp.adjustable_gain import AdjustableGain

except:
    from source import Source
    from adjustable_gain import AdjustableGain



class Oscillator(Source):
    FREQ_PARAM = None
    FREQ_RATIO = None
    FREQ_MASK = None


    def __init__(self, module, dsp = None, frequency = None):
        super().__init__(module = module, dsp = dsp)

        if frequency is not None:
            self.set_frequency(frequency)


    def get_frequency(self, param_name = None, freq_ratio = None, **kwargs):
        param_name = self.FREQ_PARAM if param_name is None else param_name
        freq_ratio = self.FREQ_RATIO if freq_ratio is None else freq_ratio

        increment = self.get_param(param_name, **kwargs).value
        frequency = (increment / freq_ratio) * (self._dsp.sample_rate / 2)

        return frequency


    def set_frequency(self, frequency, param_name = None, freq_ratio = None, mask = None, **kwargs):
        param_name = self.FREQ_PARAM if param_name is None else param_name
        freq_ratio = self.FREQ_RATIO if freq_ratio is None else freq_ratio
        mask = self.FREQ_MASK if mask is None else mask

        increment = self._get_frequency_increment(frequency) * freq_ratio

        if mask is not None:
            self.set_param(mask, param_name = 'mask', send_now = False, **kwargs)
        self.set_param(increment, param_name = param_name, send_now = True, **kwargs)


    def _get_frequency_increment(self, frequency):
        # https://wiki.analog.com/resources/tools-software/sigmastudio/toolbox/sources/sinetone
        return frequency * 2 / self._dsp.sample_rate  # percentage of frequency_max.



class BeepAlg(Oscillator):
    ENABLE_PARAM = 'enable'
    FREQ_PARAM = 'beep_freq'
    FREQ_RATIO = 4
    FREQ_MASK = None


    def enable(self, value = True):
        super().enable(value, param_name = 'kick', send_now = False)
        super().enable(value)



class PulseAlg(Oscillator):
    ENABLE_PARAM = 'ison'
    FREQ_PARAM = 'freq_step'
    FREQ_RATIO = 0.5
    FREQ_MASK = None


    def set_duty_cycle(self, duty_cycle = 0.5, **kwargs):
        self.set_param(duty_cycle, param_name = 'freq_th', send_now = True, **kwargs)


    def isRounded(self, value = True):
        self.enable(value, param_name = 'isRounded')



class sin_lookupAlg(Oscillator):
    ENABLE_PARAM = 'ison'
    FREQ_PARAM = 'increment'
    FREQ_RATIO = 1
    FREQ_MASK = 255



class SquareAlg(sin_lookupAlg):
    ENABLE_PARAM = 'ison'
    FREQ_PARAM = 'freq'
    FREQ_RATIO = 1
    FREQ_MASK = 255



class TriAlg(sin_lookupAlg):
    ENABLE_PARAM = 'ison'
    FREQ_PARAM = 'freq'
    FREQ_RATIO = 1
    FREQ_MASK = 3



class SawAlg(sin_lookupAlg):
    ENABLE_PARAM = 'ison'
    FREQ_PARAM = 'freq'
    FREQ_RATIO = 0.5
    FREQ_MASK = None



class sin_lookupPhase(sin_lookupAlg, AdjustableGain):
    ENABLE_PARAM = None
    FREQ_PARAM = 'increment'
    FREQ_RATIO = 1
    FREQ_MASK = None

    GAIN_PARAM = 'Gain_0'
    PHASE_PARAM = 'Phase_HI0'


    def __init__(self, module, dsp = None, frequency = None, phase_degree = 0):
        self.phase_degree = phase_degree

        super().__init__(module = module, dsp = dsp, frequency = frequency)


    def enable(self, value = True):
        super().enable(self.get_gain() * (1 if value else 0),
                       param_name = self.GAIN_PARAM,
                       send_now = True)


    def set_phase(self, degree, param_name = None, **kwargs):
        self.phase_degree = degree
        param_name = self.PHASE_PARAM if param_name is None else param_name
        self.set_param(int((degree % 360) / 360 * 255), param_name = param_name, **kwargs)



class SquareAlgWithPhase(sin_lookupPhase):
    ENABLE_PARAM = None
    FREQ_PARAM = 'increment'
    FREQ_RATIO = 1
    FREQ_MASK = 255



class TriAlgWithPhase(sin_lookupPhase):
    ENABLE_PARAM = None
    FREQ_PARAM = 'increment'
    FREQ_RATIO = 1
    FREQ_MASK = 3



class SawAlgWithPhase(sin_lookupPhase):
    ENABLE_PARAM = None
    FREQ_PARAM = 'increment'
    FREQ_RATIO = 1
    FREQ_MASK = None
