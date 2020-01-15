class Switch:
    def __init__(self, default=False, onflip=None):
        """
        :param default: starting value
        :param onflip: function to be executed on value change parameters(current_value: bool)
        """
        self._value = default

        if onflip is None:
            onflip = lambda _: None
        self.onflip = onflip

    def flip(self) -> bool:
        """
        inverts the switch value

        :return: current value
        """
        self._value = not self._value
        self.onflip(self.get())

        return self._value

    def set(self, value: bool):
        """
        sets the current value to :param value:

        :param value: value to be set to
        :return: current value
        """

        self._value = value
        self.onflip(self.get())

        return self._value

    def get(self):
        """
        :return: current value
        """
        return self._value