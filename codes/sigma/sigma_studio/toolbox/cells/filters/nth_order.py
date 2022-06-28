try:
    from ..cell import Cell

except:
    from cell import Cell



class NthOrderFilter(Cell):

    def get_coefficients(self, **kwargs):
        return self.get_parameters_values(**kwargs)


    def set_coefficients(self, label_value_pairs, **kwargs):
        self.set_parameters_values(label_value_pairs, **kwargs)


    def set_coefficients_values(self, values, algorithm_idx = 0):
        addresses = tuple(p.address for p in self._module._algorithms[algorithm_idx].parameters.values())
        assert len(values) <= max(addresses) - min(addresses) + 1

        bytes_array = b''.join([self._dsp.DspNumber(v).bytes for v in values])
        self._dsp.parameter_ram.write(bytes_array = bytes_array, address = min(addresses))


    def reset_coefficients(self, algorithm_idx = 0):
        addresses = tuple(p.address for p in self._module._algorithms[algorithm_idx].parameters.values())
        values = [1.0, 0.0, 0.0, 0.0, 0.0] * (len(addresses) // 5)
        self.set_coefficients_values(values, algorithm_idx = algorithm_idx)



class NthOrderDouble(NthOrderFilter):
    pass
