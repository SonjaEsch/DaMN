import Particle


class Higgs(Particle.Particle):
    parameters = ["vev", "lambda_higgs", "mass", "tree_level_mass"]


class HiggsCreator(Particle.ParticleCreator):
    def __init__(self, filename=None):
        super().__init__(Higgs, filename)


if __name__ == "__main__":
    higgs_creator = HiggsCreator("higgs.json")
    print(higgs_creator.create())
