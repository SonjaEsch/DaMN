import Particle


class Neutrino(Particle.Particle):
    parameters = ["sin_theta12_squared_e5", "sin_theta_13_squared_e4", "sin_theta_23_squared", "delta_m12_squared",
                  "delta_m23_squared", "cos_casas_ibarra_angle"]


if __name__ == "__main__":
    neutrino_creator = Particle.ParticleCreator(Neutrino, "neutrino_masses.json")
    for i in range(1000):
        neutrino = neutrino_creator.create()
        print(neutrino.to_json())