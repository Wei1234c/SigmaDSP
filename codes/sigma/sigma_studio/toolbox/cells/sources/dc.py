try:
    from .source import Source

except:
    from source import Source



class DC(Source):
    ENABLE_PARAM = None


    def __init__(self, module, dsp = None, value = 1.0):
        super().__init__(module = module, dsp = dsp)
        if value is not None:
            self.set_param(value)



class DCInpAlg(DC):
    ENABLE_PARAM = ''
