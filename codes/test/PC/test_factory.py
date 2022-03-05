import os

from bridges.ftdi.adapters.micropython import machine
from bridges.ftdi.controllers.i2c import I2cController
from sigma.factory import Factory
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

#  =================================

project_xml_file_url = os.sep.join(['..', '..', '..', 'SigmaStudio projects', 'projects', 'demo', 'demo.xml'])
class_files_root_url = os.sep.join(['..', '..', 'sigma', 'sigma_studio', 'toolbox', 'cells'])

factory = Factory(project_xml_file_url = project_xml_file_url,
                  class_files_root_url = class_files_root_url,
                  dsp = dsp
                  )

print(factory.get_ic().df)
cells = factory.get_cells()
factory.show_methods()

for o in factory.get_cells_manifest():
    print(o)

gain1 = cells['Gain_in0']
gain1.set_dB(0)

# print(factory.get_classes_df())
# tone1 = cells['Tone1_2']
# tone1.set_frequency(440)
# print(factory.get_classes_dict(cells_root_url))

# from class import
# __import__(class_path)
#
# setattr(self, module_name, __import__(module_name))

# cell = factory.get_cell_by_name('Volume_Control_out01')
for cell in cells.values():
    print(cell.properties)
