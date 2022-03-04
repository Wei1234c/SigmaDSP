try:
    from ..cell import Switch

except:
    from cell import Switch



class Counter(Switch):
    ENABLE_PARAM = 'running'
    RESET_PARAM = 'reset'
    STEP_PARAM = 'step'


    def reset(self):
        self.enable(True, param_name = self.RESET_PARAM)
        self.enable(False, param_name = self.RESET_PARAM)



class CountAlg(Counter):
    pass



class StopWatch(Counter):
    ENABLE_PARAM = 'enable'
    RESET_PARAM = 'enable'



class StopWatchAlgReset(StopWatch):
    pass
