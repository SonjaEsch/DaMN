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

    def calculate_higgs_mass(self):
        self.higgs_dependent.mass_matrix = [math.sqrt(self.higgs.lambda_higgs * self.higgs.vev ** 2)]
        self.higgs_dependent.mass_eigenstates = self.higgs_dependent.mass_matrix
        self.higgs_dependent.mixing_matrix = [1]

    def calculate_scalar_masses_and_mixings(self):
        mixing_term = self.scalar.A * self.higgs.vev / math.sqrt(2.0)
        couplings_factor = 1 / 4.0 * self.higgs.vev ** 2
        doublet_couplings_plus = couplings_factor*(self.scalar.lambda_D + self.scalar.lambda_P + 2*self.scalar.lambda_PP)
        doublet_couplings_minus = couplings_factor*(self.scalar.lambda_D + self.scalar.lambda_P - 2*self.scalar.lambda_PP)

        self.scalar_dependent.mass_matrix = [
            [self.scalar.mass_singlet ** 2 + 1 / 4.0 * self.higgs.vev ** 2 * self.scalar.lambda_S, mixing_term, 0],
            [mixing_term, self.scalar.mass_doublet ** 2 + doublet_couplings_plus, 0],
            [0, 0, self.scalar.mass_doublet ** 2 + doublet_couplings_minus]]

        self.scalar_dependent.calculate_eigenstates_mixing_matrix_from_mass_matrix()

    def calculate_fermion_masses_and_mixings(self):

        y1_term = self.fermion.y1 * self.higgs.vev / math.sqrt(2.0)
        y2_term = self.fermion.y2 * self.higgs.vev / math.sqrt(2.0)

        self.fermion_dependent.mass_matrix = [[self.fermion.mass_singlet, y1_term, y2_term],
                                              [y1_term, 0, self.fermion.mass_doublet],
                                              [y2_term, self.fermion.mass_doublet, 0]]

        self.fermion_dependent.calculate_eigenstates_mixing_matrix_from_mass_matrix()

    def calculate_neutrino_masses_and_mixings(self):
        couplings1 = [self.neutrino.g11, self.neutrino.g12, self.neutrino.g13]
        couplings2 = [self.neutrino.g21, self.neutrino.g22, self.neutrino.g23]

        self.neutrino_dependent.mass_matrix = []

        c11 = 0.0
        c12 = 0.0
        c22 = 0.0

        for j in range(3):
            for m in range(3):
                mass_fermion = self.fermion_dependent.mass_eigenstates[j]
                mass_scalar = math.sqrt(self.scalar_dependent.mass_eigenstates[m])

                mixing_fermion = self.fermion_dependent.mixing_matrix
                mixing_scalar = self.scalar_dependent.mixing_matrix

                # TODO important! notice the scalar mass matrix is quadratic and write it somewhere so people will know
                ljm = 1 / (16 * np.pi ** 2) * mass_fermion / (mass_scalar ** 2 - mass_fermion ** 2) * (
                        mass_fermion ** 2 * math.log(float(mass_fermion ** 2)) - mass_scalar ** 2 * math.log((mass_scalar ** 2)))

                c11 += mixing_fermion[2][j] ** 2 * mixing_scalar[0][m] ** 2 * ljm
                c12 += mixing_fermion[0][j] * mixing_fermion[2][j] * mixing_scalar[0][m] * mixing_scalar[1][m] * ljm
                c22 += mixing_fermion[0][j] ** 2 * (mixing_scalar[1][m] ** 2 - mixing_scalar[2][m] ** 2) * ljm

        for i in range(3):
            row = []
            for k in range(3):
                row.append(-c11 * couplings1[i] * couplings1[k]
                           + c12 * couplings1[i] * couplings2[k]
                           + c12 * couplings1[k] * couplings2[i]
                           - c22 * couplings2[i] * couplings2[k])

            self.neutrino_dependent.mass_matrix.append(row)

        self.neutrino_dependent.calculate_eigenstates_mixing_matrix_from_mass_matrix()
        # TODO one of the neutrino mass eigenvalues is actually zero! Due to numerical uncertainties it is around 1e-20
        # should it just be fixed to 0 automatically?

    def calculate_dependent_variables(self):
        # TODO one should only be able to use this function from outside, the other should not be avilable
        self.calculate_higgs_mass()
        self.calculate_scalar_masses_and_mixings()
        self.calculate_fermion_masses_and_mixings()
        self.calculate_neutrino_masses_and_mixings()


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

    # depVar = DependentVariables()
    # print(depVar.mixing_matrix) #FIXME mixing matrix does not exist even though it is defined in __init__
    #
    # print("compare")
    # print(higgsDummy.vev)
    # print("=?")
    # print(model.higgs.vev)

    # print(model.scalar_dependent.mixing_matrix) # TODO does not exist yet...just after calculating everything

    model.calculate_dependent_variables()

    print("Higgs")
    model.higgs_dependent.pprint()

    print("Scalar")
    model.scalar_dependent.pprint()

    print("Fermion")
    model.fermion_dependent.pprint()

    print("Neutrino")
    model.neutrino_dependent.pprint()
