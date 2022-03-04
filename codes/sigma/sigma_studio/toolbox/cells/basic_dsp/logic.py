try:
    from ..cell import Cell, LookUpTable
    from ..basic_dsp.adjustable_gain import AdjustableGain
    from ..muxes_demuxes.state_machine import StateMachine

except:
    from cell import Cell, LookUpTable
    from adjustable_gain import AdjustableGain
    from state_machine import StateMachine



class Logic(Cell):
    pass



class BufferAlg(Logic):
    OUTPUT_PARAM = 'output1'


    def set_target_bit(self, bit_idx = 0, **kwargs):
        self.set_param(2 ** bit_idx, self.OUTPUT_PARAM, **kwargs)



class EQ1940Invert(Logic, AdjustableGain):
    ENABLE_PARAM = 'gain'


    def enable(self, value = True, param_name = None, send_now = True, **kwargs):
        param_name = self.ENABLE_PARAM if param_name is None else param_name
        self.set_gain(-1.0 if value else 1.0, param_name = param_name, send_now = send_now, **kwargs)


    def set_dB(self, *args, **kwargs):
        raise NotImplementedError



class ZeroCompareAlg(BufferAlg):
    OUTPUT_PARAM = 'output1'



class Toggle(BufferAlg):
    pass



class OneShotRiseAlg(Toggle):
    pass



class OneShotRiseResetFixedAlg(Toggle):
    pass



class OneShotFallAlg(Toggle):
    pass



class OneShotResetFallAlg(Toggle):
    pass



class TolAlg(Logic, StateMachine):
    LIMITS_PARAM = '0lower'



class ValueCrossAlg(Logic):
    TARGET_PARAM = 'Cross'
