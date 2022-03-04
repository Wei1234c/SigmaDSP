from sigma.sigma_dsp.messages import Message, MessageWrite, MessageDelay
from sigma.sigma_studio.project.project_xml import get_IC


messages = [MessageWrite(0x081c, bytes([0x00, 0x40])),
            *[Message('No operation executed') for i in range(18)],
            MessageWrite(0x0800, bytes(32)),

            MessageDelay(0x2ff),
            *[Message('End') for i in range(2)],

            MessageDelay(0x2ff),
            *[Message('End') for i in range(2)],
            ]

message_bytes = b''.join([m.bytes for m in messages])
print([hex(b) for b in message_bytes])

while len(message_bytes) > 0:
    message, message_bytes = Message.from_bytes(message_bytes)
    print(message.message_type)

# ============================

messages = Message.messages_from_SigmStudio_files('NumBytes_IC_1.dat', 'TxBuffer_IC_1.dat')

with open('E2Prom.bin', 'rb') as f:
    messages = Message.messages_from_bytes(f.read())

for m in messages:
    print(m)

import os
from sigma.sigma_dsp.adau.adau1401 import ADAU1401
from utilities.adapters import peripherals


project_xml_file_url = os.sep.join(['..', '..', '..', 'SigmaStudio projects', 'projects', 'demo', 'demo.xml'])
ic = get_IC(project_xml_file_url)

bus = peripherals.I2C(None)
dsp = ADAU1401(bus)

messages = dsp.eeprom.generate_messages(segments_head = [(0x081c, bytes([0x00, 0x18]))],
                                        segments_tail = [(r.address, r.bytes) for r in
                                                         (ic.registers['Param'],
                                                          ic.programs['Program Data'],
                                                          ic.registers['IC 1.HWConFiguration'],
                                                          ic.registers['IC 1.CoreRegister'],)
                                                         ])
for m in messages:
    print(m)

dsp.interface_registers[3].print()
dsp.auxiliary_adc_data_registers[3].print()
