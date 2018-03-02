import random


class Distribution:
    def __call__(self):
        raise NotImplementedError


class ConstantDistribution(Distribution):
    def __init__(self, dictionary):
        self.value = dictionary["value"]

    def __call__(self):
        return self.value


class UniformRealDistribution(Distribution):
    def __init__(self, dictionary):
        self.max_value = dictionary["max_value"]
        self.min_value = dictionary["min_value"]

    def __call__(self):
        return random.uniform(self.min_value, self.max_value)


class UniformExponentDistribution(Distribution):
    def __init__(self, dictionary):
        self.factor = dictionary["factor"]
        self.base = dictionary["base"]
        self.min_exponent = dictionary["min_exponent"]
        self.max_exponent = dictionary["max_exponent"]

    def __call__(self):
        return self.factor * pow(self.base, random.uniform(self.min_exponent, self.max_exponent))


class NormalDistribution(Distribution):
    def __init__(self, dictionary):
        self.sigma = dictionary["sigma"]
        self.mu = dictionary["mu"]

    def __call__(self):
        return random.normalvariate(self.mu, self.sigma)


class MergedDistribution(Distribution):
    def __init__(self, dictionary):
        self.distribution1 = parse_dictionary_to_distribution(dictionary["distribution1"])
        self.distribution2 = parse_dictionary_to_distribution(dictionary["distribution2"])

    def __call__(self):
        distribution = random.choice([self.distribution1, self.distribution2])
        return distribution()


type_keyword = "type"
parameters_keyword = "parameters"
class_keyword = "class"

distribution_keywords = {
    "constant": {parameters_keyword: ["value"], class_keyword: ConstantDistribution},

    "uniform": {parameters_keyword: ["min_value", "max_value"], class_keyword: UniformRealDistribution},

    "uniform_exponential": {parameters_keyword: ["factor", "base", "min_exponent", "max_exponent"],
                            class_keyword: UniformExponentDistribution},

    "normal": {parameters_keyword: ["sigma", "mu"], class_keyword: NormalDistribution},

    "merged": {parameters_keyword: ["distribution1", "distribution2"], class_keyword: MergedDistribution}
}


def parse_dictionary_to_distribution(distribution_dictionary):
    if type_keyword not in distribution_dictionary:
        print("Type keyword missing in config.")
        raise TypeError

    distribution_type = distribution_dictionary[type_keyword]

    if distribution_type not in distribution_keywords:
        print("Cannot parse distribution of type {}".format(distribution_type))
        raise TypeError

    for key in distribution_keywords[distribution_type]["parameters"]:
        if key not in distribution_dictionary:
            print("parameter {} is missing in config".format(key))
            raise TypeError

    return distribution_keywords[distribution_type]["class"](distribution_dictionary)
