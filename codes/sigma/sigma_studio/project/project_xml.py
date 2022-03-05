import json


try:
    from ...sigma_dsp.dsp_processor import DspNumber
    from ...mini_xml.etree import ElementTree as ET
    # from xml.etree import ElementTree as ET

except:
    from dsp_processor import DspNumber
    import ElementTree as ET



def find(element, tag):
    for child in element:
        if child.tag == tag:
            return child



def findall(element, tag):
    matches = []

    for child in element:
        if child.tag == tag:
            matches.append(child)
        if len(child) > 0:
            matches.extend(findall(child, tag))

    return matches



def get_ICs(file_name, cls_numeric = None):
    cls_numeric = DspNumber if cls_numeric is None else cls_numeric

    with open(file_name, 'rt', encoding = 'utf8') as f:
        root = ET.parse(f).getroot()

    return tuple(IC(ic, cls_numeric = cls_numeric) for ic in findall(root, 'IC'))



class _Element:
    ATTRIBUTES = ['Name']


    def __init__(self, element, parent):
        self._ele = element
        self.parent = parent

        name = self._get_text('Name')
        self.name = name if name is not None else 'unknown'

        if 'Address' in self.ATTRIBUTES:
            self.address = int(self._get_text('Address'))


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()


    def __del__(self):
        self._ele = None
        self.parent = None


    @property
    def parameters(self):
        if hasattr(self, '_parameters'):
            return {p.name: p for p in self._parameters}


    def find(self, tag):
        return find(self._ele, tag)


    def findall(self, tag):
        return findall(self._ele, tag)


    # ===========================================

    def _get_text(self, tag):
        ele = self.find(tag)
        if ele is not None:
            return ele.text


    @staticmethod
    def _bytearray_string_to_bytes(bytearray_string):
        return bytes([int(b, 16) for b in bytearray_string.replace(' ', '').split(',') if b.startswith('0x')])


    @staticmethod
    def _bytes_to_bytearray_string(data_bytes):
        return ', '.join([f'0x{b:02X}' for b in data_bytes])



class Parameter(_Element):
    ATTRIBUTES = ['Name', 'Type', 'Address', 'Value', 'Size', 'Data']


    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.short_name = self.name.replace(self.parent.name, '')
        self._number = None
        self._bytes = None

        self._cls_numeric = self.parent.parent.parent._cls_numeric
        self._load_data()


    def __del__(self):
        super().__del__()
        self._cls_numeric = None


    def _load_data(self):

        value = self._get_text('Value')
        data_bytes = self._bytearray_string_to_bytes(self._get_text('Data'))

        if value is not None:  # is a number.
            value = float(value)
            value_from_bytes = self._cls_numeric.bytes_to_value(data_bytes, *self._cls_numeric.FLOAT_FORMAT)

            self._number = self._cls_numeric(int(value), *self._cls_numeric.INT_FORMAT) \
                if abs(value - value_from_bytes) > 1e-7 else \
                self._cls_numeric(float(value), *self._cls_numeric.FLOAT_FORMAT)

        else:  # not a number
            self._bytes = data_bytes


    @property
    def value(self):
        assert self._number is not None, 'Data bytes, not a number.'

        return self._number.value


    def set_value(self, data):

        if isinstance(data, bytes) or isinstance(data, bytearray):  # data is bytes
            if self.type is bytes:
                assert len(data) == self.size, 'Must be same size.'
                self._bytes = data
            else:
                value = self._number.bytes_to_value(data, self._number.n_bits_A, self._number.n_bits_B)
                self._number.set_value(value)

        else:  # data is a number
            self._number.set_value(data)

        return self


    @property
    def type(self):
        return self._number.type if self._number is not None else bytes


    def to_integer(self):
        assert self._number is not None, 'Data bytes, not a number.'
        self._number.to_integer()


    def to_float(self):
        assert self._number is not None, 'Data bytes, not a number.'
        self._number.to_float()


    @property
    def bytes(self):
        return self._number.bytes if self._number is not None else self._bytes


    @property
    def size(self):
        return len(self.bytes)


    @property
    def numbers(self):
        assert self.type is bytes

        data_bytes = self.bytes
        numbers = []

        for i in range(int(self.size / self._cls_numeric.N_BYTES)):
            numbers.append(self._cls_numeric.bytes_to_value(data_bytes[:self._cls_numeric.N_BYTES]))
            data_bytes = data_bytes[self._cls_numeric.N_BYTES:]

        return numbers


    def set_numbers(self, values):
        assert self.type is bytes
        assert len(values) == len(self.numbers)

        self.set_value(b''.join([self._cls_numeric(value).bytes for value in values]))


    def dumps(self):
        d = {'name'      : self.name,
             'short_name': self.short_name,
             'type'      : self.type.__name__,
             'value'     : self.value if self.type is not bytes else None,
             'address'   : self.address,
             'n_bytes'   : self.size}

        return json.dumps(d)



