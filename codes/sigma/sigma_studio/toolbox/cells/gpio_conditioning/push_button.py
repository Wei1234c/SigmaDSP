try:
    from ..cell import Cell
    from ..level_detectors_lookup_tables.lookup_tables import LookupTableAlgNew

except:
    from cell import Cell
    from lookup_tables import LookupTableAlgNew



class PushButton(Cell):
    pass



class ToggleOneAlg(PushButton):
    OUTPUT_PARAM = 'output1'


    def set_toggle_bit(self, bit_idx = 0, **kwargs):
        self.set_param(2 ** bit_idx, self.OUTPUT_PARAM, **kwargs)

        output_values = (0, 1) if bit_idx == 0 else (0, 2 ** (bit_idx - 23))
        return output_values



class ToggleCountAlg(PushButton):
    COUNT_PARAM = 'max'



class ToggleCountAlgG(ToggleCountAlg):
    pass



class pushholdAlg(PushButton):
    # https://wiki.analog.com/resources/tools-software/sigmastudio/toolbox/gpioconditioning/pushbuttonvolume

    HOLDTIME_PARAM = 'holdtime'
    REPEATTIME_PARAM = 'repeattime'


    def _get_time_units(self, time_ms):
        return int(time_ms * self._dsp.sample_rate / 1000)


    def set_hold_time(self, hold_time_ms, **kwargs):
        self.set_param(self._get_time_units(hold_time_ms), param_name = self.HOLDTIME_PARAM, **kwargs)


    def set_repeat_time(self, repeat_time_ms, **kwargs):
        self.set_param(self._get_time_units(repeat_time_ms), param_name = self.REPEATTIME_PARAM, **kwargs)



class pushholdAlg_2in(pushholdAlg):
    pass



class pushholdAlg_MUTE(pushholdAlg):
    pass



class UPDOWNvolAlg_INTF(PushButton, LookupTableAlgNew):
    pass



class UPDOWNvolAlg_mute(PushButton, LookupTableAlgNew):
    pass
