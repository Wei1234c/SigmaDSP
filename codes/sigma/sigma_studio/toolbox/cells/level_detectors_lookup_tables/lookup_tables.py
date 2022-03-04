try:
    from .. import cell
    from ..dynamics_processors.dynamics_processors import DynamicsProcessor, RMS

except:
    import cell
    from dynamics_processors import DynamicsProcessor, RMS



class LookUpTable(cell.LookUpTable):
    pass



class LookupTable2DAlg(LookUpTable):
    TABLE_PARAM = 'table_p0'


    def set_max_xy(self, x_max, y_max, **kwargs):
        assert x_max * y_max == len(self.get_table().numbers)

        self.set_param(x_max, param_name = 'maxx', **kwargs)
        self.set_param(y_max, param_name = 'maxy', **kwargs)



class LookupTable2DAlgNoLimit(LookupTable2DAlg):
    pass



class LogLookupTableAlg(LookUpTable):
    TABLE_PARAM = ''



class LogLookupTableLoRangeAlg(LogLookupTableAlg):
    pass



class RMSTableExtRangeFixAlg(LookUpTable, DynamicsProcessor, RMS):
    TABLE_PARAM = ''

    RMS_PARAM = 'RMS'
    HOLD_PARAM = 'hold'
    DECAY_PARAM = 'decay'



class LookupTableAlgNew(LookUpTable):
    TABLE_PARAM = 'table_p0'
    MAXINDEX_PARAM = 'maxindex'


    def set_table(self, values, **kwargs):
        self.set_param(len(values) - 1, self.MAXINDEX_PARAM, **kwargs)
        super().set_table(values, **kwargs)



class LookupTableConfigOutFormatAlgNew(LookupTableAlgNew):
    pass
