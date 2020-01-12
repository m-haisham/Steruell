class Switch:
    def __init__(self, default=False, onflip=None):
        self._value = default

        if onflip is None:
            onflip = lambda _: None
        self.onflip = onflip

    def flip(self):
        self._value = not self._value
        self.onflip(self.get())

    def set(self, value: bool):
        self._value = value
        self.onflip(self.get())

    def get(self):
        return self._value