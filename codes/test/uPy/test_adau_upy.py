import os
import sys


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
    import gc



    def collect_garbage():
        gc.collect()
        if sys.platform == 'esp32':
            print('[Memory - free: {}   allocated: {}]'.format(gc.mem_free(), gc.mem_alloc()))



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

factory = Factory(project_xml_file_url = project_xml_file_url,
                  dsp = dsp
                  )

print('factory ready.')

#
# # for testing on ESP32 =============================
# # dsp, factory ======================================
#
# from test_adau_upy import dsp, factory, collect_garbage
#
# collect_garbage()
# # factory.classes_dict
#
# # ======================================
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
# dsp.read_parameter(param)
#
# # IC and Parameter ==============================
#
# collect_garbage()
# ic = factory.get_ic()
#
# module = ic._modules[0]
# print('module.name:', module.name)
#
# p = module._parameters[0]
# print('parameter.name:', p.name)
# p.dumps()
# p.value
# # p.set_value(2)
# # p.value
# # factory.dsp.write_parameter(p)
# factory.dsp.read_parameter(p)
# dsp.read_addressed_bytes(0, 4)
#
# # ==============================
#
#
# collect_garbage()
# cell = factory.get_cell_by_name(ic._modules[0].name, ic)
#
# # ==============================
