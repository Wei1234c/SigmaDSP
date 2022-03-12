from bridges.ftdi.adapters.micropython import machine
from bridges.ftdi.controllers.i2c import I2cController
from sigma.bus import adapters
from sigma.sigma_dsp.adau.adau1401 import ADAU1401
from sigma.sigma_studio.project.project_xml import get_ICs
from sigma.sigma_studio.toolbox.cells.sources.oscillators import *


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

#  =================================
import os


project_xml_file_url = os.sep.join(['..', '..', '..', 'SigmaStudio projects', 'projects', 'demo', 'demo.xml'])
ic = get_ICs(project_xml_file_url)[0]

m = ic.modules['Tone1']
cell = sin_lookupAlg(m, dsp)

print(cell.name)
print(cell.PARAMETER_SHORT_NAMES)

cell.enable(False)

print()
# print(cell.get_coefficients())
# cell.get_table()
# cell.set_coefficients(
# [('0B1', 0.00379860401153564), ('1B1', 0.00759732723236084), ('2B1', 0.00379860401153564), ('1A1', 1.76088035106659), ('2A1', -0.776074886322021), ('0B2', 0.00391614437103271), ('1B2', 0.00783228874206543), ('2B2', 0.00391614437103271), ('1A2', 1.81534111499786), ('2A2', -0.831005573272705), ('0B3', 0.00413775444030762), ('1B3', 0.00827550888061523), ('2B3', 0.00413775444030762), ('1A3', 1.91809153556824), ('2A3', -0.934642672538757)]
#     )

# cell.enable()
# cell.set_gain(0.8)
# cell.set_hold_time(10)
# p = cell.get_param('slope_1')
# print(p.numbers)
cell.set_frequency(1200)
# table = cell.get_table()
# cell.set_table([1.0, 2.0, 3.0, 4.0, 5.0, 1.0])
# print(table.numbers)
# print(table.bytes)
# cell.set_table(b'\x00\x80\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
# table.set_numbers(table.numbers)
# print(table.bytes)
# cell.set_debounce_counter(3)
# print(cell.readback().value)
# cell.set_table(bytes(132))
# cell.set_hold_time(50)
# print(cell.set_toggle_bit(22))
# print(cell.get_value())
# cell.enable(True)
# print(cell.get_coefficient(0, 'b2'))
# print(cell.get_param('F3_b1').value)
# cell.set_trig_time(200)
# cell.set_dB(0)
# cell.set_dB(0, 1)
# cell.set_gain(0, 1, 0)
# cell.switch(2)
# cell.set_limits(-127, 127)
# cell.set_volume(0)
# cell.set_slew_rate(6)
# print(cell.slew_rate)
# cell.set_alpha(1212)
# print(cell.get_param('step').value)
# cell.set_thresholds(0.5, 0.4)
# p_name = 'up'
# cell.set_param(0.4, p_name, algorithm_idx = 0)
# print(cell.get_param(p_name, algorithm_idx = 0).value)
print()
