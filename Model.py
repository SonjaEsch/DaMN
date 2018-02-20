import json


class Model:
    # particles = []  # TODO?? do we need this here?
    # mass_matrices = []
    # dependent_variables = []

    def __init__(self):
        # for particle in particles:
        #     self.particle = particle
        pass

    def __str__(self):
        pass

    def calculate_dependent_variables(self):
        pass

    def from_json(self):
        pass

    def to_json(self):
        return json.dumps(self.__dict__)
