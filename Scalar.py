import Particle


class Scalar(Particle.Particle):
    parameters = ["mass_singlet", "mass_doublet", "lambda_S", "lambda_D", "lambda_P", "lambda_PP", "A"]


if __name__ == "__main__":
    scalar_creator = Particle.ParticleCreator(Scalar, "scalar.json")
    for i in range(1000):
        scalar = scalar_creator.create()
        print(scalar.to_json())