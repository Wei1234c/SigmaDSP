try:
    from ..basic_dsp.adjustable_gain import AdjustableGain

except:
    from adjustable_gain import AdjustableGain



class Splitter(AdjustableGain):
    pass



class SingleCtrlSplit(Splitter):
    GAIN_PARAM = ''



class SingleCtrlSplitSlew(SingleCtrlSplit):
    pass



class MultiCtrlSplitter(Splitter):

    def set_dB(self, dB, idx = 0, **kwargs):
        super().set_dB(dB, param_name = f'{(idx + 1)}', **kwargs)



class MultiCtrlSplitterSLEW(MultiCtrlSplitter):
    pass
