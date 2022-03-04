try:
    from ..cell import Cell, Slewer
    from .nth_order import NthOrderFilter

except:
    from cell import Cell, Slewer
    from nth_order import NthOrderFilter



class FirstOrderFilter(Cell):
    pass



class FistOrderSingle(FirstOrderFilter, NthOrderFilter):
    pass



class ParamToneIndexwStepAlg1stOrder(FirstOrderFilter, Slewer):
    pass
