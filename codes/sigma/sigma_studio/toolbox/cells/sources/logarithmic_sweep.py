try:
    from .oscillators import Oscillator
    from .linear_sweep import Sweep

except:
    from oscillators import Oscillator
    from linear_sweep import Sweep



class LogarithmicSweep(Sweep):
    ENABLE_PARAM = 'ison'
    FREQ_PARAM = 'freq_increment'
    FREQ_RATIO = 1
    FREQ_MASK = 255


    @property
    def freq_increment(self):
        raise NotImplementedError  # todo: not completed.



class LogSweepAlg(LogarithmicSweep):

    @property
    def freq_increment(self):
        numsteps = self.get_param('numsteps').value
        start_freq = self.get_param('start_freq').value
        stop_freq = self.get_param('stop_freq').value

        raise NotImplementedError  # todo: not completed.



class LogSweepExTrigAlg(LogSweepAlg):
    ENABLE_PARAM = None



class sweep_lookup_Alg(LogarithmicSweep):
    ENABLE_PARAM = None
    FREQ_PARAM = 'increment'
    FREQ_RATIO = 1
    FREQ_MASK = 255
