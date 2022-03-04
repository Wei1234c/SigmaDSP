try:
    from ..cell import Switch

except:
    from cell import Switch



class SampleAndHold(Switch):
    ENABLE_PARAM = 'active'



class SampleAndHoldAlg(SampleAndHold):
    pass
