try:
    from ..cell import Cell
    from ..sources.oscillators import Oscillator

except:
    from cell import Cell
    from oscillators import Oscillator



class PitchModifier(Cell):
    pass



class PitchShiftDataCtrlsAlg(PitchModifier):
    pass



class PitchShiftsAlg(PitchModifier, Oscillator):
    FREQ_PARAM = 'freq'
