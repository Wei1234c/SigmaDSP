try:
    from ..cell import Cell, Slewer

except:
    from cell import Cell, Slewer



class Mute(Cell):
    ENABLE_PARAM = 'mute'


    @property
    def muted(self):
        return self.get_param(param_name = self.ENABLE_PARAM).value == 0.0


    def mute(self, value = True, **kwargs):
        self.set_param(0.0 if value else 1.0, param_name = self.ENABLE_PARAM, send_now = True, **kwargs)



class MuteNoSlewAlg(Mute):
    pass



class MuteSWSlewAlg(Mute, Slewer):
    SLEW_PARAM = 'step'
