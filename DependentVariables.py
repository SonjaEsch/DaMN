import pprint
import numpy as np


class DependentVariables:

    def __init__(self):
        self.mass_matrix = []
        self.mass_eigenstates = []
        self.mixing_matrix = []

    def calculate_eigenstates_mixing_matrix_from_mass_matrix(self):
        eigenvalues, eigenvectors = np.linalg.eig(np.array(self.mass_matrix))
        self.mass_eigenstates = eigenvalues.tolist()
        self.mixing_matrix = eigenvectors.tolist()


    def __str__(self):
        string = "{}\n".format(self.__class__.__name__)
        for key in self.__dict__:
            string += "\t{}: {}\n".format(key, self.__dict__[key])

        return string

    def pprint(self):
        pretty = pprint.PrettyPrinter(indent=4)

        print("mass_matrix")
        pretty.pprint(self.mass_matrix)

        print("mass_eigenstates")
        pretty.pprint(self.mass_eigenstates)

        print("mixing_matrix")
        pretty.pprint(self.mixing_matrix)


