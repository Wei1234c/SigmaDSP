try:
    from .oscillators import Oscillator

except:
    from oscillators import Oscillator



class Chime(Oscillator):
    pass



class OptimizedChimeGUIVCOAlg_rev(Chime):
    ENABLE_PARAM = 'ison'
    FREQ_PARAM = None
    FREQ_RATIO = 1
    FREQ_MASK = 255


    def set_timingtable(self, time_points):
        raise NotImplementedError  # todo: not completed.


    def set_freqincrement(self, freqincrements):
        raise NotImplementedError  # todo: not completed.



class Optimized2ChimeAlgWGainGUI(OptimizedChimeGUIVCOAlg_rev):

    def set_gaintable(self, gaintable):
        raise NotImplementedError  # todo: not completed.


    def set_gainincrementtable(self, gainincrementtable):
        raise NotImplementedError  # todo: not completed.



class Optimized2ChimeAlgWGainGUIEndlessLoop2ndGen(Optimized2ChimeAlgWGainGUI):
    pass
