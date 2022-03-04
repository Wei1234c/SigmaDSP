# https://wiki.analog.com/resources/tools-software/sigmastudio/toolbox/filters/general2ndorder

try:
    from ..cell import Cell, Slewer, LookUpTable
    from .nth_order import NthOrderFilter

except:
    from cell import Cell, Slewer, LookUpTable
    from nth_order import NthOrderFilter



class SecondOrderFilter(Cell):
    pass



class SecondOrderFilterCoeffs(SecondOrderFilter, NthOrderFilter):
    pass



class SecondOrderFilterLUT(SecondOrderFilter, LookUpTable):
    TABLE_PARAM = None


    def get_coefficients(self, **kwargs):
        return self.get_table(**kwargs).numbers


    def set_coefficients(self, coefficients, **kwargs):
        self.set_table(coefficients, **kwargs)



class EQ1940Dual(SecondOrderFilterCoeffs):
    pass



class EQ1940DualS(SecondOrderFilterCoeffs):
    pass



class EQ1940Hexa(SecondOrderFilterCoeffs):
    pass



class EQ1940HexaS(SecondOrderFilterCoeffs):
    pass



class EQ1940Penta(SecondOrderFilterCoeffs):
    pass



class EQ1940PentaS(SecondOrderFilterCoeffs):
    pass



class EQ1940Quad(SecondOrderFilterCoeffs):
    pass



class EQ1940QuadS(SecondOrderFilterCoeffs):
    pass



class EQ1940Single(SecondOrderFilterCoeffs):
    pass



class EQ1940SingleS(SecondOrderFilterCoeffs):
    pass



class EQ1940Triple(SecondOrderFilterCoeffs):
    pass



class EQ1940TripleS(SecondOrderFilterCoeffs):
    pass



class IdxIndpEQAlg2ChanDP_Gen(SecondOrderFilterLUT):
    TABLE_PARAM = '00b0'



class IdxIndpEQAlgDB_Gen(SecondOrderFilterLUT):
    TABLE_PARAM = '00b0'



class IdxIndpEQAlg_Gen(SecondOrderFilterLUT):
    TABLE_PARAM = '00b0'



class IdxIndpEQSTAlg_Gen(SecondOrderFilterLUT):
    TABLE_PARAM = '00b0'



class IndexSelectFiltDoubleS4p6Alg(SecondOrderFilterLUT, Slewer):
    TABLE_PARAM = '_0b0'
    SLEW_PARAM = 'step'



class IndexSelectFiltSP4p6Alg(SecondOrderFilterLUT, Slewer):
    TABLE_PARAM = '_0b0'
    SLEW_PARAM = 'step'



class PEQ1Chan(SecondOrderFilterCoeffs):
    pass



class PEQ1Chan_SinglePrec(SecondOrderFilterCoeffs):
    pass



class ParamToneIndexAlgFix(SecondOrderFilterLUT):
    TABLE_PARAM = '_0b0'



class ParamToneIndexwStepAlgFix(SecondOrderFilterLUT):
    TABLE_PARAM = '_0b0'