class Algorithm(_Element):
    ATTRIBUTES = ['AlgoName', 'DetailedName', 'Description']


    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.name = self._get_text('DetailedName')
        self.algorithm_name = self._get_algorithm_name(self.name)
        self.full_description = self._get_text('Description')
        self.description = self.full_description.split(':')[0].strip()

        self._parameters = list(Parameter(ele, self) for ele in self.findall('ModuleParameter'))
        self._parameters.extend((Parameter(ele, self) for ele in self.findall('Table')))


    @property
    def properties(self):

        def get_name_value(prop):
            pos1 = prop.find('[')
            pos2 = prop.find(']')
            name = prop[:pos1].strip()
            value = prop[pos1 + 1:pos2].strip().replace('$', ',')

            try:
                value = eval(value)
            except (SyntaxError, NameError) as e:
                pass

            return name, value


        segments = self.full_description.split(':')
        properties = []

        if len(segments) > 1:
            properties = segments[1].split(',')

        return {name: value for name, value in [get_name_value(prop) for prop in properties]}


    @property
    def parameters(self):
        if hasattr(self, '_parameters'):
            return {p.short_name: p for p in self._parameters}


    def dumps(self):
        d = {'name'          : self.name,
             'algorithm_name': self.algorithm_name,
             'description'   : self.description,
             'parameters'    : [json.loads(p.dumps()) for p in self._parameters]}

        return json.dumps(d)


    @property
    def df(self):
        import pandas as pd

        my_dict = json.loads(self.dumps())
        df = pd.DataFrame(my_dict['parameters'])

        df['algorithm_name'] = my_dict['algorithm_name']
        # df['algorithm_full_name'] = my_dict['name']
        df.rename(columns = {'name'      : 'param_full_name',
                             'short_name': 'param_name'}, inplace = True)
        df = df[['algorithm_name', 'param_name',
                 'param_full_name',
                 'type', 'value', 'address', 'n_bytes']]
        df.sort_values(by = ['algorithm_name', 'param_name'], inplace = True)
        df.index = range(len(df))

        return df


    @staticmethod
    def _get_algorithm_name(name):
        while True:
            if name[-1].isdigit():
                name = name[:-1]
            else:
                return name



class Module(_Element):
    ATTRIBUTES = ['CellName']


    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.name = self._get_text('CellName')
        self._algorithms = tuple(Algorithm(ele, self) for ele in self.findall('Algorithm'))
        self._parameters = tuple(parameter
                                 for algo in self._algorithms
                                 for parameter in algo._parameters)


    @property
    def algorithm_name(self):
        return self._algorithms[0].algorithm_name


    @property
    def description(self):
        return self._algorithms[0].description


    @property
    def properties(self):
        return self._algorithms[0].properties


    @property
    def algorithms(self):
        return {a.name: a for a in self._algorithms}


    @property
    def df(self):
        import pandas as pd

        df = pd.concat([a.df for a in self._algorithms])
        df['cell_name'] = self.name
        df = df[['cell_name', 'algorithm_name', 'param_name',
                 'param_full_name',
                 'type', 'value', 'address', 'n_bytes']]
        df.sort_values(by = ['cell_name', 'algorithm_name', 'param_name'], inplace = True)
        df.index = range(len(df))

        return df



class Register(_Element):
    ATTRIBUTES = ['Name', 'Address', 'AddrIncr', 'Size', 'Data']


    def __init__(self, element, parent):
        super().__init__(element, parent)

        self.address_increment = int(self._get_text('AddrIncr'))
        self._bytes = None
        self.bytes = self._bytearray_string_to_bytes(self._get_text('Data'))


    @property
    def bytes(self):
        return self.parent.parameter_bytes if self.name == 'Param' else self._bytes


    @bytes.setter
    def bytes(self, data_bytes):
        if self.name != 'Param':
            self._bytes = data_bytes


    @property
    def size(self):
        return len(self.bytes)



class Program(Register):
    pass



class IC(_Element):
    ATTRIBUTES = ['Name', 'PartNumber']


    def __init__(self, element, parent = None, cls_numeric = DspNumber):
        super().__init__(element, parent)

        self.part_number = self._get_text('PartNumber')
        self._cls_numeric = cls_numeric

        self._registers = tuple(Register(ele, self) for ele in self.findall('Register'))
        self._programs = tuple(Program(ele, self) for ele in self.findall('Program'))
        self._modules = tuple(Module(ele, self) for ele in self.findall('Module'))
        self._parameters = tuple(parameter
                                 for module in self._modules
                                 for parameter in module._parameters)


    def __del__(self):
        super().__del__()
        self._cls_numeric = None


    @property
    def registers(self):
        return {r.name: r for r in self._registers}


    @property
    def programs(self):
        return {p.name: p for p in self._programs}


    @property
    def modules(self):
        return {m.name: m for m in self._modules}


    @property
    def parameter_bytes(self):
        addr_max = max(p.address for p in self._parameters)
        ba = [bytes(self._cls_numeric.N_BYTES)] * (addr_max + 1)

        for p in self._parameters:
            ba[p.address] = p.bytes

        return b''.join(ba)


    @property
    def df(self):
        import pandas as pd

        df = pd.concat([m.df for m in self._modules])
        df.drop_duplicates(inplace = True)
        df = df[['cell_name', 'algorithm_name', 'param_name',
                 'param_full_name',
                 'type', 'value', 'address', 'n_bytes']]
        df['value'] = df.apply(lambda row: int(row['value']) if row['type'] == 'int' else row['value'], axis = 1)
        # df.sort_values(by = ['cell_name', 'algorithm_name', 'param_name'], inplace = True)
        # df.index = range(len(df))
        df.set_index(['algorithm_name', 'cell_name', 'param_name'], inplace = True)
        df.sort_index(inplace = True)

        return df
