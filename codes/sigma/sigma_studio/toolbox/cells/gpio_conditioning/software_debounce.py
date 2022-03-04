try:
    from ..cell import Cell

except:
    from cell import Cell



class SoftwareDebounce(Cell):
    DEBOUNCE_COUNT_PARAM = 'countmax'


    def set_max_count(self, count, **kwargs):
        self.set_param(count, param_name = self.DEBOUNCE_COUNT_PARAM, **kwargs)



class SWDebounceAlg(SoftwareDebounce):
    pass
