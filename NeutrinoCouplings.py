import Particle


class Neutrino(Particle.Particle):
    parameters = ["g11", "g12", "g13", "g21", "g22", "g23"]


if __name__ == "__main__":
    neutrino_creator = Particle.ParticleCreator(Neutrino, "neutrino_couplings.json")
    for i in range(1000):
        neutrino = neutrino_creator.create()
        print(neutrino.to_json())