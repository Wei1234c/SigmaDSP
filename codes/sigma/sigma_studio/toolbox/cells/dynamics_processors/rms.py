# todo: not completed.

try:
    import dynamics_processors
    from .dynamics_processors import DynamicsProcessor
    from ..basic_dsp.adjustable_gain import AdjustableGain

except:
    import dynamics_processors
    from dynamics_processors import DynamicsProcessor
    from adjustable_gain import AdjustableGain



class RMS(DynamicsProcessor, dynamics_processors.RMS):
    RMS_PARAM = 'RMS'

    TABLE_PARAM = ''

    HOLD_PARAM = 'hold'
    DECAY_PARAM = 'decay'



class MonoAlgDetectInNoPostExpGain(RMS):
    HOLD_PARAM = None
    DECAY_PARAM = None



class MonoAlgDetectInNoPostExpGainNoHoldNoDelay(RMS):
    pass



class MonoNoPostGain3dBFixExpGain(RMS):
    pass



class MonoNoPostGainExpGain(RMS):
    pass



class MonoNoPostGainExpGainNoHoldNoDelay(RMS):
    HOLD_PARAM = None
    DECAY_PARAM = None



class N_ChannelStereoDetectInNoGainBExpGain(RMS):
    pass



class StereoDetectInNoGainExpGainFix(RMS):
    pass



class StereoDetectInNoGainExpGainNoHoldNoDelay(RMS):
    HOLD_PARAM = None
    DECAY_PARAM = None



class TwoChannelExtDetectExpGainAlgNoGain6dBFix(RMS):
    pass



class TwoChannelSingleDetectAlgNoGainExpGain6dBFix(RMS):
    pass



class TwoChannelSingleDetectAlgNoGainExpGainDelayHoldFix(RMS):
    HOLD_PARAM = None
    DECAY_PARAM = None



class TwoChannelSingleDetectExpGainAlgNoGainFix(RMS):
    pass



class TwoChannelSingleDetectExpGainAlg_Hi_Res(RMS):
    pass



class MonoAlgDetectInNoPost(RMS):
    pass



class MonoAlgDetectInNoPostNoHoldNoDelay(RMS):
    HOLD_PARAM = None
    DECAY_PARAM = None



class MonoNoPostGain(RMS):
    pass



class MonoNoPostGainNoHoldNoDelay(RMS):
    HOLD_PARAM = None
    DECAY_PARAM = None



class N_ChannelStereoDetectInNoGainB(RMS):
    pass



class StdRMSCompressorAlgIndp_SecondGen(RMS, AdjustableGain):
    GAIN_PARAM = 'attenuation'



class StdRMSCompressorAlg_2ndGen(RMS, AdjustableGain):
    GAIN_PARAM = 'attenuation'



class StereoDetectInNoGainFix(RMS):
    pass



class StereoDetectInNoGainNoHoldNoDelay(RMS):
    HOLD_PARAM = None
    DECAY_PARAM = None



class TwoChannelSingleDetectAlgNoGainDelayHoldFix(RMS):
    HOLD_PARAM = None
    DECAY_PARAM = None



class TwoChannelSingleDetectAlgNoGainFix(RMS):
    pass



class MonoAlg(RMS, AdjustableGain):
    GAIN_PARAM = 'post_gain'



class MonoAlgDetectIn(MonoAlg):
    pass



class MonoVisualExtOutAlgNew(MonoAlg):
    pass



class StdRMSCompressorExtDetAlg_SecondGen(MonoAlg):
    GAIN_PARAM = 'attenuation'



class StereoDetectInFix(MonoAlg):
    GAIN_PARAM = 'post_gain'



class TwoChannelSingleDetectAlg(MonoAlg):
    GAIN_PARAM = 'post_gain'



class TwoChannelSingleDetectAlgFix(MonoAlg):
    GAIN_PARAM = 'post_gain'



class MonoNoPostGain3dBFix(MonoAlg):
    pass



class TwoChannelExtDetectAlgNoGain6dBFix(MonoAlg):
    pass



class TwoChannelSingleDetectAlgNoGain6dBFix(MonoAlg):
    pass



class TwoChannelSingleDetectAlg_Hi_Res(MonoAlg):
    pass



class limiterAlg(RMS):
    TABLE_PARAM = None
    HOLD_PARAM = None
