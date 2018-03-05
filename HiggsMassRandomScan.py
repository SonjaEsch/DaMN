import random

import Fermion
import Higgs
import ModelSPheno
import NeutrinoCouplings
import Particle
import Scalar

import math
import time
import datetime
import json
import os

import matplotlib.pyplot as plt
from MicroMegas import MicroMegas


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
    time_report_interval = 5

    while len(accepted_points) < number_of_points:

        time_running = time.time() - time_start
        if time_running > time_last_report + time_report_interval:
            time_last_report = time_running
            print("[{:0.1f}]: Checked: {}({:0.2f}/s), Accepted: {}({:0.2f}/s)".format(
                time_running,
                number_of_points_checked,
                number_of_points_checked/time_running,
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

        micromegas = MicroMegas(model.spheno_output_file_path)
        micromegas.calculate()

        if random.random() < calculate_likelihood(model):
            accepted_points.append(model)
            with open("saved_models/{}.json".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f")), "w") as f:
                f.write(
                    json.dumps(model, default=lambda object: object.__dict__, sort_keys=True, indent=4)
                )


def load_scan_data():
    base_dir="saved_models"
    models = []
    for filename in os.listdir(base_dir):
        with open(os.path.join(base_dir, filename), "r") as filehandle:
            models.append(json.load(filehandle))

    return models


def plot_function_vs_function(function1, function2, axis, models):

    x = [(function1(model)) for model in models]
    y = [(function2(model)) for model in models]

    # axis.set_xscale("log")
    # axis.set_yscale("log")

    axis.hist2d(x, y, bins=20, normed=True, cmap=plt.cm.spectral)


def plot(functions, models):
    n = len(functions)
    f, axarr = plt.subplots(n, n, sharex='col', sharey='row')
    for x in range(n):
        for y in range(n):
            plot_function_vs_function(functions[x], functions[y], axarr[y, x], models)

    plt.show()


if __name__ == "__main__":
    # random_scan()
    models = load_scan_data()

    functions = []
    tmp_function = lambda particle, parameter: (lambda model: model[particle][parameter])

    for parameter in Higgs.Higgs.parameters:
        functions.append(tmp_function("higgs", parameter))

    for parameter in Scalar.Scalar.parameters:
        functions.append(tmp_function("scalar", parameter))

    for parameter in Fermion.Fermion.parameters:
        functions.append(tmp_function("fermion", parameter))

    for parameter in NeutrinoCouplings.Neutrino.parameters:
        functions.append(tmp_function("neutrino", parameter))

    plot(
        functions,
        models
    )
