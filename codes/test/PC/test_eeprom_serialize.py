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
def print_eeprom_messages():
    for m in dsp.eeprom.messages:
        print(m)



print_eeprom_messages()

file_name = 'E2Prom.bin'
# dsp.eeprom.to_file(file_name)

# dsp.eeprom.clear()

ba = dsp.eeprom.from_file(file_name)
print_eeprom_messages()

for m in dsp.control.messages_from_bytes(ba):
    print(m)
