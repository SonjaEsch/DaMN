import json


class Model:
    def __init__(self):
        pass

    def __str__(self):
        string = "{}\n".format(self.__class__.__name__)
        for key in self.__dict__:
            string += "\t{}: {}\n".format(key, self.__dict__[key])

        return string

    def calculate_dependent_variables(self):
        pass

    def from_json(self):
        pass

    def to_json(self):
        return json.dumps(self.__dict__)
