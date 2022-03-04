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

# =============================================


dsp.parameter_ram.to_file('parameter_ram.bin')
ba_params = dsp.parameter_ram.bytes
dsp.parameter_ram.clear()
dsp.parameter_ram.from_file('parameter_ram.bin')

dsp.program_ram.to_file('program_ram.bin')
ba_program = dsp.program_ram.bytes
dsp.program_ram.clear()
dsp.program_ram.from_file('program_ram.bin')
