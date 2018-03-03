import random

import Fermion
import Higgs
import ModelSPheno
import NeutrinoCouplings
import Particle
import Scalar

import math
import time

def higgs_mass_likelihood(mass_eigenstates):
    mu = 124.98
    sigma = 0.28

    return math.exp((-(mu-mass_eigenstates[0])**2)/(2*sigma**2))

def calculate_likelihood(model):
    return higgs_mass_likelihood(model.higgs_dependent.mass_eigenstates)

def random_scan():
    number_of_points_checked = 0
    number_of_points = 100
    accepted_points = []


    higgs_creator = Particle.ParticleCreator(Higgs.Higgs, "configs/higgs.json")
    scalar_creator = Particle.ParticleCreator(Scalar.Scalar, "configs/scalar.json")
    fermion_creator = Particle.ParticleCreator(Fermion.Fermion, "configs/fermion.json")
    neutrino_creator = Particle.ParticleCreator(NeutrinoCouplings.Neutrino, "configs/neutrino_couplings.json")

    time_start = time.time()
    time_last_report = 0
    time_report_interval = 10

    while len(accepted_points) < number_of_points:

        time_running = time.time() - time_start
        if time_running > time_last_report + time_report_interval:
            time_last_report = time_running
            print("[{:0.1f}]: Checked: {}, Accepted: {}({:0.2f}/s)".format(
                time_running,
                number_of_points_checked,
                len(accepted_points),
                len(accepted_points)/time_running)
            )


        model = ModelSPheno.ModelSPheno(
            higgs_creator.create(),
            fermion_creator.create(),
            scalar_creator.create(),
            neutrino_creator.create(),
            calculate_branching_ratios=False,
            calculate_one_loop_masses=True
        )

        number_of_points_checked += 1

        try:
            model.calculate_dependent_variables()
        except:
            continue

        if random.random() < calculate_likelihood(model):
            accepted_points.append(model)

    for point in accepted_points:
        print(point.to_json())


if __name__ == "__main__":
    random_scan()
