try:
    from ..cell import LookUpTable

except:
    from cell import LookUpTable



class FIR(LookUpTable):
    # https://wiki.analog.com/resources/tools-software/sigmastudio/toolbox/filters/firfilter

    TABLE_PARAM = 'fircoeff_0'


    def get_coefficients(self, **kwargs):
        return self.get_table(**kwargs).numbers


    def set_coefficients(self, coefficients, **kwargs):
        self.set_table(coefficients, **kwargs)



class FIRFiltAlg(FIR):
    pass
