try:
    from .software_debounce import SoftwareDebounce

except:
    from software_debounce import SoftwareDebounce



class RotaryEncoder(SoftwareDebounce):
    DEBOUNCE_COUNT_PARAM = 'countmax'



class RotaryEncAlg(RotaryEncoder):
    pass
