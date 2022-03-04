from math import ceil


try:
    from signal_generators import interfaces
    from utilities.numeric import Number

except:
    import interfaces
    from numeric import Number

FREQ_DEFAULT = None



class Device(interfaces.DeviceBase):
    FREQ_REF = None


    def __init__(self, registers_map = None, registers_values = None,
                 commands = None):
        super().__init__(registers_map = registers_map,
                         registers_values = registers_values,
                         commands = commands)


    @property
    def is_virtual_device(self):
        return self._bus.is_virtual_device



class DspNumber(Number):
    N_BITS_A = 5
    N_BITS_B = 23
    LIMIT = 1 << (N_BITS_A - 1)

    N_BITS = N_BITS_A + N_BITS_B
    N_BITS_INTEGER = N_BITS_A
    N_BYTES = ceil(N_BITS / 8)
    INT_FORMAT = (N_BITS, 0)
    FLOAT_FORMAT = (N_BITS_INTEGER, N_BITS - N_BITS_INTEGER)
