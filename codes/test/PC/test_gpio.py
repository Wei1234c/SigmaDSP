from bridges.ftdi.adapters.micropython import machine
from bridges.ftdi.controllers.i2c import I2cController
from sigma.bus import adapters
from sigma.sigma_dsp.adau.adau1401 import ADAU1401


with_hardware_device = True

if with_hardware_device:

    ctrl = I2cController()
    _machine = ctrl.get_gpio()

    _i2c = ctrl.I2C()

    _pin_reset = _machine.Pin('ADBUS4', mode = machine.Pin.OUT)
    _pin_reset.high()

else:
    _i2c = _pin_reset = None  # using None for testing without actual hardware device.

bus = adapters.I2C(_i2c)
dsp = ADAU1401(bus, pin_reset = _pin_reset)

# =============================================

import time


dsp.gpio.pin_setting_register_control_port_write_mode = True
print(dsp.gpio.pin_setting_register_control_port_write_mode)

for i in dsp.gpio.PIN_INDICES:
    print(i, dsp.gpio.get_mode(i))



def pin_test(pin_idx):
    mode = dsp.gpio.get_mode(pin_idx)
    dsp.gpio.set_mode(pin_idx, 'GPIO output')

    for l in (0, 1, 0, 1):
        dsp.gpio.set_pin_level(pin_idx, l)
        time.sleep(0.5)

    dsp.gpio.set_mode(pin_idx, mode)



for i in dsp.gpio.PIN_INDICES:
    print(i)
    pin_test(i)

for i in dsp.gpio.PIN_INDICES:
    print(i, dsp.gpio.get_mode(i))

dsp.gpio.pin_setting_register_control_port_write_mode = False
