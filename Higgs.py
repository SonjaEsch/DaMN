import Particle


class Higgs(Particle.Particle):
    def __init__(self):
        self.vev = None
        self.lambda_higgs = None
        self.mass = None
        self.tree_level_mass = None


class HiggsCreator(Particle.ParticleCreator):
    def __init__(self, filename=None):
        super().__init__(Higgs, filename)


if __name__ == "__main__":
    higgs_creator = HiggsCreator("higgs.json")

    print(higgs_creator.create())
