import gc
import os
import sys


try:
    from sigma.bus import adapters
    # from sigma.sigma_dsp.adau import ADAU
    from sigma.sigma_dsp.adau.adau1401 import ADAU1401 as ADAU
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

    bus = adapters.I2C(_i2c)

    project_xml_file_url = os.sep.join(['..', '..', '..', 'SigmaStudio projects', 'projects', 'demo', 'demo.xml'])
    # class_files_root_url = os.sep.join(['..', '..', 'sigma', 'sigma_studio', 'toolbox', 'cells'])

except:

    #  for ESP32 ===========================
    import config
    import peripherals
    import adapters
    # from adau import ADAU
    from adau1401 import ADAU1401 as ADAU
    from ufactory import Factory


    # from factory import Factory

    with_hardware_device = True

    if with_hardware_device:
        _i2c = peripherals.I2C.get_uPy_i2c(id = -1,
                                           scl_pin_id = config.I2C_SCL_PIN_ID,
                                           sda_pin_id = config.I2C_SDA_PIN_ID)
    else:
        _i2c = None  # using None for testing without actual hardware device.

    bus = adapters.I2C(_i2c)

    project_xml_file_url = 'demo_upy.xml'



def collect_garbage():
    gc.collect()
    if sys.platform == 'esp32':
        print('[Memory - free: {}   allocated: {}]'.format(gc.mem_free(), gc.mem_alloc()))



dsp = ADAU(bus)

factory = Factory(project_xml_file_url = project_xml_file_url,
                  dsp = dsp,
                  # temp_folder = '../PC/temp'
                  )

print('factory ready.')

# # # for testing on ESP32 =============================
# # # dsp, factory ======================================
#
# from test_adau_upy import dsp, factory, collect_garbage

# # IO ==============================
#
# class mo:
#     pass
#
#
#
# param = mo()
# param.address = 8
#
# param.type = int
# param.bytes = bytes([0, 0, 0, 1])
# param.size = len(param.bytes)
# # dsp.write_parameter(param)
# print(dsp.read_parameter(param))
#
# # IC and Parameter ==============================
#
# collect_garbage()
# ic = factory.get_ic()
# collect_garbage()
# cells = factory.get_cells(ic)
# collect_garbage()
# print(cells.keys())
# # ==============================
