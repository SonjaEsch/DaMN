import json

from Distribution import parse_dictionary_to_distribution


class Particle:
    parameters = []

    def __init__(self):
        for key in self.parameters:
            self.__dict__.update({key: None})

    def __str__(self):
        string = "{}\n".format(self.__class__.__name__)
        for key in self.__dict__:
            string += "\t{}: {}\n".format(key, self.__dict__[key])

        return string


class ParticleCreator:
    def __init__(self, particle_class, filename=None):
        self.particle_class = particle_class
        self.initialize_to_none()
        self.parse_config(filename)

    def initialize_to_none(self):
        for key in self.particle_class.parameters:
            self.__dict__.update({key: None})

    def parse_config(self, filename):
        with open(filename) as file:
            config = json.load(file)
            for key in self.particle_class.parameters:
                if key in config:
                    try:
                        self.__dict__[key] = float(config[key])
                    except TypeError:
                        self.__dict__[key] = parse_dictionary_to_distribution(config[key])

    def create(self):
        particle = self.particle_class()
        for key in self.particle_class.parameters:
            if key in particle.__dict__:
                try:
                    particle.__dict__[key] = self.__dict__[key]()
                except TypeError:
                    particle.__dict__[key] = self.__dict__[key]
        return particle
