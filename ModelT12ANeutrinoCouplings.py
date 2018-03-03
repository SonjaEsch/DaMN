import Model
import Particle
import Higgs
import Scalar
import Fermion
import NeutrinoCouplings
import numpy as np
import math
from DependentVariables import DependentVariables


class ModelT12A(Model.Model):

    def __init__(self, higgs, fermion, scalar, neutrino):
        super().__init__()
        self.higgs = higgs
        self.scalar = scalar
        self.fermion = fermion
        self.neutrino = neutrino

        self.higgs_dependent = DependentVariables()
        self.scalar_dependent = DependentVariables()
        self.fermion_dependent = DependentVariables()
        self.neutrino_dependent = DependentVariables()

    def calculate_dependent_variables(self):
        self.calculate_higgs_dependent()
        self.calculate_scalar_dependent()
        self.calculate_fermion_dependent()
        self.calculate_neutrino_dependent()

    def calculate_higgs_dependent(self):
        self.higgs_dependent.mass_matrix = [math.sqrt(self.higgs.lambda_higgs * self.higgs.vev ** 2)]
        self.higgs_dependent.mass_eigenstates = self.higgs_dependent.mass_matrix
        self.higgs_dependent.mixing_matrix = [1]

    def calculate_scalar_dependent(self):
        mixing_term = self.scalar.A * self.higgs.vev
        couplings_factor = 1 / 2.0 * self.higgs.vev ** 2
        doublet_couplings_plus = couplings_factor*(self.scalar.lambda_D + self.scalar.lambda_P + 2*self.scalar.lambda_PP)
        doublet_couplings_minus = couplings_factor*(self.scalar.lambda_D + self.scalar.lambda_P - 2*self.scalar.lambda_PP)

        self.scalar_dependent.mass_matrix = [
            [self.scalar.mass_singlet ** 2 + 1 / 2.0 * self.higgs.vev ** 2 * self.scalar.lambda_S, mixing_term, 0],
            [mixing_term, self.scalar.mass_doublet ** 2 + doublet_couplings_plus, 0],
            [0, 0, self.scalar.mass_doublet ** 2 + doublet_couplings_minus]]

        self.scalar_dependent.calculate_eigenstates_mixing_matrix_from_mass_matrix()

        if min(self.scalar_dependent.mass_eigenstates) < 0:
            raise ValueError("calculate_scalar_dependent: Found negative value in mass_eigenstates")

        self.scalar_dependent.mass_eigenstates = [math.sqrt(value) for value in self.scalar_dependent.mass_eigenstates]

    def calculate_fermion_dependent(self):

        y1_term = self.fermion.y1 * self.higgs.vev / math.sqrt(2.0)
        y2_term = self.fermion.y2 * self.higgs.vev / math.sqrt(2.0)

        self.fermion_dependent.mass_matrix = [[self.fermion.mass_singlet, y1_term, y2_term],
                                              [y1_term, 0, self.fermion.mass_doublet],
                                              [y2_term, self.fermion.mass_doublet, 0]]

        self.fermion_dependent.calculate_eigenstates_mixing_matrix_from_mass_matrix()

    def calculate_neutrino_dependent(self):

        co11, co12, co22 = self.get_neutrino_coefficients()

        couplings1 = [self.neutrino.g11, self.neutrino.g12, self.neutrino.g13]
        couplings2 = [self.neutrino.g21, self.neutrino.g22, self.neutrino.g23]
        self.neutrino_dependent.mass_matrix = []

        for i in range(3):
            row = []
            for k in range(3):
                row.append(-co11 * couplings1[i] * couplings1[k]
                           + co12 * couplings1[i] * couplings2[k]
                           + co12 * couplings1[k] * couplings2[i]
                           - co22 * couplings2[i] * couplings2[k])

            self.neutrino_dependent.mass_matrix.append(row)

        self.neutrino_dependent.calculate_eigenstates_mixing_matrix_from_mass_matrix()

    def get_neutrino_coefficients(self):
        co11 = 0.0
        co12 = 0.0
        co22 = 0.0

        mixing_fermion = self.fermion_dependent.mixing_matrix
        mixing_scalar = self.scalar_dependent.mixing_matrix

        for j in range(3):
            for m in range(3):
                mass_fermion = self.fermion_dependent.mass_eigenstates[j]
                mass_scalar = self.scalar_dependent.mass_eigenstates[m]

                mass_combination_jm = 1 / (16 * np.pi ** 2) * mass_fermion / (mass_scalar ** 2 - mass_fermion ** 2) * (
                        mass_fermion ** 2 * math.log(float(mass_fermion ** 2)) - mass_scalar ** 2
                        * math.log((mass_scalar ** 2)))

                co11 += mixing_fermion[2][j] ** 2 * mixing_scalar[0][m] ** 2 * mass_combination_jm
                co12 += mixing_fermion[0][j] * mixing_fermion[2][j] * mixing_scalar[0][m] * mixing_scalar[1][
                    m] * mass_combination_jm
                co22 += mixing_fermion[0][j] ** 2 * (
                            mixing_scalar[1][m] ** 2 - mixing_scalar[2][m] ** 2) * mass_combination_jm
        return co11, co12, co22

    def pprint(self):
        print(self.higgs)
        self.higgs_dependent.pprint()

        print(self.scalar)
        self.scalar_dependent.pprint()

        print(self.fermion)
        self.fermion_dependent.pprint()

        print(self.neutrino)
        self.neutrino_dependent.pprint()


if __name__ == "__main__":
    higgs_creator = Particle.ParticleCreator(Higgs.Higgs, "configs/higgs.json")
    higgsDummy = higgs_creator.create()

    scalar_creator = Particle.ParticleCreator(Scalar.Scalar, "configs/scalar.json")
    scalarDummy = scalar_creator.create()

    fermion_creator = Particle.ParticleCreator(Fermion.Fermion, "configs/fermion.json")
    fermionDummy = fermion_creator.create()

    neutrino_creator = Particle.ParticleCreator(NeutrinoCouplings.Neutrino, "configs/neutrino_couplings.json")
    neutrinoDummy = neutrino_creator.create()

    model = ModelT12A(higgsDummy, fermionDummy, scalarDummy, neutrinoDummy)

    model.calculate_dependent_variables()

    model.pprint()

