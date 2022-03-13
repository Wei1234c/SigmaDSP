from math import ceil


try:
    from .. import dsp_processor
    from ..messages import Message, MessageWrite

except:
    import dsp_processor
    from messages import Message, MessageWrite

SAMPLING_FREQ_DEFAULT = 48000



class ADAU(dsp_processor.Device):
    I2C_ADDRESS = 0x68 >> 1
    I2C_ADDRESS_EEPROM = 0xA0 >> 1
    SPI_ADDRESS = 0x00
    READ_ONLY_REGISTERS = []

    FREQ_REF = 12.288e6
    SAMPLE_RATE = 48e3
    POWER_UP_TIME_ms = 85

    HARDWARE_READBACK_NUMERIC_FORMAT = (5, 19)


    class DspNumber(dsp_processor.DspNumber):
        pass


    class _Base:

        def __init__(self, parent):
            self._parent = parent


    class _RAM(_Base):

        ADDRESS_MIN = 0x0000
        ADDR_INCREMENT = None
        N_BYTES = None


        def __init__(self, parent, i2c_address = None):
            super().__init__(parent)
            self._i2c_address = i2c_address or self._parent._i2c_address


        # # ==============================================================
        # CHUNK_SIZE_READ = 0x0200
        # CHUNK_SIZE_WRITE = 0x020
        #
        # def read(self, n_bytes, address = None):
        #     address = self.ADDRESS_MIN if address is None else address
        #     ba = []
        #
        #     for addr, nbytes in self._chunks_to_read(n_bytes, address):
        #         ba.append(self._read(n_bytes = nbytes, address = addr))
        #
        #     return b''.join(ba)
        #
        #
        # def write(self, bytes_array, address = None):
        #     address = self.ADDRESS_MIN if address is None else address
        #
        #     for addr, data_bytes in self._chunks_to_write(bytes_array, address):
        #         self._write(bytes_array = data_bytes, address = addr)
        #
        #
        # def _chunks_to_read(self, n_bytes, address):
        #     chunk_size = self.CHUNK_SIZE_READ
        #     assert chunk_size % self.ADDR_INCREMENT == 0
        #
        #     n_chunks = ceil(n_bytes / chunk_size)
        #
        #     for i in range(n_chunks):
        #         addr = address + (i * chunk_size // self.ADDR_INCREMENT)
        #         nbytes = min(n_bytes - i * chunk_size, chunk_size)
        #         yield addr, nbytes
        #
        #
        # def _chunks_to_write(self, bytes_array, address):
        #     chunk_size = self.CHUNK_SIZE_WRITE
        #     assert chunk_size % self.ADDR_INCREMENT == 0
        #
        #     n_chunks = ceil(len(bytes_array) / chunk_size)
        #
        #     for i in range(n_chunks):
        #         addr = address + (i * chunk_size // self.ADDR_INCREMENT)
        #         yield addr, bytes_array[:chunk_size]
        #         bytes_array = bytes_array[chunk_size:]
        #
        #
        # def _read(self, n_bytes, address):
        #     return self._parent._read_addressed_bytes(i2c_address = self._i2c_address,
        #                                               sub_address = address,
        #                                               n_bytes = n_bytes)
        #
        #
        # def _write(self, bytes_array, address):
        #     return self._parent._write_addressed_bytes(i2c_address = self._i2c_address,
        #                                                sub_address = address,
        #                                                bytes_array = bytes_array)
        #
        # # ==============================================================

        def read(self, n_bytes, address):
            return self._parent._read_addressed_bytes(i2c_address = self._i2c_address,
                                                      sub_address = address,
                                                      n_bytes = n_bytes)


        def write(self, bytes_array, address):
            return self._parent._write_addressed_bytes(i2c_address = self._i2c_address,
                                                       sub_address = address,
                                                       bytes_array = bytes_array)


        # ==============================================================

        @property
        def bytes(self):
            return self.read(self.N_BYTES)


        # Message related ==========================

        @property
        def message(self):
            return MessageWrite(subaddress = self.ADDRESS_MIN, data = self.bytes)


        @message.setter
        def message(self, message):
            assert message.message_type == 'Write'
            assert message.subaddress == self.ADDRESS_MIN
            self.write(message.data)


        # =============================

        def clear(self):
            self.write(bytes(self.N_BYTES))


        def to_file(self, binary_file_name):
            with open(binary_file_name, 'wb') as f:
                f.write(self.bytes)


        def from_file(self, binary_file_name):
            with open(binary_file_name, 'rb') as f:
                ba = f.read()
                self.write(ba)
                return ba


    class _EEPROM(_RAM):

        ADDRESS_MIN = 0x0000
        ADDRESS_MAX = 0x3FFF
        N_BITS = 8
        ADDR_INCREMENT = N_BITS // 8
        N_BYTES = (ADDRESS_MAX - ADDRESS_MIN + 1) * ADDR_INCREMENT
        N_BYTES_PER_PAGE = 32
        N_ADDRESS_BYTES = 2

        INTERFACE_REGISTERS_ADDRESS_MIN = 32


        def _get_pages(self, bytes_array, address):

            page_idx = address // self.N_BYTES_PER_PAGE
            sub_addr_start = address % self.N_BYTES_PER_PAGE

            while len(bytes_array) > 0:
                page_addr = page_idx * self.N_BYTES_PER_PAGE
                addr_start = page_addr + sub_addr_start
                addr_stop = page_addr + self.N_BYTES_PER_PAGE
                len_seg = addr_stop - addr_start

                yield bytes_array[:len_seg], addr_start

                bytes_array = bytes_array[len_seg:]
                page_idx += 1
                sub_addr_start = 0


        def write(self, bytes_array, address = None):
            address = self.ADDRESS_MIN if address is None else address

            for data_bytes, addr in self._get_pages(bytes_array, address):
                super().write(bytes_array = data_bytes, address = addr)

            return len(bytes_array)


        @property
        def bytes(self):
            return self.messages.bytes


        # message ==========================================

        @property
        def messages(self):
            return self._parent.control.messages_from_bytes(self.read(self.N_BYTES))


        @messages.setter
        def messages(self, messages):
            self.write(messages.bytes)


    class _ParameterRAM(_RAM):

        NAME = 'Param'
        ADDRESS_MIN = 0x0000
        ADDRESS_MAX = 0x03FF
        N_BITS = 32
        ADDR_INCREMENT = N_BITS // 8
        N_BYTES = (ADDRESS_MAX - ADDRESS_MIN + 1) * ADDR_INCREMENT

        SAFELOAD_REGISTERS_PAIRS = ((0x0815, 0x0810),
                                    (0x0816, 0x0811),
                                    (0x0817, 0x0812),
                                    (0x0818, 0x0813),
                                    (0x0819, 0x0814))
        N_SAFELOAD_REGISTERS = len(SAFELOAD_REGISTERS_PAIRS)
        N_BYTES_SAFELOAD_ADDRESS_REGISTERS = 2
        N_BYTES_SAFELOAD_DATA_REGISTERS = 5
        IST_REGISTER_ADDRESS = 0x081C
        N_BYTES_IST_REGISTER = 2
        IST_BIT_IDX = 5


        def __init__(self, parent, i2c_address = None):
            super().__init__(parent, i2c_address)
            self._safeload_idx = 0


        @property
        def n_bytes_max_to_safeload(self):
            return self.N_SAFELOAD_REGISTERS * self._parent.N_BYTES_PER_PARAMETER


        # parameter =================================
        def read_parameter(self, param):  # param: project_xml.Parameter
            if not self._parent.is_virtual_device:
                return self.read(n_bytes = param.size, address = param.address)


        def write_parameter(self, param, send_now = True):  # param: project_xml.Parameter
            if not self._parent.is_virtual_device:

                if param.type is bytes:  # not a number
                    if param.size <= self.n_bytes_max_to_safeload:
                        self.safe_loads(param_address = param.address, data_bytes = param.bytes)
                    else:
                        self.write(bytes_array = param.bytes, address = param.address)

                else:  # is a number
                    self.safe_load(param_address = param.address,
                                   data_bytes = param.bytes,
                                   send_now = send_now)


        # safe load =================================
        def safe_load(self, param_address, data_bytes, send_now = True):
            n_bytes_pre_pend = self.N_BYTES_SAFELOAD_DATA_REGISTERS - len(data_bytes)
            data_bytes = b''.join([bytes(n_bytes_pre_pend), data_bytes])
            assert len(data_bytes) == self.N_BYTES_SAFELOAD_DATA_REGISTERS

            self._safeload_idx = (self._safeload_idx + 1) % self.N_SAFELOAD_REGISTERS
            pair = self.SAFELOAD_REGISTERS_PAIRS[self._safeload_idx]
            param_address_bytes = param_address.to_bytes(self.N_BYTES_SAFELOAD_ADDRESS_REGISTERS, 'big')

            self._parent.write_addressed_bytes(address = pair[0], bytes_array = param_address_bytes)
            self._parent.write_addressed_bytes(address = pair[1], bytes_array = data_bytes)

            if send_now:
                self.initiate_safeload_transfer()


        def safe_loads(self, param_address, data_bytes):
            n_bytes_per_number = self._parent.N_BYTES_PER_PARAMETER
            n_numbers = ceil(len(data_bytes) / n_bytes_per_number)

            for i in range(n_numbers):
                idx_start = i * n_bytes_per_number
                self.safe_load(param_address = param_address + idx_start,
                               data_bytes = data_bytes[:n_bytes_per_number],
                               send_now = False)
                data_bytes = data_bytes[n_bytes_per_number:]

            self.initiate_safeload_transfer()


        def initiate_safeload_transfer(self):
            address = self.IST_REGISTER_ADDRESS
            n_bytes = self.N_BYTES_IST_REGISTER

            value = int.from_bytes(self._parent.read_addressed_bytes(address, n_bytes), 'big')
            ba = (value | (1 << self.IST_BIT_IDX)).to_bytes(n_bytes, 'big')

            self._parent.write_addressed_bytes(address, ba)


    class _Control(_Base):
        SAMPLING_RATE_Hz = {44100: 0, 48000: 0, 96000: 1, 192000: 2}
        SAMPLING_RATE_RATIO = {1: 0, 2: 1, 4: 2}
        SAMPLING_RATE_RATIO_value_key = {v: k for k, v in SAMPLING_RATE_RATIO.items()}


        # Messages operations ===================
        @classmethod
        def messages_from_bytes(cls, message_bytes):
            return Message.messages_from_bytes(message_bytes)


        def write_message(self, message):
            if message.message_type == 'Write':
                self._parent.write_addressed_bytes(message.subaddress, message.data)


        # eeprom operations ===================

        def reload_from_eeprom(self):
            for message in self._parent.eeprom.messages:
                self.write_message(message)


    def __init__(self, bus, i2c_address = I2C_ADDRESS, sample_rate = None, **kwargs):

        super().__init__(**kwargs)

        self._bus = bus
        self._i2c_address = i2c_address
        self.sample_rate = self.SAMPLE_RATE if sample_rate is None else sample_rate

        self.init()


    def _build(self):
        self.control = self._Control(self)
        self.parameter_ram = self._ParameterRAM(self)
        self.eeprom = self._EEPROM(self, self.I2C_ADDRESS_EEPROM)
        self.N_BYTES_PER_PARAMETER = self.DspNumber.N_BYTES

        # ====================================    


    def init(self):
        self._action = 'init'

        self._build()
        self.start()


    def enable_output(self, value = True):
        pass


    @property
    def status(self):
        return


    # encapsulated hardware functions =======================

    def read_parameter(self, *args, **kwargs):
        return self.parameter_ram.read_parameter(*args, **kwargs)


    def write_parameter(self, *args, **kwargs):
        return self.parameter_ram.write_parameter(*args, **kwargs)


    def reload_from_eeprom(self):
        self.control.reload_from_eeprom()


    # hardware related IO ===============================================

    def _read_addressed_bytes(self, i2c_address, sub_address, n_bytes):
        return self._bus.read_addressed_bytes(i2c_address, sub_address, n_bytes)


    def read_addressed_bytes(self, sub_address, n_bytes):
        return self._read_addressed_bytes(self._i2c_address, sub_address, n_bytes)


    def _write_addressed_bytes(self, i2c_address, sub_address, bytes_array):
        return self._bus.write_addressed_bytes(i2c_address, sub_address, bytes_array)


    def write_addressed_bytes(self, address, bytes_array):
        return self._write_addressed_bytes(self._i2c_address, address, bytes_array)

    # ======================================
