import Particle


class Higgs(Particle.Particle):
    parameters = ["vev", "lambda_higgs"]


if __name__ == "__main__":
    higgs_creator = Particle.ParticleCreator(Higgs, "configs/higgs.json")
    for i in range(100000):
        higgs = higgs_creator.create()
        print(higgs.to_json())