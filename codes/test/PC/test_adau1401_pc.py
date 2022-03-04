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

dsp.read_all_registers()
dsp.map.print()

dsp._read_register_by_name('DSP Core Control').print()

dsp.adc.mute(True)
dsp.adc.mute(False)
dsp.dac.mute(True)
dsp.dac.mute(False)
dsp.mute(True)
dsp.mute(False)

dsp.dac.power_down(True)
dsp.dac.power_down(False)

dsp.reset()
dsp._read_register_by_name('DSP Core Control').print()
