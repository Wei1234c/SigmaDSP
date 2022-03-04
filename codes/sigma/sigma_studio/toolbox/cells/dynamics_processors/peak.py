try:
    from .dynamics_processors import DynamicsProcessor
    from ..basic_dsp.adjustable_gain import AdjustableGain

except:
    from dynamics_processors import DynamicsProcessor
    from adjustable_gain import AdjustableGain



class Peak(DynamicsProcessor):
    TABLE_PARAM = ''

    HOLD_PARAM = 'hold'
    DECAY_PARAM = 'decay'



class MonoChannelSeparateDetectNoPost2prec(Peak):
    pass



class MonoChannelSeparateDetectNoPost2precFastRelease(Peak):
    pass



class MonoChannelSingleDetectNoPost2prec(Peak):
    pass



class MonoPeak_StResHiRange_NoExtDet_NoPos_2ndGen(Peak):
    pass



class MonoPeak_StResHiRange_NoExt_NoPos_2ndGen(Peak):
    pass



class StereoPeak_StResHiRange_NoExt_NoPos_2ndGen(Peak):
    pass



class MonoExtraDetectAttackHoldDecay_B(Peak, AdjustableGain):
    TABLE_PARAM = 'table'
    HOLD_PARAM = 'hold0'
    GAIN_PARAM = EXTERNAL_DETECT_PARAM = 'extdetgain'



class TwoChannelSeparateDetect2prec(Peak, AdjustableGain):
    GAIN_PARAM = 'post_gain'



class TwoChannelSingleDetect2prec(TwoChannelSeparateDetect2prec):
    pass



class TwoChannelSeparateDetectNoPost2prec(Peak):
    pass



class TwoChannelSeparateDetectNoPost2precFastRelease(Peak):
    pass



class TwoChannelSingleDetectNoPost2prec(Peak):
    pass



class MonoChannelSeparateDetectNoPost2precExpGain(Peak):
    pass



class MonoChannelSeparateDetectNoPost2precFastReleaseExpGain(Peak):
    pass



class MonoChannelSingleDetectNoPost2precExpGain(Peak):
    pass



class MonoPeak_StResHiRange_NoExtDet_NoPos_2ndGenExpGain(Peak):
    pass



class TwoChannelSeparateDetectNoPost2precExpGain(Peak):
    pass



class TwoChannelSeparateDetectNoPost2precFastReleaseExpGain(Peak):
    pass



class TwoChannelSingleDetectNoPost2precExpGain(Peak):
    pass
