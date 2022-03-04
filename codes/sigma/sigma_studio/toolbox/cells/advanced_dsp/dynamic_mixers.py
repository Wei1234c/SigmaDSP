try:
    from ..cell import Slewer
    from ..dynamics_processors.dynamics_processors import RMS

except:
    from cell import Slewer
    from dynamics_processors import RMS



class AdaptiveMixer(Slewer, RMS):
    RMS_PARAM = 'RMS'
    SLEW_PARAM = 'step'



class DynamicsMixer1940Alg(AdaptiveMixer):
    pass



class DynamicsMixer1940AlgSingle(AdaptiveMixer):
    pass
