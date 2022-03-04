try:
    from ..cell import Cell, LookUpTable

except:
    from cell import Cell, LookUpTable



class Loudness(Cell):
    pass



class LoudnessLH(Loudness, LookUpTable):
    TABLE_PARAM = 'iir_coeff_b0_hi'
