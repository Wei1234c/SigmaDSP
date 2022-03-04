try:
    from ..cell import LookUpTable

except:
    from cell import LookUpTable



class LinearInterpolator(LookUpTable):
    # https://wiki.analog.com/resources/tools-software/sigmastudio/toolbox/basicdsp/linearinterpolator

    TABLE_PARAM = ''
    MIN_PARAM = 'Min'
    NUMBER_OF_POINTS_PARAM = 'Number'
    Q_PARAM = 'Q'


    def set_table(self, values, **kwargs):
        table = self.get_table(**kwargs)
        table.set_numbers(values)
        self.write_parameter(table)

        self.set_param(min(values), param_name = self.MIN_PARAM, **kwargs)
        self.set_param(max(values) - min(values), param_name = self.Q_PARAM, **kwargs)
        self.set_param(len(values) - 1, param_name = self.NUMBER_OF_POINTS_PARAM, **kwargs)



class LinearIntGrowableS100Alg(LinearInterpolator):
    pass
