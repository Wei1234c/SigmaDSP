try:
    from ..cell import Slewer

except:
    from cell import Slewer



class XFadeAlg(Slewer):
    SLEW_PARAM = 'step'
