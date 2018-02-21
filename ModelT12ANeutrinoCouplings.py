import Model
import Particle
import Higgs
import Scalar
import Fermion
import NeutrinoCouplings
import numpy as np
import pprint


# TODO write a routine to save/restore model points easily

# TODO should this be in an extra file?
class DependentVariables:

    def __init__(self):
        mass_matrix = []
        mass_eigenstates = []
        mixing_matrix = []


def diagnolaization(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(np.array(matrix))
    return eigenvalues.tolist(), eigenvectors.tolist()


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
        self.calculate_higgs_mass()
        self.calculate_scalar_masses_and_mixings()
        self.calculate_fermion_masses_and_mixings()
        self.calculate_neutrino_masses_and_mixings()

    def calculate_higgs_mass(self):
        self.higgs_dependent.mass_matrix = [np.sqrt(self.higgs.lambda_higgs * self.higgs.vev ** 2)]
        self.higgs_dependent.mass_eigenstates = self.higgs_dependent.mass_matrix
        self.higgs_dependent.mixing_matrix = [1]

    def calculate_scalar_masses_and_mixings(self):
        self.scalar_dependent.mass_matrix = [
            [self.scalar.mass_singlet ** 2 + 0.5 * self.higgs.vev ** 2 * self.scalar.lambda_S,
             self.scalar.A * self.higgs.vev, 0],
            [self.scalar.A * self.higgs.vev,
             self.scalar.mass_doublet ** 2 + 0.5 * self.higgs.vev ** 2 * (
                     self.scalar.lambda_D + self.scalar.lambda_P + self.scalar.lambda_PP), 0],
            [0, 0, self.scalar.mass_doublet ** 2 + 0.5 * self.higgs.vev ** 2 * (
                    self.scalar.lambda_D + self.scalar.lambda_P - self.scalar.lambda_PP)]]

        self.scalar_dependent.mass_eigenstates, self.scalar_dependent.mixing_matrix = diagnolaization(
            self.scalar_dependent.mass_matrix)

    def calculate_fermion_masses_and_mixings(self):

        temp1 = self.fermion.y1 * self.higgs.vev / np.sqrt(2.0)
        temp2 = self.fermion.y2 * self.higgs.vev / np.sqrt(2.0)

        self.fermion_dependent.mass_matrix = [[self.fermion.mass_singlet, temp1, temp2],
                                              [temp1, 0, self.fermion.mass_doublet],
                                              [temp2, self.fermion.mass_doublet, temp2]]
        self.fermion_dependent.mass_eigenstates, self.fermion_dependent.mixing_matrix = diagnolaization(
            self.fermion_dependent.mass_matrix)

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
                mass_scalar = self.scalar_dependent.mass_eigenstates[m]
                mixing_fermion = self.fermion_dependent.mixing_matrix
                mixing_scalar = self.scalar_dependent.mixing_matrix

                ljm = 1 / (16 * np.pi ** 2) * mass_fermion / (mass_scalar ** 2 - mass_fermion ** 2) * (
                        mass_fermion ** 2 * np.log(float(mass_fermion ** 2)) + mass_scalar ** 2 * np.log(
                    float(mass_scalar ** 2)))

                c11 += mixing_fermion[2][j] ** 2 * mixing_scalar[0][m] ** 2 * ljm
                c12 += mixing_fermion[0][j] * mixing_fermion[2][j] * mixing_scalar[0][m] * mixing_scalar[1][m] * ljm
                c22 += mixing_fermion[0][j] ** 2 * mixing_scalar[2][m] ** 2 * ljm

        for i in range(3):
            row = []
            for k in range(3):
                row.append(c11 * couplings1[i] * couplings1[k]
                           + c12 * couplings1[i] * couplings2[k]
                           + c12 * couplings1[k] * couplings2[i]
                           + c22 * couplings2[i] * couplings2[k])

            self.neutrino_dependent.mass_matrix.append(row)

        self.neutrino_dependent.mass_eigenstates, self.neutrino_dependent.mixing_matrix = diagnolaization(
            self.neutrino_dependent.mass_matrix)


if __name__ == "__main__":
    higgs_creator = Higgs.HiggsCreator("higgs.json")
    higgsDummy = higgs_creator.create()

    scalar_creator = Particle.ParticleCreator(Scalar.Scalar, "scalar.json")
    scalarDummy = scalar_creator.create()

    fermion_creator = Particle.ParticleCreator(Fermion.Fermion, "fermion.json")
    fermionDummy = fermion_creator.create()

    neutrino_creator = Particle.ParticleCreator(NeutrinoCouplings.Neutrino, "neutrino_couplings.json")
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

    pretty = pprint.PrettyPrinter(indent = 4)
    print("higgs mass")
    pretty.pprint(model.higgs_dependent.mass_eigenstates)
    print("\n")

    print("Scalar mixing matrix")
    pretty.pprint(model.scalar_dependent.mixing_matrix)
    print("\n")

    print("scalar masses")
    pretty.pprint(model.scalar_dependent.mass_eigenstates)
    print("\n")

    print("Fermion mixing matrix")
    pretty.pprint(model.fermion_dependent.mixing_matrix)
    print("\n")

    print("fermion masses")
    pretty.pprint(model.fermion_dependent.mass_eigenstates)
    print("\n")

    print("neutrino mixing matrix")
    pretty.pprint(model.neutrino_dependent.mixing_matrix)
    print("\n")

    print("neutrino masses")
    pretty.pprint(model.neutrino_dependent.mass_eigenstates)
    print("\n")