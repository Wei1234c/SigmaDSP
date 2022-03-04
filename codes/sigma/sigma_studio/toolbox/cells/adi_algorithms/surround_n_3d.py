try:
    from ..basic_dsp.adjustable_gain import AdjustableGain

except:
    from adjustable_gain import AdjustableGain



class SurroundN3D(AdjustableGain):
    pass



class ADIVirtualAlg(SurroundN3D):
    pass



class PhatStereoAlg(SurroundN3D):
    pass



class SuperPhatAlg(SurroundN3D):
    pass
