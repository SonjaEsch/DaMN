import Particle


class Neutrino(Particle.Particle):
    parameters = ["sin_theta12_squared", "sin_theta13_squared", "sin_theta23_squared", "delta_m12_squared_e5",
                  "delta_m23_squared_e4", "cos_casas_ibarra_angle"]


if __name__ == "__main__":
    neutrino_creator = Particle.ParticleCreator(Neutrino, "configs/neutrino_masses.json")
    for i in range(1000):
        neutrino = neutrino_creator.create()
        print(neutrino.to_json())