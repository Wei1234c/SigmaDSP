try:
    from ..cell import Cell

except:
    from cell import Cell



class Pin(Cell):
    LEVEL_PARAM = None

    LOW = 0
    HIGH = 1


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = None
        self._invert = False


    def value(self, value = None, **kwargs):
        if value is None:
            self._value = self.get_param(self.LEVEL_PARAM, **kwargs).value
            return self._value
        else:
            self._value = value
            self.set_param(value, self.LEVEL_PARAM, **kwargs)


    def high(self):
        self.value(self.HIGH)


    def low(self):
        self.value(self.LOW)


    def on(self):
        self.low() if self._invert else self.high()


    def off(self):
        self.high() if self._invert else self.low()


    def toggle(self):
        self.value(not self.value())



class GeneralPurposeInput(Pin):
    LEVEL_PARAM = 'input'


    def value(self, value = None, **kwargs):
        self._value = self.get_param(self.LEVEL_PARAM, **kwargs).value
        return self._value



class GeneralPurposeOutput(Pin):
    LEVEL_PARAM = 'output'
