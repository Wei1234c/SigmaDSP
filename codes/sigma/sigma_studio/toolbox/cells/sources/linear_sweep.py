try:
    from .oscillators import Oscillator

except:
    from oscillators import Oscillator



class Sweep(Oscillator):
    ENABLE_PARAM = None
    FREQ_PARAM = None
    FREQ_RATIO = None
    FREQ_MASK = None


    def set_param(self, *args, **kwargs):
        super().set_param(self.freq_increment, self.FREQ_PARAM, send_now = False, **kwargs)
        super().set_param(*args, **kwargs)


    @property
    def freq_increment(self):
        raise NotImplementedError



class LinearSweep(Sweep):
    ENABLE_PARAM = 'ison'
    FREQ_PARAM = 'freq_increment'
    FREQ_RATIO = 1
    FREQ_MASK = 255


    @property
    def freq_increment(self):
        raise NotImplementedError  # todo: not completed.



class LinearSweepAlg(LinearSweep):

    @property
    def freq_increment(self):
        numsteps = self.get_param('numsteps').value
        start_freq = self.get_param('start_freq').value
        stop_freq = self.get_param('stop_freq').value

        return (stop_freq - start_freq) / numsteps



class LinearSweepAlgBurst(LinearSweepAlg):
    pass



class LinearSweepExTrigAlg(LinearSweep):
    ENABLE_PARAM = None



class LinearSweepExTrigAlgBurst(LinearSweepExTrigAlg):
    pass
