import os

from sigma.bus import adapters
from sigma.factory import Factory
from sigma.sigma_dsp.adau.adau1401 import ADAU1401
from usbi.usbi import I2C, release_usb_device


release_usb_device()

with_hardware_device = True  # set True if hardware is connected.

if with_hardware_device:
    i2c = I2C(n_sub_address_bytes = 2)

else:
    i2c = adapters.I2C(None)  # using None for testing without actual hardware device.

dsp = ADAU1401(i2c)

# # ===================================
# n = 32
# addr = 0
#
# ba_to_write = bytes(range(n))
# print('ba_to_write:', [(i) for i in ba_to_write])
#
# # dsp.parameter_ram.write(ba_to_write, addr)
#
# ba_readback = dsp.parameter_ram.read(n_bytes = n, address = addr)
# print('ba_readback:', [(i) for i in ba_readback])
#
# ba_readback = dsp.parameter_ram.read(n_bytes = 4, address = 0)
# print('ba_readback:', [(i) for i in ba_readback])
#
# ba_readback = dsp.parameter_ram.read(n_bytes = 4, address = 1)
# print('ba_readback:', [(i) for i in ba_readback])
#
# print()

# # ===================================
messages = dsp.eeprom.messages
for m in messages:
    print(m)
# print()
# dsp.eeprom.write(messages.bytes)
#
#
# with open('E2Prom.bin', 'br') as f:
#     ba = f.read()
#
# ba1 = dsp.eeprom.read(dsp.eeprom.N_BYTES)
# print(ba == dsp.eeprom.read(dsp.eeprom.N_BYTES))
# print()
# # ===================================
# # ===================================
# n = 32 * 2
# addr = 0
#

# ba = dsp.eeprom.bytes
# print(len(ba))
#
# ba = dsp.parameter_ram.bytes
# print(len(ba))
#
# ba = dsp.program_ram.bytes
# print(len(ba))

#
#
# ba_original = dsp.parameter_ram.read(n, addr)
# print('ba_original:', [(i) for i in ba_original])
#
# ba_to_write = bytes(range(n))
# print('ba_to_write:', [(i) for i in ba_to_write])
#
# dsp.parameter_ram.write(ba_to_write, addr)
# ba_readback = dsp.parameter_ram.read(n, addr)
# print('ba_readback:', [(i) for i in ba_readback])
#
# print(ba_to_write == ba_readback)
#
# ba_to_write = ba_original
# print('ba_to_write:', [(i) for i in ba_to_write])
#
# dsp.parameter_ram.write(ba_to_write, addr)
# ba_readback = dsp.parameter_ram.read(n, addr)
# print('ba_readback:', [(i) for i in ba_readback])
#
# print(ba_readback == ba_original)

#
# # ===================================
print()
#  =================================

project_xml_file_url = os.sep.join(['..', '..', '..', 'SigmaStudio projects', 'projects', 'demo', 'demo.xml'])
class_files_root_url = os.sep.join(['..', '..', 'sigma', 'sigma_studio', 'toolbox', 'cells'])

factory = Factory(project_xml_file_url = project_xml_file_url,
                  class_files_root_url = class_files_root_url,
                  dsp = dsp
                  )

# print(factory.classes_dict)
#
# print(factory.get_ic().df)
ic = factory.get_ic(ic_idx = 0)
cells = factory.get_cells(ic)
# # factory.show_methods()
# #
# # for o in factory.get_cells_manifest():
# #     print(o)
# #
# gain1 = cells['Gain_in0']
# # print(gain1.df)
# print(gain1.get_param('').dumps())
# factory.read_all_parameters(ic)
# gain1.set_dB(0)
#
# # print(factory.get_classes_df())
# # tone1 = cells['Tone1_2']
# # tone1.set_frequency(440)
# # print(factory.get_classes_dict(cells_root_url))
#
# # from class import
# # __import__(class_path)
# #
# # setattr(self, module_name, __import__(module_name))
#
# cell = factory.get_cell_by_name('Volume_Control_out01')
# for cell in cells.values():
#     print(cell.properties)
#
# dsp.control.load_eeprom_from_file('E2Prom.bin')
# dsp.reload_from_eeprom()
#
# # save_parameters_to_eeprom: save current parameters' value to EEPROM.
#
tone1 = cells['Tone1']

# dsp.eeprom.from_file('E2Prom.bin')
# dsp.reload_from_eeprom()
#
# dsp.program_ram.bytes
# dsp.parameter_ram.bytes
#
# tone1.set_frequency(1200)
# factory.save_parameters_to_eeprom()
# dsp.reload_from_eeprom()
# #
# tone1.set_frequency(440)
# factory.save_parameters_to_eeprom()
# dsp.reload_from_eeprom()
