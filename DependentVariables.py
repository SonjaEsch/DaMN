class DependentVariables:

    def __init__(self):
        self.mass_matrix = []
        self.mass_eigenstates = []
        self.mixing_matrix = []

    def __str__(self):
        # TODO the print routine does not print DependentVariable objects nicely, the matrices do not look good

        string = "{}\n".format(self.__class__.__name__)
        for key in self.__dict__:
            string += "\t{}: {}\n".format(key, self.__dict__[key])

        return string
