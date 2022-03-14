import time
from math import ceil


try:
    from ..adau import ADAU, SAMPLING_FREQ_DEFAULT
    from utilities.register import RegistersMap
    from .registers_map import _get_all_registers
    from ....sigma_dsp.messages import Message, MessageWrite, MessageWrite_SUBADDRESS_SLICE

except:
    from adau import ADAU, SAMPLING_FREQ_DEFAULT
    from register import RegistersMap
    from registers_map import _get_all_registers
    from messages import Message, MessageWrite, MessageWrite_SUBADDRESS_SLICE



class ADAU1701(ADAU):
    class _RAM(ADAU._RAM):

        # chunks ==============================================================
        # for USBi as USB-I2C converter. USBi hangs when handling long chunk (> 512K bytes) of data.

        CHUNK_SIZE_READ = 500
        CHUNK_SIZE_WRITE = 60


        @classmethod
        def _chunks_to_read(cls, n_bytes, address, n_bytes_per_address = 1):
            chunk_size = cls.CHUNK_SIZE_READ
            n_chunks = ceil(n_bytes / chunk_size)
            assert chunk_size % n_bytes_per_address == 0

            for i in range(n_chunks):
                addr = address + (i * chunk_size // n_bytes_per_address)
                nbytes = min(n_bytes - i * chunk_size, chunk_size)
                yield addr, nbytes


        @classmethod
        def _chunks_to_write(cls, bytes_array, address, n_bytes_per_address = 1):
            chunk_size = cls.CHUNK_SIZE_WRITE
            n_chunks = ceil(len(bytes_array) / chunk_size)
            assert chunk_size % n_bytes_per_address == 0

            for i in range(n_chunks):
                addr = address + (i * chunk_size // n_bytes_per_address)
                yield addr, bytes_array[:chunk_size]
                bytes_array = bytes_array[chunk_size:]


        def read(self, n_bytes, address = None):
            address = self.ADDRESS_MIN if address is None else address
            ba = []

            for addr, nbytes in self._chunks_to_read(n_bytes, address, self.ADDR_INCREMENT):
                ba.append(self._parent._bus.read_addressed_bytes(i2c_address = self._i2c_address,
                                                                 sub_address = addr,
                                                                 n_bytes = nbytes))
            return b''.join(ba)


        def write(self, bytes_array, address = None):
            address = self.ADDRESS_MIN if address is None else address

            for addr, data_bytes in self._chunks_to_write(bytes_array, address, self.ADDR_INCREMENT):
                self._parent._bus.write_addressed_bytes(i2c_address = self._i2c_address,
                                                        sub_address = addr,
                                                        bytes_array = data_bytes)

        # chunks ==============================================================


    class _EEPROM(ADAU._EEPROM, _RAM):

        # message ==========================================
        @property
        def message(self):
            raise NotImplementedError


        @message.setter
        def message(self, message):
            raise NotImplementedError


        @staticmethod
        def _find_message_write(messages, subaddress):
            for message in messages:
                if message.message_type == 'Write' and \
                        message.subaddress == subaddress:
                    return message


        @property
        def params_message(self):
            return self._find_message_write(self.messages, self._parent.parameter_ram.ADDRESS_MIN)


        @property
        def program_message(self):
            return self._find_message_write(self.messages, self._parent.program_ram.ADDRESS_MIN)


        def save_as_message(self, address, data_bytes):
            messages = self.messages
            message = self._find_message_write(messages, address)

            if message is not None:
                assert len(data_bytes) == len(message.data)

                message.data = data_bytes
                self.write(messages.bytes)
                return

            messages.append(MessageWrite(subaddress = address, data = data_bytes))
            self.write(messages.bytes)


        @classmethod
        def generate_messages(cls, segments_head, segments_tail):
            messages = [MessageWrite(subaddress = addr, data = data) for addr, data in segments_head]
            messages.extend([Message(message_type = 'No operation executed')] *
                            (cls.INTERFACE_REGISTERS_ADDRESS_MIN - sum(len(m.bytes) for m in messages) -
                             MessageWrite_SUBADDRESS_SLICE.stop))
            messages.extend([MessageWrite(subaddress = addr, data = data) for addr, data in segments_tail])
            messages.append(Message(message_type = 'End and wait for writeback'))
            messages.append(Message(message_type = 'End'))

            return messages


        # serialization =====================================

        def to_file(self, binary_file_name):
            with open(binary_file_name, 'wb') as f:
                f.write(self.messages.bytes)


        # ===================================================
        def enable_write(self, value = True):
            if self._parent._pin_write_protect is not None:
                self._parent._pin_write_protect.value(0 if value else 1)


    class _ParameterRAM(ADAU._ParameterRAM, _RAM):

        def safe_loads(self, param_address, data_bytes):
            assert self.safeload_done, 'Previous safeload is still on going.'

            super().safe_loads(param_address = param_address, data_bytes = data_bytes)


        def initiate_safeload_transfer(self):
            self._parent._write_element_by_name('IST', 1)


        @property
        def safeload_done(self):
            return self._parent._read_element_by_name('IST').value == 0


    class _Control(ADAU._Control):

        # ======================
        def power_down_voltage_reference(self, value = True):
            if value and not self._parent.is_virtual_device:
                assert self._parent.adc.is_power_down and self._parent.dac.all_power_down, \
                    'ADCs and DACs need to power down first.'

            self._parent._write_element_by_name('VBPD', 1 if value else 0)
            self._parent._write_element_by_name('VRPD', 1 if value else 0)


        def power_up(self):
            self._parent.reference_clock.power_down_oscillator(False)
            self.power_down_voltage_reference(False)
            self._parent.dac.power_down(False)
            self._parent.adc.power_down(False)
            self.setup_control_registers(True)


        def power_down(self):
            self.setup_control_registers(False)
            self._parent.adc.power_down(True)
            self._parent.dac.power_down(True)
            self.power_down_voltage_reference(True)
            self._parent.reference_clock.power_down_oscillator(True)


        def setup_control_registers(self, value = True):
            self.mute(not value)
            self._parent.control.freeze_internal_registers(not value)
            self._parent.dac.initialize(value)


        def freeze_internal_registers(self, value = True):
            self._parent._write_element_by_name('CR', 0 if value else 1)


        def mute(self, value = True):
            self._parent.adc.mute(value)
            self._parent.dac.mute(value)


        # ======================

        def switch_to_SPI_mode(self):
            assert self._parent._pin_write_protect is not None, 'No Write_Protect pin.'
            for i in range(3):
                for level in (1, 0, 1):
                    self._parent._pin_write_protect.value(level)
                    time.sleep(0.001)


        def self_boot_mode(self, value = True):
            if value:
                self._parent.eeprom.enable_write(False)
            self._parent._pin_self_boot.value(1 if value else 0)


        def write_back(self):
            assert self._parent._pin_write_back is not None, 'No Write Back pin.'
            for level in (1, 0, 1) if self._parent._write_back_on_falling_edge else (0, 1, 0):
                self._parent._pin_write_back.value(level)
                time.sleep(0.001)


        @property
        def sampling_ratio(self):
            return self.SAMPLING_RATE_RATIO_value_key[self._parent._read_element_by_name('SR').value]


        @sampling_ratio.setter
        def sampling_ratio(self, ratio = 1):
            self._parent._write_element_by_name('SR', self.SAMPLING_RATE_RATIO[ratio])


        @property
        def sampling_rate_is_192KHz(self):
            return self.sampling_ratio == 4


        # eeprom operations ===================

        def load_eeprom_from_file(self, binary_file_name):
            self._parent.eeprom.from_file(binary_file_name)


        def dump_eeprom_to_file(self, binary_file_name):
            self._parent.eeprom.to_file(binary_file_name)


        def save_parameters_to_eeprom(self, data_bytes):
            self._parent.eeprom.save_as_message(address = self._parent.parameter_ram.ADDRESS_MIN,
                                                data_bytes = data_bytes)


        def reload_from_eeprom(self):
            for message in self._parent.eeprom.messages:
                if message.message_type == 'Write' and \
                        message.subaddress not in (self._parent.parameter_ram.ADDRESS_MIN,
                                                   self._parent.program_ram.ADDRESS_MIN):
                    self.write_message(message)

            self._parent.parameter_ram.write(self._parent.eeprom.params_message.data)
            self._parent.program_ram.write(self._parent.eeprom.program_message.data)


        # text file operations ===================

        def load_SigmaStudio_files(self, file_NumBytes, file_TxBuffer):
            for message in Message.messages_from_SigmaStudio_files(file_NumBytes, file_TxBuffer):
                self.write_message(message)


        # XML operations ===================

        def write_xml_register(self, register):  # register: project_xml.Register
            self._parent.write_addressed_bytes(sub_address = register.address, bytes_array = register.bytes)


        def write_xml_ic(self, ic):  # ic: project_xml.IC
            for reg in ic._programs + ic._registers:
                self.write_xml_register(reg)


    class _ADC(ADAU._Base):

        ADC_INPUT_RESISTOR_TOTAL_DEFAULT = 20000
        ADC_INTERNAL_RESISTOR = 2000


        def mute(self, value = True):
            self._parent._write_element_by_name('ADM', 0 if value else 1)


        # =================

        def power_down(self, value = True):
            self._parent._write_element_by_name('AAPD', 1 if value else 0)


        @property
        def is_power_down(self):
            return self._parent._read_element_by_name('AAPD').value == 1


        @classmethod
        def adc_input_resistor_total(cls, input_voltage_rms = 2, sampling_frequency = SAMPLING_FREQ_DEFAULT):
            return input_voltage_rms * cls.ADC_INPUT_RESISTOR_TOTAL_DEFAULT * SAMPLING_FREQ_DEFAULT // sampling_frequency


        @classmethod
        def adc_input_resistor_external(cls, input_voltage_rms = 2, sampling_frequency = SAMPLING_FREQ_DEFAULT):
            return cls.adc_input_resistor_total(input_voltage_rms, sampling_frequency) - cls.ADC_INTERNAL_RESISTOR


        @classmethod
        def adc_reference_resistor_total(cls, sampling_frequency = SAMPLING_FREQ_DEFAULT):
            return cls.ADC_INPUT_RESISTOR_TOTAL_DEFAULT * SAMPLING_FREQ_DEFAULT // sampling_frequency


        @classmethod
        def adc_reference_resistor_external(cls, sampling_frequency = SAMPLING_FREQ_DEFAULT):
            return cls.adc_reference_resistor_total(sampling_frequency) - cls.ADC_INTERNAL_RESISTOR


    class _DAC(ADAU._Base):

        DACs_INDICES = (0, 1, 2, 3)


        def initialize(self, value = True):
            self._parent._write_element_by_name('DS', 1 if value else 0)


        def mute(self, value = True):
            self._parent._write_element_by_name('DAM', 0 if value else 1)


        # ========================

        def power_down(self, value = True, indices = None):
            indices = self.DACs_INDICES if indices is None else indices

            for idx in indices:
                self._parent._write_element_by_name(f'D{idx}PD', 1 if value else 0)


        def is_power_down(self, idx):
            return self._parent._read_element_by_name(f'D{idx}PD').value == 1


        @property
        def all_power_down(self):
            return all(self.is_power_down(idx) for idx in self.DACs_INDICES)


    class _SerialInput(ADAU._Base):

        MODEs = {'I2S'                     : 0,
                 'Left-justified'          : 1,
                 'TDM'                     : 2,
                 'Right-justified, 24 bits': 3,
                 'Right-justified, 20 bits': 4,
                 'Right-justified, 18 bits': 5,
                 'Right-justified, 16 bits': 6}


        def set_mode(self, mode = 'I2S'):
            valids = self.MODEs.keys()
            assert mode in valids, 'valid mode:{}'.format(valids)

            self._parent._write_element_by_name('M', self.MODEs[mode])


        @property
        def left_channel_LRclk_polarity(self):
            return self._parent._read_element_by_name('ILP').value


        @left_channel_LRclk_polarity.setter
        def left_channel_LRclk_polarity(self, polarity = 0):
            self._parent._write_element_by_name('ILP', bool(polarity))


        @property
        def data_on_Bclk_rising_edge(self):
            return self._parent._read_element_by_name('IBP').value


        @data_on_Bclk_rising_edge.setter
        def data_on_Bclk_rising_edge(self, on_rising_edge = False):
            self._parent._write_element_by_name('IBP', bool(on_rising_edge))


        def enable(self, value = True):
            self._parent.gpio.enable_serial_input(value)


    class _SerialOutput(ADAU._Base):

        BCLK_FREQUENCY_DIVIDER = {16: 0, 8: 1, 4: 2, 2: 3}
        BCLK_FREQUENCY_DIVIDER_value_key = {v: k for k, v in BCLK_FREQUENCY_DIVIDER.items()}

        LRCLK_FREQUENCY_DIVIDER = {1024: 0, 512: 1, 256: 2}
        WORD_LENGTH_BITS = {24: 0, 20: 1, 16: 2}

        MSB_POSITION_DELAY = {1: 0, 0: 1, 8: 2, 12: 3, 16: 4}


        @property
        def left_channel_LRclk_polarity(self):
            return self._parent._read_element_by_name('OLRP').value


        @left_channel_LRclk_polarity.setter
        def left_channel_LRclk_polarity(self, polarity = 0):
            self._parent._write_element_by_name('OLRP', bool(polarity))


        @property
        def data_on_Bclk_rising_edge(self):
            return self._parent._read_element_by_name('OBP').value


        @data_on_Bclk_rising_edge.setter
        def data_on_Bclk_rising_edge(self, on_rising_edge = False):
            self._parent._write_element_by_name('OBP', bool(on_rising_edge))


        @property
        def is_master(self):
            return self._parent._read_element_by_name('M_S').value


        @is_master.setter
        def is_master(self, value = False):
            self._parent._write_element_by_name('M_S', bool(value))


        def set_Bclk_frequency_divider(self, divider = 16):
            valids = self.BCLK_FREQUENCY_DIVIDER.keys()
            assert divider in valids, 'valid divider:{}'.format(valids)

            self._parent._write_element_by_name('OBF', self.BCLK_FREQUENCY_DIVIDER[divider])


        def set_LRclk_frequency_divider(self, divider = 1024):
            valids = self.LRCLK_FREQUENCY_DIVIDER.keys()
            assert divider in valids, 'valid divider:{}'.format(valids)

            self._parent._write_element_by_name('OLF', self.LRCLK_FREQUENCY_DIVIDER[divider])


        def enable_TDM(self, value = True):
            assert not (self.is_master and self._parent.control.sampling_rate_is_192KHz), \
                'Only slave mode is supported with 192KHz sampling rate.'

            self._parent._write_element_by_name('TDM', bool(value))


        def set_MSB_position(self, delay = 1):
            valids = self.MSB_POSITION_DELAY.keys()
            assert delay in valids, 'valid delay:{}'.format(valids)

            self._parent._write_element_by_name('MSB', self.MSB_POSITION_DELAY[delay])


        def set_output_word_length(self, bits = 24):
            valids = self.WORD_LENGTH_BITS.keys()
            assert bits in valids, 'valid bits:{}'.format(valids)

            self._parent._write_element_by_name('OWL', self.WORD_LENGTH_BITS[bits])


        def set_frame_sync_type(self, bit_wide_pulse_mode = False):
            self._parent._write_element_by_name('FST', bool(bit_wide_pulse_mode))


        def enable(self, value = True):
            self._parent.gpio.enable_serial_output(value)


    class _InterfaceRegisters(_RAM):

        ADDRESS_MIN = 0x0800
        ADDRESS_MAX = 0x0807
        N_BITS = 32
        ADDR_INCREMENT = N_BITS // 8
        N_REGISTERS = (ADDRESS_MAX - ADDRESS_MIN + 1)
        N_BYTES = N_REGISTERS * ADDR_INCREMENT
        REGISTER_NAME_PREFIX = 'Interface Register'


        def __getitem__(self, i):
            return self._parent.map.registers[f'{self.REGISTER_NAME_PREFIX} {i}']


        @property
        def control_port_write_mode(self):
            return self._parent._read_element_by_name('IFCW').value == 1


        @control_port_write_mode.setter
        def control_port_write_mode(self, value = True):
            self._parent._write_element_by_name('IFCW', 1 if value else 0)


        def write_to_eeprom(self):
            self._parent.eeprom.write(bytes_array = self.bytes,
                                      address = self._parent.eeprom.INTERFACE_REGISTERS_ADDRESS_MIN)


        def read_from_eeprom(self):
            assert self.control_port_write_mode, 'Control_port_write_mode not enabled.'

            self.write(bytes_array = self._parent.eeprom.read(n_bytes = self.N_BYTES,
                                                              address = self._parent.eeprom.INTERFACE_REGISTERS_ADDRESS_MIN))
            for i in range(self.N_REGISTERS):
                self._parent._read_register(self[i])


    class _AuxADC(ADAU._Base):

        AUXILIARY_ADC_FILTERING = {'4-bit hysteresis (12-bit level)': 0,
                                   '5-bit hysteresis (12-bit level)': 1,
                                   'Filter and hysteresis bypassed' : 2,
                                   'Low-pass filter bypassed'       : 3}


        def set_filtering(self, filter_type = '4-bit hysteresis (12-bit level)'):
            valids = self.AUXILIARY_ADC_FILTERING.keys()
            assert filter_type in valids, 'valid filter:{}'.format(valids)

            self._parent._write_element_by_name('FIL', self.AUXILIARY_ADC_FILTERING[filter_type])


        def data_registers_control_port_write_mode(self, value = True):
            self._parent._write_element_by_name('AACW', 1 if value else 0)


        def enable(self, value = True):
            self._parent._write_element_by_name('AAEN', 1 if value else 0)


    class _AuxiliaryAdcDataRegisters(_InterfaceRegisters):

        ADDRESS_MIN = 0x0809
        ADDRESS_MAX = 0x080C
        N_BITS = 16
        ADDR_INCREMENT = N_BITS // 8
        N_REGISTERS = (ADDRESS_MAX - ADDRESS_MIN + 1)
        N_BYTES = N_REGISTERS * ADDR_INCREMENT
        REGISTER_NAME_PREFIX = 'Auxiliary ADC Data'


    class _ProgramRAM(_RAM):
        NAME = 'Program Data'
        ADDRESS_MIN = 0x0400
        ADDRESS_MAX = 0x07FF
        N_BITS = 40
        ADDR_INCREMENT = N_BITS // 8
        N_BYTES = (ADDRESS_MAX - ADDRESS_MIN + 1) * ADDR_INCREMENT


    class _ReferenceClock(ADAU._Base):

        def power_down_oscillator(self, value = True):
            self._parent._write_element_by_name('OPD', 1 if value else 0)


    class _PLL(ADAU._Base):
        MCLK_INPUT_DIVIDER_BASE = {0: 64, 2: 256, 1: 384, 3: 512}


        def __init__(self, parent, mode = 2):
            super().__init__(parent)
            self.mode = mode


        @property
        def mclk_input_divider(self):
            return self.MCLK_INPUT_DIVIDER_BASE[self.mode] // self._parent.control.sampling_ratio


    class _DataCapturer(ADAU._Base):
        DATA_SOURCE = {'Multiplier X input (Mult_X_input)'      : 0,
                       'Multiplier Y input (Mult_Y_input) '     : 1,
                       'Multiplier-accumulator output (MAC_out)': 2,
                       'Accumulator feedback (Accum_fback)'     : 3}
        NUMERIC_FORMAT = (5, 19)
        N_BYTES = ceil(sum(NUMERIC_FORMAT) / 8)
        INDICES = {0x081A: 0, 0x081B: 1}


        def set_data_capture(self, register_idx = 0, step_count = 0, source = 'Multiplier X input (Mult_X_input'):
            valids = self.DATA_SOURCE.keys()
            assert source in valids, 'valid source:{}'.format(valids)

            reg = self._parent.map.registers[f'Data Capture {register_idx}']
            reg.elements['PC'].value = step_count
            reg.elements['RS'].value = self.DATA_SOURCE[source]
            self._parent._write_register(reg)


        def readback(self, address):
            return self.read_reg(self.INDICES[address])


        def read_reg(self, register_idx = 0):
            reg = self._parent.map.registers[f'Data Capture {register_idx}']
            return self._parent.DspNumber.from_bytes(self._parent.read_addressed_bytes(sub_address = reg.address,
                                                                                       n_bytes = self.N_BYTES),
                                                     n_bits_A = self.NUMERIC_FORMAT[0],
                                                     n_bits_B = self.NUMERIC_FORMAT[1])


    class _GPIO(ADAU._Base):
        PIN_FUNCTIONS = {'Auxiliary ADC input'             : 15,
                         'Serial data port'                : 4,
                         'Serial data port—inverted'       : 12,
                         'GPIO input, no debounce'         : 1,
                         'GPIO input, no debounce—inverted': 9,
                         'GPIO input, debounced'           : 0,
                         'GPIO input, debounced—inverted'  : 8,
                         'GPIO output'                     : 2,
                         'GPIO output—inverted'            : 10,
                         'Open-collector output'           : 3,
                         'Open-collector output—inverted'  : 11}
        PIN_FUNCTIONS_value_key = {v: k for k, v in PIN_FUNCTIONS.items()}

        GPIO_DEBOUNCE_TIME_ms = {20: 0, 40: 1, 10: 2, 5: 3}
        AuxADC_PIN_MAPPING = {0: 9, 1: 2, 2: 3, 3: 8}
        SERIAL_INPUT_PINs = list(range(6))
        SERIAL_OUTPUT_PINs = list(range(6, 12))
        N_PINS = 12
        PIN_INDICES = list(range(N_PINS))


        @property
        def pin_setting_register_control_port_write_mode(self):
            return bool(self._parent._read_element_by_name('GPCW').value)


        @pin_setting_register_control_port_write_mode.setter
        def pin_setting_register_control_port_write_mode(self, value = True):
            self._parent._write_element_by_name('GPCW', 1 if value else 0)


        def set_mode(self, idx, mode = 'GPIO input, debounced'):
            valids = self.PIN_FUNCTIONS.keys()
            assert mode in valids, 'valid mode:{}'.format(valids)

            self._parent._write_element_by_name(f'MP_{idx}', self.PIN_FUNCTIONS[mode])


        def get_mode(self, idx):
            assert idx in self.PIN_INDICES, 'valid idx:{}'.format(self.PIN_INDICES)

            return self.PIN_FUNCTIONS_value_key[self._parent._read_element_by_name(f'MP_{idx}').value]


        def get_pin_level(self, idx):
            return (self._parent._read_element_by_name('MP').value >> idx) & 0x01


        def set_pin_level(self, idx, level = 0):
            if not self._parent.is_virtual_device:
                assert self.pin_setting_register_control_port_write_mode, 'Can write Pin_Setting register.'
                assert 'output' in self.get_mode(idx), 'Not an output pin.'

            current_value = self._parent._read_element_by_name('MP').value
            value = current_value & (0xFFFF - (1 << idx)) | (level << idx)
            self._parent._write_element_by_name('MP', value)


        def sets_debounce_time(self, delay_ms = 20):
            valids = self.GPIO_DEBOUNCE_TIME_ms.keys()
            assert delay_ms in valids, 'valid delay_ms:{}'.format(valids)

            self._parent._write_element_by_name('GD', self.GPIO_DEBOUNCE_TIME_ms[delay_ms])


        def enable_AuxADC(self, idx = (0, 1, 2, 3)):
            for i in idx:
                self.set_mode(self.AuxADC_PIN_MAPPING[i], mode = 'Auxiliary ADC input')


        def enable_serial_input(self, value = True):
            for i in self.SERIAL_INPUT_PINs:
                self.set_mode(i, mode = 'Serial data port' if value else 'GPIO input, debounced')


        def enable_serial_output(self, value = True):
            for i in self.SERIAL_OUTPUT_PINs:
                self.set_mode(i, mode = 'Serial data port' if value else 'GPIO input, debounced')


    def __init__(self, bus, i2c_address = ADAU.I2C_ADDRESS,
                 pin_reset = None,
                 pin_self_boot = None,
                 pin_write_back = None,
                 pin_write_protect = None,
                 registers_map = None, registers_values = None,
                 sample_rate = None):

        registers_map = RegistersMap(name = 'ADAU1401',
                                     description = 'ADAU1401 registers.',
                                     registers = _get_all_registers()) \
            if registers_map is None else registers_map

        self._pin_reset = pin_reset
        self._pin_self_boot = pin_self_boot
        self._pin_write_back = pin_write_back
        self._write_back_on_falling_edge = False
        self._pin_write_protect = pin_write_protect

        super().__init__(bus = bus, i2c_address = i2c_address, sample_rate = sample_rate,
                         registers_map = registers_map, registers_values = registers_values)


    def _build(self):
        super()._build()

        # ====================================
        self.adc = self._ADC(self)
        self.dac = self._DAC(self)

        self.serial_input = self._SerialInput(self)
        self.serial_output = self._SerialOutput(self)

        self.interface_registers = self._InterfaceRegisters(self)
        self.aux_adc = self._AuxADC(self)
        self.auxiliary_adc_data_registers = self._AuxiliaryAdcDataRegisters(self)

        self.program_ram = self._ProgramRAM(self)

        self.reference_clock = self._ReferenceClock(self)
        self.pll = self._PLL(self)

        self.data_capturer = self._DataCapturer(self)

        self.gpio = self._GPIO(self)


    def init(self):
        self._action = 'init'
        self.map.reset()

        self._build()
        self.control.power_up()
        self.start()


    def mute(self, value = True):
        self.control.mute(value)


    def enable_output(self, value = True):
        self._action = 'enable_output: {}'.format(value)
        self.mute(not value)


    # external control pins =================================

    def reset(self):
        self.init()


    def _assert_reset(self):
        if self._pin_reset is not None:
            for level in (1, 0, 1):
                self._pin_reset.value(level)
                time.sleep(0.001)


    # encapsulated hardware functions =======================

    def readback(self, *args, **kwargs):
        return self.data_capturer.readback(*args, **kwargs)


    # hardware related IO========= ======================================

    # register related ============================================
    def _read_register(self, register):
        value = self.read_addressed_bytes(sub_address = register.address, n_bytes = register.n_bytes)
        register.load_value(int.from_bytes(value, byteorder = 'big'))
        self._show_bus_data(register.bytes, address = register.address, reading = True)
        self._print_register(register)
        return register.value


    def _write_register(self, register, reset = False):
        if register.address not in self.READ_ONLY_REGISTERS:
            super()._write_register(register, reset = reset)
            return self.write_addressed_bytes(sub_address = register.address, bytes_array = register.bytes)


    # by element's name ===========================================

    def _duplicated_element_names_guard(self, element_name):
        assert element_name not in self.map.duplicated_element_names, \
            f"More than one elements have the same name {element_name} ."


    def _read_element_by_name(self, element_name):
        self._duplicated_element_names_guard(element_name)
        return super()._read_element_by_name(element_name)


    def _write_element_by_name(self, element_name, value):
        self._duplicated_element_names_guard(element_name)
        return super()._write_element_by_name(element_name, value)



class ADAU1702(ADAU1701):
    class _ProgramRAM(ADAU1701._ProgramRAM):
        ADDRESS_MIN = 0x0400
        ADDRESS_MAX = 0x05FF
        N_BITS = 40
        ADDR_INCREMENT = N_BITS // 8
        N_BYTES = (ADDRESS_MAX - ADDRESS_MIN + 1) * ADDR_INCREMENT



class ADAU1401(ADAU1701):
    pass



class ADAU1401A(ADAU1401):
    pass
