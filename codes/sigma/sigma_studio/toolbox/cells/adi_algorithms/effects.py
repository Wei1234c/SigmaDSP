try:
    from ..cell import Cell, LookUpTable

except:
    from cell import Cell, LookUpTable



class Effect(Cell):
    pass



class Chorus(Effect, LookUpTable):
    TABLE_PARAM = 'src_64'
