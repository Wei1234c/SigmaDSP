try:
    from .peak import Peak
    from ..dynamics_processors.dynamics_processors import DynamicsProcessor, RMS

except:
    from peak import Peak
    from dynamics_processors import DynamicsProcessor, RMS



class Combo(DynamicsProcessor, Peak, RMS):
    TABLE_PARAM = ''

    HOLD_PARAM = 'hold'
    DECAY_PARAM = 'decay'

    HOLD_ALL_PARAM = 'holdAll'
    DECAY_ALL_PARAM = 'decayAll'

    RMS_PARAM = 'RMS'



class PeakRMSComboMon(Combo):
    pass



class PeakRMSComboMonExpGain(Combo):
    pass



class PeakRMSCombo(Combo):
    pass



class PeakRMSComboExpGain(Combo):
    pass
