# import fx2lp
from bridges.ftdi.adapters.micropython import machine
from bridges.ftdi.controllers.i2c import I2cController
from sigma.sigma_dsp.adau.adau1401 import ADAU1401
from utilities.adapters import peripherals


with_hardware_device = False

if with_hardware_device:
    ctrl = I2cController()
    _machine = ctrl.get_gpio()

    _i2c = ctrl.I2C()

    _pin_reset = _machine.Pin('ADBUS4', mode = machine.Pin.OUT)
    _pin_reset.high()

else:
    _i2c = _pin_reset = None  # using None for testing without actual hardware device.

bus = peripherals.I2C(_i2c)
dsp = ADAU1401(bus, pin_reset = _pin_reset)



def read(n_bytes, address = None):
    ba = dsp.eeprom.read(n_bytes, address)
    print([hex(b) for b in ba])
    return ba



ba = read(8)

dsp.eeprom.write(bytes(8))
read(8)

dsp.eeprom.write(ba)
read(8)

ba = ['0x1', '0x0', '0x5', '0x0', '0x8', '0x1c', '0x0', '0x58']
ba = bytes([int(b, 16) for b in ba])

dsp.eeprom.write(ba)
read(8)
