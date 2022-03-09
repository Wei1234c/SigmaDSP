class slice:  # for ESP32, which doesn't have "slice".

    def __init__(self, start, stop):
        self.start = start
        self.stop = stop



Message_ID_SLICE = slice(0, 1)
MessageWrite_LENGTH_SLICE = slice(1, 3)
MessageWrite_LENGTH_SLICE_LENGTH = MessageWrite_LENGTH_SLICE.stop - MessageWrite_LENGTH_SLICE.start

MessageWrite_DEVICE_ADDRESS_SLICE = slice(3, 4)
MessageWrite_DEVICE_ADDRESS_SLICE_LENGTH = MessageWrite_DEVICE_ADDRESS_SLICE.stop - MessageWrite_DEVICE_ADDRESS_SLICE.start

MessageWrite_SUBADDRESS_SLICE = slice(4, 6)
MessageWrite_SUBADDRESS_SLICE_LENGTH = MessageWrite_SUBADDRESS_SLICE.stop - MessageWrite_SUBADDRESS_SLICE.start

MessageWrite_DEVICE_ADDRESS_SUBADDRESS_LENGTH = MessageWrite_DEVICE_ADDRESS_SLICE_LENGTH + \
                                                MessageWrite_SUBADDRESS_SLICE_LENGTH
MessageWrite_DATA_SLICE = slice(6, None)

MessageDelay_DELAY_SLICE = slice(1, 3)
MessageDelay_DELAY_SLICE_LENGTH = MessageDelay_DELAY_SLICE.stop - MessageDelay_DELAY_SLICE.start



class Message:
    BYTEORDER = 'big'
    MESSAGE_TYPES = {'End'                             : 0x00,
                     'Write'                           : 0x01,
                     'Delay'                           : 0x02,
                     'No operation executed'           : 0x03,
                     'Set multiple writeback'          : 0x04,
                     'Set WB to falling edge sensitive': 0x05,
                     'End and wait for writeback'      : 0x06}

    MESSAGE_TYPES_value_key = {v: k for k, v in MESSAGE_TYPES.items()}


    def __init__(self, message_type = 'No operation executed'):
        valid_types = self.MESSAGE_TYPES.keys()
        assert message_type in valid_types, f'{message_type} is not in valid types: {valid_types}.'

        self.message_type = message_type
        self.message_id = self.MESSAGE_TYPES[self.message_type]


    def __str__(self):
        return str({'Type'   : self.message_type,
                    'Type ID': self.message_id})


    @property
    def _body(self) -> bytes:
        return b''


    @property
    def bytes(self):
        return b''.join([bytes([self.message_id]), self._body])


    @classmethod
    def from_bytes(cls, message_bytes):
        message_id = message_bytes[0]
        message_type = cls.MESSAGE_TYPES_value_key[message_id]

        if message_type == 'Write':
            device_address = int.from_bytes(
                message_bytes[MessageWrite_DEVICE_ADDRESS_SLICE.start:MessageWrite_DEVICE_ADDRESS_SLICE.stop],
                'big')

            subaddress = int.from_bytes(
                message_bytes[MessageWrite_SUBADDRESS_SLICE.start: MessageWrite_SUBADDRESS_SLICE.stop],
                'big')

            nbytes_data = int.from_bytes(message_bytes[MessageWrite_LENGTH_SLICE.start: MessageWrite_LENGTH_SLICE.stop],
                                         'big') - MessageWrite_DEVICE_ADDRESS_SUBADDRESS_LENGTH

            data_slice = slice(MessageWrite_DATA_SLICE.start, MessageWrite_DATA_SLICE.start + nbytes_data)

            message = MessageWrite(subaddress = subaddress,
                                   data = message_bytes[data_slice.start: data_slice.stop],
                                   device_address = device_address)

            return message, message_bytes[data_slice.stop:]

        elif message_type == 'Delay':
            delay_ms = int.from_bytes(message_bytes[MessageDelay_DELAY_SLICE.start: MessageDelay_DELAY_SLICE.stop],
                                      'big')
            message = MessageDelay(delay_ms = delay_ms)
            return message, message_bytes[MessageDelay_DELAY_SLICE.stop:]

        elif message_type == 'End':
            message = Message(message_type = message_type)
            return message, b''

        else:
            message = Message(message_type = message_type)
            return message, message_bytes[1:]


    @classmethod
    def messages_from_bytes(cls, message_bytes):
        messages = []

        while len(message_bytes) > 0:
            message, message_bytes = cls.from_bytes(message_bytes)
            messages.append(message)

        return Messages(messages)


    @staticmethod
    def messages_from_SigmaStudio_files(file_NumBytes, file_TxBuffer):
        with open(file_NumBytes, 'tr') as f:
            sizes = ''.join(f.readlines()).replace('\n', ',').replace(' ', '').split(',')
            segment_sizes = tuple(int(s) for s in sizes if s != '')

        with open(file_TxBuffer, 'tr') as f:
            bytes_str = ''.join(f.readlines()).replace('\n', ',').replace(' ', '').split(',')
            bytes_array = bytes(int(s, 16) for s in bytes_str if s.startswith('0x'))

        messages = []

        for n_bytes in segment_sizes:
            subaddress = int.from_bytes(bytes_array[:2], 'big')
            data = bytes_array[2:n_bytes]
            messages.append(MessageWrite(subaddress, data))
            bytes_array = bytes_array[n_bytes:]

        return Messages(messages)



class MessageWrite(Message):
    DEVICE_ADDRESS = 0x00


    def __init__(self, subaddress, data, device_address = DEVICE_ADDRESS):
        super().__init__(message_type = 'Write')

        self.device_address = device_address
        self.subaddress = subaddress
        self.data = data


    def __str__(self):
        return str({'Type'          : self.message_type,
                    'Type ID'       : self.message_id,
                    'Device Address': self.device_address,
                    'Sub Address'   : f'0x{self.subaddress:04X}',
                    'Data'          : self.data})


    @property
    def _body(self) -> bytes:
        bytes_length = (MessageWrite_DEVICE_ADDRESS_SUBADDRESS_LENGTH +
                        len(self.data)).to_bytes(MessageWrite_LENGTH_SLICE_LENGTH, self.BYTEORDER)

        bytes_device_address = self.device_address.to_bytes(MessageWrite_DEVICE_ADDRESS_SLICE_LENGTH,
                                                            self.BYTEORDER)

        bytes_subaddress = self.subaddress.to_bytes(MessageWrite_SUBADDRESS_SLICE_LENGTH, self.BYTEORDER)

        return b''.join([bytes_length, bytes_device_address, bytes_subaddress, self.data])



class MessageDelay(Message):

    def __init__(self, delay_ms = 0):
        super().__init__(message_type = 'Delay')

        self.delay_ms = delay_ms


    def __str__(self):
        return str({'Type'    : self.message_type,
                    'Type ID' : self.message_id,
                    'Delay ms': self.delay_ms})


    @property
    def _body(self) -> bytes:
        return self.delay_ms.to_bytes(MessageDelay_DELAY_SLICE_LENGTH, self.BYTEORDER)



class Messages(list):

    @property
    def bytes(self):
        return b''.join([m.bytes for m in self])
