import gc
import os
import sys



def collect_garbage():
    gc.collect()
    if sys.platform == 'esp32':
        print('[Memory - free: {}   allocated: {}]'.format(gc.mem_free(), gc.mem_alloc()))



try:
    from utilities.adapters import peripherals
    from sigma.sigma_dsp.adau import ADAU
    from sigma.factory.ufactory import Factory
    from bridges.ftdi.controllers.i2c import I2cController
    from bridges.interfaces.micropython.machine import Pin


    # import fx2lp
    #
    #
    # bus = fx2lp.I2C(as_400KHz = True)

    with_hardware_device = False

    if with_hardware_device:
        _i2c = I2cController().I2C()

    else:
        _i2c = pin_reset = None

    bus = peripherals.I2C(_i2c)

    project_xml_file_url = os.sep.join(['..', '..', '..', 'SigmaStudio projects', 'projects', 'demo', 'demo.xml'])
    class_files_root_url = os.sep.join(['..', '..', 'sigma', 'sigma_studio', 'toolbox', 'cells'])

except:

    #  for ESP32 ===========================
    import peripherals
    from adau import ADAU
    from ufactory import Factory


    with_hardware_device = True

    if with_hardware_device:
        _i2c = peripherals.I2C.get_uPy_i2c(id = -1, scl_pin_id = 5, sda_pin_id = 4, freq = 400000)

    else:
        _i2c = None  # using None for testing without actual hardware device.

    bus = peripherals.I2C(_i2c)

    project_xml_file_url = 'demo.xml'
    class_files_root_url = 'cells'

    #  for ESP32 ===========

dsp = ADAU(bus)



class mo:
    pass



param = mo()
param.address = 0
param.bytes = bytes(4)
param.type = float
param.size = len(param.bytes)

dsp.write_parameter(param)
print(dsp.read_parameter(param))

# ======================================
# from test_adau_upy import dsp

factory = Factory(project_xml_file_url = project_xml_file_url,
                  dsp = dsp
                  )

print('factory ready.')
# print(factory.classes_dict)

# cells = factory.get_cells()
# cell = factory.get_cell_by_name('Volume_Control_out01')
# cell.show_methods()

#
# factory = Factory(project_xml_file_url = project_xml_file_url,
#                   # class_files_root_url = class_files_root_url,
#                   dsp = dsp
#                   )
#
# print(factory._get_classes_dict())
