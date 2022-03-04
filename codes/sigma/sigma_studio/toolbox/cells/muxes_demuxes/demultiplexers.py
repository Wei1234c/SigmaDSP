try:
    from ..cell import Cell
    from .multiplexers import Selector

except:
    from cell import Cell
    from multiplexers import Selector



class DeMultiplexer(Cell):
    pass



class Switch(DeMultiplexer, Selector):

    def switch(self, idx_on, **kwargs):
        super().switch(idx_on, n_options = len(self._module._parameters), **kwargs)



class monoDemux1940ns(Switch):
    pass



class monoDemuxSlew(monoDemux1940ns):
    pass



class stereoDemux1940ns(monoDemux1940ns):
    pass



class stereoDemuxSlew(stereoDemux1940ns):
    pass
