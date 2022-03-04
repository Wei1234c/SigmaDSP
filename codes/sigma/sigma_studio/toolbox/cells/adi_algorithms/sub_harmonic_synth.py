try:
    from ..cell import Cell, LookUpTable

except:
    from cell import Cell, LookUpTable



class SubHarmonicSynth(Cell):
    pass



class SimpleSubHarmonicAlg(SubHarmonicSynth):
    pass



class SubHarmonicAlg(SubHarmonicSynth, LookUpTable):
    TABLE_PARAM = 'prelpb0'
