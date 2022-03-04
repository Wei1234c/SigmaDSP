try:
    from ..cell import LookUpTable

except:
    from cell import LookUpTable



class Hibert(LookUpTable):
    TABLE_PARAM = 'ap1a_'



class HilbertAlg(Hibert):
    pass
