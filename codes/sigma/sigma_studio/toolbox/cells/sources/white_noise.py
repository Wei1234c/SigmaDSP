try:
    from ..sources.source import Source

except:
    from source import Source



class WhiteNoise(Source):
    ENABLE_PARAM = 'enable'
    FREQ_PARAM = None
    FREQ_RATIO = None
    FREQ_MASK = None



class WhiteNAlgNew(WhiteNoise):
    pass
