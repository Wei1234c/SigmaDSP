try:
    from .source import Source

except:
    from source import Source



class Switch(Source):
    ENABLE_PARAM = 'ison'


    def __init__(self, module, dsp = None, is_integer = False):
        super().__init__(module = module, dsp = dsp)
        self._is_integer = is_integer


    def switch(self, on, **kwargs):
        state = (int if self._is_integer else float)(bool(on))
        self.set_param(state, param_name = self.ENABLE_PARAM, **kwargs)


    def enable(self, *args, **kwargs):
        raise NotImplementedError



class SwitchAlg(Switch):
    pass
