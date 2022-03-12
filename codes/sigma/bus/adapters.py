import os
import sys


try:
    machine_name = os.uname().machine
except Exception:
    machine_name = os.name

IS_PC = machine_name.startswith('x86_64') or machine_name.startswith('nt')
IS_RPi = machine_name.startswith('armv')
IS_MICROPYTHON = (sys.implementation.name == 'micropython')

VIRTUAL_DEVICE_WARNING = '\n****** Virtual device. Data may not be real ! ******\n'



class Bus:
    DEBUG_MODE = False


    def __init__(self, bus):
        self._bus = bus

        if self.is_virtual_device:
            print(VIRTUAL_DEVICE_WARNING)
        else:
            self.init()


    def init(self):
        if IS_RPi:
            raise NotImplementedError()
        elif IS_MICROPYTHON:
            raise NotImplementedError()
        elif IS_PC:
            raise NotImplementedError()


    @property
    def is_virtual_device(self):
        return self._bus is None



class I2C(Bus):  # transform MicroPython, FTDI I2C objects into unified interface.

    N_SUB_ADDRESS_BYTES = 2


    def __init__(self, i2c, n_sub_address_bytes = N_SUB_ADDRESS_BYTES):
        super().__init__(bus = i2c)

        self.n_sub_address_bytes = n_sub_address_bytes


    def init(self):
        if IS_RPi:
            raise NotImplementedError

        elif IS_MICROPYTHON or IS_PC:
            self._read_bytes = self._bus.readfrom
            self._write_bytes = self._bus.writeto


    def read_bytes(self, i2c_address, n_bytes):
        if not self.is_virtual_device:
            return self._read_bytes(i2c_address, n_bytes)


    def read_addressed_bytes(self, i2c_address, sub_address, n_bytes, n_sub_address_bytes = None, stop = False):
        if not self.is_virtual_device:
            n_sub_address_bytes = self.n_sub_address_bytes if n_sub_address_bytes is None else n_sub_address_bytes

            self._write_bytes(i2c_address, sub_address.to_bytes(n_sub_address_bytes, 'big'), stop)
            return self.read_bytes(i2c_address, n_bytes)


    def write_bytes(self, i2c_address, bytes_array):
        if not self.is_virtual_device:
            return self._write_bytes(i2c_address, bytes_array)


    def write_addressed_bytes(self, i2c_address, sub_address, bytes_array, n_sub_address_bytes = None):
        if not self.is_virtual_device:
            n_sub_address_bytes = self.n_sub_address_bytes if n_sub_address_bytes is None else n_sub_address_bytes

            return self.write_bytes(i2c_address = i2c_address,
                                    bytes_array = sub_address.to_bytes(n_sub_address_bytes, 'big') + bytes_array)
