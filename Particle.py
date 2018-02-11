import json


class Particle:
    def __str__(self):
        string = "{}\n".format(self.__class__.__name__)
        for key in self.__dict__:
            string += "\t{}: {}\n".format(key, self.__dict__[key])

        return string


class ParticleCreator:
    def __init__(self, particle_class, filename=None):
        self.particle_class = particle_class
        temp_particle = particle_class()
        for key in temp_particle.__dict__:
            self.__dict__.update({key: None})

        self.parse_config(filename)

    def parse_config(self, filename):
        with open(filename) as file:
            config = json.load(file)
            print(config)
            for key in self.__dict__:
                if key in config:
                    try:
                        self.__dict__[key] = float(config[key])
                    except TypeError:
                        pass

    def create(self):
        particle = self.particle_class()
        for key in self.__dict__:
            if key in particle.__dict__:
                try:
                    particle.__dict__[key] = self.__dict__[key]()
                except TypeError:
                    particle.__dict__[key] = self.__dict__[key]
        return particle

