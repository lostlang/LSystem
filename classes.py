
class LSystem:

    def __init__(self, seed: str, rules: dict):
        """
        Create object LSystem type
        :param seed: start system value
        :param rules: rule for changing system
        """
        self._value = seed
        self._rules = rules

    def _update_system(self):
        """
        Function for updating system value
        """
        self._value = "".join([self._rules[i] if i in self._rules else i
                               for i in self._value])

    def next(self, step=None):
        """
        Function for use rules into system value
        :param step: number of iteration ( if type not int, step = 1 )
        :return: value system after step
        """
        if type(step) is not int:
            step = 1
        for i in range(step):
            self._update_system()

        return self._value

    def get_value(self):
        """
        Function for get system value
        :return: value system
        """
        return self._value
