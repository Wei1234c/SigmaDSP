try:
    from .nth_order import NthOrderFilter

except:
    from nth_order import NthOrderFilter



class CrossOver(NthOrderFilter):
    pass



class CrossoverFilter2WayAlgDP(CrossOver):
    pass



class CrossoverFilter2WayAlgSP(CrossOver):
    pass



class CrossoverFilter3WayAlgDP(CrossOver):
    pass



class CrossoverFilter3WayAlgSP(CrossOver):
    pass
