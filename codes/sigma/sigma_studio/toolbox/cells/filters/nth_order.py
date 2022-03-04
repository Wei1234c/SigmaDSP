try:
    from ..cell import Cell

except:
    from cell import Cell



class NthOrderFilter(Cell):

    def get_coefficients(self, **kwargs):
        return self.get_parameters_values(**kwargs)


    def set_coefficients(self, label_value_pairs, **kwargs):
        self.set_parameters_values(label_value_pairs, **kwargs)



class NthOrderDouble(NthOrderFilter):
    pass
