from math import log2



class Cell:

    def __init__(self, module, dsp = None):  # module: project_xml.Module
        self._check_compatibility(module)

        self._module = module
        self._dsp = dsp

        self.PARAMETER_SHORT_NAMES = sorted(set(p.short_name for p in self.parameters.values()))


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()


    def __del__(self):
        self._dsp = None
        self._module = None
        self.PARAMETER_SHORT_NAMES = None


    # properties =========================
    @property
    def name(self):
        return self._module.name


    @property
    def algorithm_name(self):
        return self._module.algorithm_name


    @property
    def description(self):
        return self._module.description


    @property
    def properties(self):
        return self._module.properties


    @property
    def parameters(self):
        return self._module.parameters


    @property
    def df(self):

        try:
            return self._module.df.set_index(['cell_name', 'algorithm_name', 'param_name'])

        except AttributeError as e:
            print('Need Pandas.')


    def show_methods(self, print_out = True):
        import json
        from inspect import signature

        methods = []
        properties = []

        for attr in dir(self):
            if not attr.startswith('_'):
                if hasattr(getattr(self, attr), '__call__'):
                    methods.append(attr + str(signature(getattr(self, attr))))
                else:
                    properties.append(attr)

        json_str = json.dumps({'cell_name'     : self.name,
                               'algorithm_name': self.algorithm_name,
                               'methods'       : methods,
                               'properties'    : properties},
                              indent = 4, sort_keys = False)
        if print_out:
            print(json_str)
        else:
            return json_str


    # utilities functions - parameter-related ================

    def get_param(self, param_name = '', algorithm_idx = 0):
        assert param_name in self.PARAMETER_SHORT_NAMES, \
            f'{param_name} not in valid params: {self.PARAMETER_SHORT_NAMES}'

        param = self._module._algorithms[algorithm_idx].parameters[param_name]

        return self.read_parameter(param)


    def set_param(self, data, param_name = '', send_now = True, algorithm_idx = None):
        if algorithm_idx is None:
            indices = range(len(self._module._algorithms))
        else:
            indices = algorithm_idx if hasattr(algorithm_idx, '__iter__') else [algorithm_idx]

        for i in indices:
            self._set_a_param(data = data, param_name = param_name, send_now = send_now, algorithm_idx = i)


    def read_parameter(self, param):  # read from hardware
        if self._dsp is not None:  # added for Factory.show_methods()
            ba = self._dsp.read_parameter(param)
            if ba is not None:
                param.set_value(ba)

        return param


    def write_parameter(self, param, send_now = True):  # write to hardware
        self._dsp.write_parameter(param, send_now = send_now)


    def get_parameters_values(self, **kwargs):
        params = (self.get_param(param_name = p.short_name, **kwargs) for p in self.parameters.values())
        return sorted([p.short_name, p.value] for p in params if p._number is not None)


    def set_parameters_values(self, name_value_pairs, **kwargs):
        for short_name, value in name_value_pairs:
            self.set_param(value, param_name = short_name, **kwargs)


    # dsp chip related low level utilities ==================

    def _set_a_param(self, data, param_name = '', send_now = True, algorithm_idx = None):

        param = self.get_param(param_name, algorithm_idx)
        param.set_value(data)

        self.write_parameter(param, send_now = send_now)


    # error prevention utilities ==================

    def _check_compatibility(self, module):
        algorithm_name = module.algorithm_name

        assert algorithm_name == self.__class__.__name__, \
            f'Wrong Cell class "{self.__class__.__name__}" for algorithm "{algorithm_name}".'



class Slewer(Cell):
    SLEW_PARAM = None


    @property
    def slew_rate(self):
        return self._get_slew_rate_RC(self.get_param(self.SLEW_PARAM).value)


    def set_slew_rate(self, slew_rate, **kwargs):
        self.set_param(self._get_slew_RC(slew_rate), param_name = self.SLEW_PARAM, **kwargs)


    @staticmethod
    def _get_slew_RC(slew_rate, limit_min = 1, limit_max = 23):
        slew_rate = int(slew_rate)
        assert limit_min <= slew_rate <= limit_max, f'Needs {limit_min} <= slew_rate:{slew_rate} <= {limit_max}'

        return 1 / (2 ** slew_rate)


    @staticmethod
    def _get_slew_rate_RC(slew):
        if slew > 0:
            return int(log2(1 / slew))



class Switch(Cell):
    ENABLE_PARAM = None


    def enable(self, value = True, param_name = None, send_now = True, **kwargs):
        param_name = self.ENABLE_PARAM if param_name is None else param_name

        self.set_param(1.0 if value else 0.0, param_name = param_name, send_now = send_now, **kwargs)



class LookUpTable(Cell):
    TABLE_PARAM = None


    def get_table(self, **kwargs):
        return self.get_param(self.TABLE_PARAM, **kwargs)


    def set_table(self, values, **kwargs):
        table = self.get_table(**kwargs)
        table.set_numbers(values)
        self.write_parameter(table)
