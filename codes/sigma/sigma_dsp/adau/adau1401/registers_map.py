try:
    from utilities.register import Register, Element

except:
    from register import Register, Element



def _get_all_registers():
    registers = []

    registers.append(
        Register(name = 'Interface Register 0', address = 0x0800,
                 description = '''Interface Register 0''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 28, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'IF', idx_lowest_bit = 0, n_bits = 28, value = 0,
                                     description = '''Interface register 28-bit parameter'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Interface Register 1', address = 0x0801,
                 description = '''Interface Register 1''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 28, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'IF', idx_lowest_bit = 0, n_bits = 28, value = 0,
                                     description = '''Interface register 28-bit parameter'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Interface Register 2', address = 0x0802,
                 description = '''Interface Register 2''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 28, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'IF', idx_lowest_bit = 0, n_bits = 28, value = 0,
                                     description = '''Interface register 28-bit parameter'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Interface Register 3', address = 0x0803,
                 description = '''Interface Register 3''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 28, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'IF', idx_lowest_bit = 0, n_bits = 28, value = 0,
                                     description = '''Interface register 28-bit parameter'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Interface Register 4', address = 0x0804,
                 description = '''Interface Register 4''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 28, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'IF', idx_lowest_bit = 0, n_bits = 28, value = 0,
                                     description = '''Interface register 28-bit parameter'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Interface Register 5', address = 0x0805,
                 description = '''Interface Register 5''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 28, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'IF', idx_lowest_bit = 0, n_bits = 28, value = 0,
                                     description = '''Interface register 28-bit parameter'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Interface Register 6', address = 0x0806,
                 description = '''Interface Register 6''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 28, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'IF', idx_lowest_bit = 0, n_bits = 28, value = 0,
                                     description = '''Interface register 28-bit parameter'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Interface Register 7', address = 0x0807,
                 description = '''Interface Register 7''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 28, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'IF', idx_lowest_bit = 0, n_bits = 28, value = 0,
                                     description = '''Interface register 28-bit parameter'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'GPIO Pin Setting', address = 0x0808,
                 description = '''GPIO Pin Setting''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'MP', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Setting of multipurpose pin when controlled through SPI or I2C'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Auxiliary ADC Data 0', address = 0x0809,
                 description = '''Auxiliary ADC Data 0''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'AA', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Auxiliary ADC output data, MSB first'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Auxiliary ADC Data 1', address = 0x080A,
                 description = '''Auxiliary ADC Data 1''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'AA', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Auxiliary ADC output data, MSB first'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Auxiliary ADC Data 2', address = 0x080B,
                 description = '''Auxiliary ADC Data 2''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'AA', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Auxiliary ADC output data, MSB first'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Auxiliary ADC Data 3', address = 0x080C,
                 description = '''Auxiliary ADC Data 3''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'AA', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Auxiliary ADC output data, MSB first'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Registers 0', address = 0x0810,
                 description = '''Safeload Registers 0''',
                 elements = [Element(name = 'SD', idx_lowest_bit = 0, n_bits = 40, value = 0,
                                     description = '''Safeload Data. Data (program, parameters, register contents) to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Registers 1', address = 0x0811,
                 description = '''Safeload Registers 1''',
                 elements = [Element(name = 'SD', idx_lowest_bit = 0, n_bits = 40, value = 0,
                                     description = '''Safeload Data. Data (program, parameters, register contents) to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Registers 2', address = 0x0812,
                 description = '''Safeload Registers 2''',
                 elements = [Element(name = 'SD', idx_lowest_bit = 0, n_bits = 40, value = 0,
                                     description = '''Safeload Data. Data (program, parameters, register contents) to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Registers 3', address = 0x0813,
                 description = '''Safeload Registers 3''',
                 elements = [Element(name = 'SD', idx_lowest_bit = 0, n_bits = 40, value = 0,
                                     description = '''Safeload Data. Data (program, parameters, register contents) to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Registers 4', address = 0x0814,
                 description = '''Safeload Registers 4''',
                 elements = [Element(name = 'SD', idx_lowest_bit = 0, n_bits = 40, value = 0,
                                     description = '''Safeload Data. Data (program, parameters, register contents) to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Address 0', address = 0x0815,
                 description = '''Safeload Address 0''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'SA', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Safeload Address. Address of data that is to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Address 1', address = 0x0816,
                 description = '''Safeload Address 1''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'SA', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Safeload Address. Address of data that is to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Address 2', address = 0x0817,
                 description = '''Safeload Address 2''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'SA', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Safeload Address. Address of data that is to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Address 3', address = 0x0818,
                 description = '''Safeload Address 3''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'SA', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Safeload Address. Address of data that is to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Safeload Address 4', address = 0x0819,
                 description = '''Safeload Address 4''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'SA', idx_lowest_bit = 0, n_bits = 12, value = 0,
                                     description = '''Safeload Address. Address of data that is to be loaded into the RAMs or registers.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Data Capture 0', address = 0x081A,
                 description = '''Data Capture 0''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'PC', idx_lowest_bit = 2, n_bits = 10, value = 0,
                                     description = '''10-bit program counter address'''),
                             Element(name = 'RS', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                     description = '''Select the register to be transferred to the data capture output'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Data Capture 1', address = 0x081B,
                 description = '''Data Capture 1''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'PC', idx_lowest_bit = 2, n_bits = 10, value = 0,
                                     description = '''10-bit program counter address'''),
                             Element(name = 'RS', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                     description = '''Select the register to be transferred to the data capture output'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'DSP Core Control', address = 0x081C,
                 description = '''DSP Core Control''',
                 elements = [Element(name = 'RSVD_1', idx_lowest_bit = 14, n_bits = 2, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'GD', idx_lowest_bit = 12, n_bits = 2, value = 0,
                                     description = '''GPIO Debounce Control. Sets debounce time of multipurpose pins that are set as GPIO inputs.'''),
                             Element(name = 'RSVD_0', idx_lowest_bit = 9, n_bits = 3, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'AACW', idx_lowest_bit = 8, n_bits = 1, value = 0,
                                     description = '''Auxiliary ADC Data Registers Control Port Write Mode. Setting this bit allows data to be written directly to the auxiliary ADC data registers (2057 to 2060) from the control port. When this bit is set, the auxiliary ADC data registers ignore the settings on the multipurpose pins.'''),
                             Element(name = 'GPCW', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                     description = '''GPIO Pin Setting Register Control Port Write Mode. When this bit is set, the GPIO pin setting register (2056) can be written to directly from the control port and this register ignores the input settings on the multipurpose pins.'''),
                             Element(name = 'IFCW', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                     description = '''Interface Registers Control Port Write Mode. When this bit is set, data can be written directly to the interface registers (2048 to 2055) from the control port. In that state, the interface registers are not written from the SigmaDSP program.'''),
                             Element(name = 'IST', idx_lowest_bit = 5, n_bits = 1, value = 0,
                                     description = '''Initiate Safeload Transfer. Setting this bit to 1 initiates a safeload transfer to the parameter RAM. This bit is automatically cleared when the operation is complete. There are five safeload register pairs (address/data); only those registers that have been written since the last safeload event are transferred to the parameter RAM.'''),
                             Element(name = 'ADM', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                     description = '''Mute ADCs. This bit mutes the output of the ADCs. The bit defaults to 0 and is active low; therefore, it must be set to 1 to transmit audio signals from the ADCs.'''),
                             Element(name = 'DAM', idx_lowest_bit = 3, n_bits = 1, value = 0,
                                     description = '''Mute DACs. This bit mutes the output of the DACs. The bit defaults to 0 and is active low; therefore, it must be set to 1 to transmit audio signals from the DACs.'''),
                             Element(name = 'CR', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                     description = '''Clear Internal Registers to 0. This bit defaults to 0 and is active low. It must be set to 1 for a signal to pass through the SigmaDSP core.'''),
                             Element(name = 'SR', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                     description = '''Sample Rate. These bits set the number of DSP instructions for every sample and the sample rate at which the ADAU1401 operates. At the default setting of 1กั, there are 1024 instructions per audio sample. This setting should be used with sample rates such as 48 kHz and 44.1 kHz.
At the 2กั setting, the number of instructions per frame is halved to 512 and the ADCs and DACs nominally run at a 96 kHz sample rate. 
At the 4กั setting, there are 256 instructions per cycle and the converters run at a 192 kHz sample rate.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Serial Output Control', address = 0x081E,
                 description = '''Serial Output Control''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 14, n_bits = 2, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'OLRP', idx_lowest_bit = 13, n_bits = 1, value = 0,
                                     description = '''OUTPUT_LRCLK Polarity. When this bit is set to 0, the left-channel data is clocked when OUTPUT_LRCLK is low and the right-channel data is clocked when OUTPUT_LRCLK is high. When this bit is set to 1, the right- channel data is clocked when OUTPUT_LRCLK is low and the left-channel data is clocked when OUTPUT_LRCLK is high.'''),
                             Element(name = 'OBP', idx_lowest_bit = 12, n_bits = 1, value = 0,
                                     description = '''OUTPUT_BCLK Polarity. This bit controls on which edge of the bit clock the output data is clocked. Data changes on the falling edge of OUTPUT_BCLK when this bit is set to 0 and on the rising edge when this bit is set to 1.'''),
                             Element(name = 'M_S', idx_lowest_bit = 11, n_bits = 1, value = 0,
                                     description = '''Master/Slave. This bit sets whether the output port is a clock master or slave. The default setting is slave; on power-up, the OUTPUT_BCLK and OUTPUT_LRCLK pins are set as inputs until this bit is set to 1, at which time they become clock outputs.'''),
                             Element(name = 'OBF', idx_lowest_bit = 9, n_bits = 2, value = 0,
                                     description = '''OUTPUT_BCLK Frequency (Master Mode Only). When the output port is being used as a clock master, these bits set the frequency of the output bit clock, which is divided down from an internal 1024 กั fS clock (49.152 MHz for a fS of 48 kHz).'''),
                             Element(name = 'OLF', idx_lowest_bit = 7, n_bits = 2, value = 0,
                                     description = '''OUTPUT_LRCLK Frequency (Master Mode Only). When the output port is used as a clock master, these bits set the frequency of the output word clock on the OUTPUT_LRCLK pins, which is divided down from an internal 1024 กั fS clock (49.152 MHz for a fS of 48 kHz).'''),
                             Element(name = 'FST', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                     description = '''Frame Sync Type. This bit sets the type of signal on the OUTPUT_LRCLK pins. When this bit is set to 0, the signal is a word clock with a 50% duty cycle; when this bit is set to 1, the signal is a pulse with a duration of one bit clock at the beginning of the data frame.'''),
                             Element(name = 'TDM', idx_lowest_bit = 5, n_bits = 1, value = 0,
                                     description = '''TDM Enable. Setting this bit to 1 changes the output port from four serial stereo outputs to a single 8- channel TDM output stream on the SDATA_OUT0 pin (MP6).'''),
                             Element(name = 'MSB', idx_lowest_bit = 3, n_bits = 2, value = 0,
                                     description = '''MSB Position. These three bits set the position of the MSB of data with respect to the LRCLK edge. The data output of the ADAU1401 is always MSB first.'''),
                             Element(name = 'OWL', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                     description = '''Output Word Length. These bits set the word length of the output data-word. All bits following the LSB are set to 0.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Serial Input Control', address = 0x081F,
                 description = '''Serial Input Control''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 5, n_bits = 3, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'ILP', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                     description = '''INPUT_LRCLK Polarity. When this bit is set to 0, the left-channel data on the SDATA_INx pins is clocked when INPUT_LRCLK is low and the right-channel data is clocked when INPUT_LRCLK is high. When this bit is set to 1, the clocking of these channels is reversed. In TDM mode when this bit is set to 0, data is clocked in, starting with the next appropriate BCLK edge (set in Bit 3 of this register) after a falling edge on the INPUT_LRCLK pin. When this bit is set to 1 and the device is running in TDM mode, the input data is valid on the BCLK edge after a rising edge on the word clock (INPUT_LRCLK). INPUT_LRCLK can also operate with a pulse input, rather than a clock. In this case, the first edge of the pulse is used by the ADAU1401 to start the data frame. When this polarity bit is set to 0, a low pulse should be used; when the bit it set to 1, a high pulse should be used.'''),
                             Element(name = 'IBP', idx_lowest_bit = 3, n_bits = 1, value = 0,
                                     description = '''INPUT_BCLK Polarity. This bit controls on which edge of the bit clock the input data changes and on which edge it is clocked. Data changes on the falling edge of INPUT_BCLK when this bit is set to 0 and on the rising edge when this bit is set at 1.'''),
                             Element(name = 'M', idx_lowest_bit = 0, n_bits = 3, value = 0,
                                     description = '''Serial Input Mode. These two bits control the data format that the input port expects to receive. Bit 3 and Bit 4 of this control register override the settings of Bits[2:0]; therefore, all four bits must be changed together for 
proper operation in some modes. The clock diagrams for these modes are shown in Figure 32, Figure 33, and Figure 34. Note that for left-justified and right-justified modes, the LRCLK polarity is high and then low, which is 
the opposite of the default setting for ILP. 
When these bits are set to accept a TDM input, the ADAU1401 data starts after the edge defined by ILP. The ADAU1401 TDM data stream should be input on Pin SDATA_IN0. Figure 35 shows a TDM stream with a high-to- 
low triggered LRCLK and data changing on the falling edge of the BCLK. The ADAU1401 expects the MSB of each data slot to be delayed by one BCLK from the beginning of the slot, as it would in stereo I2S format. In TDM 
mode, Channel 0 to Channel 3 are in the first half of the frame, and Channel 4 to Channel 7 are in the second half. Figure 36 shows an example of a TDM stream running with a pulse word clock, which is used to interface to 
ADI codecs in auxiliary mode. To work in this mode with either the input or output serial ports, set the ADAU1401 to begin the frame on the rising edge of LRCLK, to change data on the falling edge of BCLK, and to 
delay the MSB position from the start of the word clock by one BCLK.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Multipurpose Pin Configuration 0', address = 0x0820,
                 description = '''Multipurpose Pin Configuration 0''',
                 elements = [Element(name = 'MP_0', idx_lowest_bit = 0, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_1', idx_lowest_bit = 4, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_2', idx_lowest_bit = 8, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_3', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_4', idx_lowest_bit = 16, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_5', idx_lowest_bit = 20, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Multipurpose Pin Configuration 1', address = 0x0821,
                 description = '''Multipurpose Pin Configuration 1''',
                 elements = [Element(name = 'MP_6', idx_lowest_bit = 0, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_7', idx_lowest_bit = 4, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_8', idx_lowest_bit = 8, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_9', idx_lowest_bit = 12, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_10', idx_lowest_bit = 16, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             Element(name = 'MP_11', idx_lowest_bit = 20, n_bits = 4, value = 0,
                                     description = '''Set the function of each multipurpose pin.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Auxiliary ADC and Power Control', address = 0x0822,
                 description = '''Auxiliary ADC and Power Control''',
                 elements = [Element(name = 'RSVD_1', idx_lowest_bit = 10, n_bits = 6, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'FIL', idx_lowest_bit = 8, n_bits = 2, value = 0,
                                     description = '''Auxiliary ADC filtering'''),
                             Element(name = 'AAPD', idx_lowest_bit = 7, n_bits = 1, value = 0,
                                     description = '''ADC power-down (both ADCs)'''),
                             Element(name = 'VBPD', idx_lowest_bit = 6, n_bits = 1, value = 0,
                                     description = '''Voltage reference buffer power-down'''),
                             Element(name = 'VRPD', idx_lowest_bit = 5, n_bits = 1, value = 0,
                                     description = '''Voltage reference power-down'''),
                             Element(name = 'RSVD_0', idx_lowest_bit = 4, n_bits = 1, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'D0PD', idx_lowest_bit = 3, n_bits = 1, value = 0,
                                     description = '''DAC0 power-down'''),
                             Element(name = 'D1PD', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                     description = '''DAC1 power-down'''),
                             Element(name = 'D2PD', idx_lowest_bit = 1, n_bits = 1, value = 0,
                                     description = '''DAC2 power-down'''),
                             Element(name = 'D3PD', idx_lowest_bit = 0, n_bits = 1, value = 0,
                                     description = '''DAC3 power-down'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Auxiliary ADC Enable', address = 0x0824,
                 description = '''Auxiliary ADC Enable''',
                 elements = [Element(name = 'AAEN', idx_lowest_bit = 15, n_bits = 1, value = 0,
                                     description = '''Enable the auxiliary ADC'''),
                             Element(name = 'RSVD', idx_lowest_bit = 0, n_bits = 15, value = 0,
                                     description = '''Reserved.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'Oscillator Power Down', address = 0x0826,
                 description = '''Oscillator Power Down''',
                 elements = [Element(name = 'RSVD_1', idx_lowest_bit = 3, n_bits = 13, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'OPD', idx_lowest_bit = 2, n_bits = 1, value = 0,
                                     description = '''Oscillator Power Down. Power down the oscillator.'''),
                             Element(name = 'RSVD_0', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                     description = '''Reserved.'''),
                             ], default_value = 0))

    registers.append(
        Register(name = 'DAC Setup', address = 0x0827,
                 description = '''DAC Setup''',
                 elements = [Element(name = 'RSVD', idx_lowest_bit = 2, n_bits = 14, value = 0,
                                     description = '''Reserved.'''),
                             Element(name = 'DS', idx_lowest_bit = 0, n_bits = 2, value = 0,
                                     description = '''DAC Setup.'''),
                             ], default_value = 0))

    return registers
