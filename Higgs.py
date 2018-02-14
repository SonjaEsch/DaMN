import Particle


class Higgs(Particle.Particle):
    parameters = ["vev", "lambda_higgs"]


class HiggsCreator(Particle.ParticleCreator):
    def __init__(self, filename=None):
        super().__init__(Higgs, filename)


if __name__ == "__main__":
    higgs_creator = HiggsCreator("higgs.json")
    for i in range(100000):
        higgs = higgs_creator.create()
        print(higgs.to_json())