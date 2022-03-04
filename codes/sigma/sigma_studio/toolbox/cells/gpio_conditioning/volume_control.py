try:
    from ..cell import Cell, Slewer
    from .push_button import pushholdAlg
    from .software_debounce import SoftwareDebounce
    from ..level_detectors_lookup_tables.lookup_tables import LookupTableAlgNew

except:
    from cell import Cell, Slewer
    from push_button import pushholdAlg
    from software_debounce import SoftwareDebounce
    from lookup_tables import LookupTableAlgNew



class VolumeControl(Cell):
    pass



class PushButtonVolAlg(VolumeControl, pushholdAlg, LookupTableAlgNew, Slewer):
    HOLDTIME_PARAM = 'holdtime'
    REPEATTIME_PARAM = 'repeattime'

    TABLE_PARAM = 'table_p0'
    MAXINDEX_PARAM = 'maxindex'

    SLEW_PARAM = 'step'



class PushButtonNoMuteAlg(PushButtonVolAlg):
    pass



class RotaryVolAlg(VolumeControl, LookupTableAlgNew, Slewer, SoftwareDebounce):
    DEBOUNCE_COUNT_PARAM = 'countmax'
