from bridges.ftdi.adapters.micropython import machine
from bridges.ftdi.controllers.i2c import I2cController
from sigma.bus import adapters
from sigma.sigma_dsp.adau.adau1401 import ADAU1401
from sigma.sigma_dsp.messages import Message, Messages


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

message_bytes = dsp.eeprom.read(1024 * 32)
messages = Message.messages_from_bytes(message_bytes)

print(len(messages))
print(len(messages.bytes))
print(len(messages[0].bytes))
print(messages[0].bytes)
print(len(Messages(messages[1:]).bytes))

for m in messages:
    print(m)

for m in messages:
    if m.message_type == 'Write':
        dsp.control.write_message(m)

print('Done')
