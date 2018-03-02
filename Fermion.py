import Particle


class Fermion(Particle.Particle):
    parameters = ["mass_singlet", "mass_doublet", "y1", "y2"]


if __name__ == "__main__":
    fermion_creator = Particle.ParticleCreator(Fermion, "configs/fermion.json")
    for i in range(1000):
        fermion = fermion_creator.create()
        print(fermion.to_json())