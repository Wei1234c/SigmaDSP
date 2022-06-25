try:
    from ..cell import Cell

except:
    from cell import Cell



class LevelDetector(Cell):
    TCONST_PARAM = 'TCONST'
    DECAY_PARAM = 'decay'


    def get_coefficient(self, band_idx, coff_name, **kwargs):
        return self.get_param(f'F{band_idx}_{coff_name}', **kwargs).value


    def set_coefficient(self, band_idx, coff_name, value, **kwargs):
        return self.set_param(value, f'F{band_idx}_{coff_name}', **kwargs)



class LevelDetGrow(LevelDetector):
    pass



class LevelDetGrowPinOut(LevelDetector):
    pass



class LevelDetGrowPinOutSimp(LevelDetector):
    pass



class LevelDetGrowPinOutSimpDouble(LevelDetGrowPinOutSimp):
    pass



class SevenBandLevelDet(LevelDetector):
    pass



class SingleBandLevelDet(LevelDetector):
    HOLD_PARAM = 'hold'


    def set_hold_time(self, time_ms, **kwargs):  # todo: need to validate formular..
        self.set_param(int(time_ms * self._dsp.sample_rate / 1000),
                       param_name = self.HOLD_PARAM, **kwargs)


    def get_coefficient(self, *args, **kwargs):
        raise NotImplementedError


    def set_coefficient(self, *args, **kwargs):
        raise NotImplementedError



class SingleBandLevelDetwOutDisplay2ndGen(SingleBandLevelDet):
    pass
