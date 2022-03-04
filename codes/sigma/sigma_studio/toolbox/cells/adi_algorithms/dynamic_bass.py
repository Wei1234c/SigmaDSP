try:
    from ..cell import Cell, LookUpTable
    from ..sources.oscillators import Oscillator

except:
    from cell import Cell, LookUpTable
    from oscillators import Oscillator



class DynamicBass(Cell):
    pass



class BassBAlg(DynamicBass, LookUpTable, Oscillator):
    TABLE_PARAM = 'compbase_table1_comp'



class BassBAlg_stereo(DynamicBass, LookUpTable, Oscillator):
    TABLE_PARAM = 'compbase_table1_comp'



class EnhanceAlg(DynamicBass, Oscillator):
    pass



class EnhanceAlg_st(DynamicBass, Oscillator):
    pass



class SuperBassAlgSWSlew(DynamicBass, LookUpTable):
    TABLE_PARAM = 'comp_base'
