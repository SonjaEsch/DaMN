import Model
import Particle
import Higgs
import Scalar
import Fermion
import NeutrinoCouplings
import numpy as np
import pprint
from DependentVariables import DependentVariables

# TODO write a routine to save/restore model points easily
# TODO in other scenarios the neutrino couplings are not input parameter but the mass eigenstates and mixing matrix are
# TODO if one would like to write all couplings to micromegas or spheno input how can one have everything accessible in the same way?
# is it a good idea to add the couplings to the neutrino element in model afterwards ??

# TODO only the routine for neutrinos is different, should one still leave this as one model construction?
# shall the other functions be separated?



def diagonalization(matrix):
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

    def calculate_higgs_mass(self):
        self.higgs_dependent.mass_matrix = [np.sqrt(self.higgs.lambda_higgs * self.higgs.vev ** 2)]
        self.higgs_dependent.mass_eigenstates = self.higgs_dependent.mass_matrix
        self.higgs_dependent.mixing_matrix = [1]

    def calculate_scalar_masses_and_mixings(self):
        self.scalar_dependent.mass_matrix = [
            [self.scalar.mass_singlet ** 2 + 1 / 4.0 * self.higgs.vev ** 2 * self.scalar.lambda_S,
             self.scalar.A * self.higgs.vev / np.sqrt(2.0),
             0],
            [self.scalar.A * self.higgs.vev / np.sqrt(2.0),
             self.scalar.mass_doublet ** 2 + 1 / 4.0 * self.higgs.vev ** 2 * (
                     self.scalar.lambda_D + self.scalar.lambda_P + 2 * self.scalar.lambda_PP),
             0],
            [0,
             0,
             self.scalar.mass_doublet ** 2 + 1 / 4.0 * self.higgs.vev ** 2 * (
                     self.scalar.lambda_D + self.scalar.lambda_P - 2 * self.scalar.lambda_PP)]]

        self.scalar_dependent.mass_eigenstates, self.scalar_dependent.mixing_matrix = diagonalization(
            self.scalar_dependent.mass_matrix)

    def calculate_fermion_masses_and_mixings(self):

        temp1 = self.fermion.y1 * self.higgs.vev / np.sqrt(2.0)
        temp2 = self.fermion.y2 * self.higgs.vev / np.sqrt(2.0)

        self.fermion_dependent.mass_matrix = [[self.fermion.mass_singlet, temp1, temp2],
                                              [temp1, 0, self.fermion.mass_doublet],
                                              [temp2, self.fermion.mass_doublet, 0]]
        self.fermion_dependent.mass_eigenstates, self.fermion_dependent.mixing_matrix = diagonalization(
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
                mass_scalar = np.sqrt(self.scalar_dependent.mass_eigenstates[m])

                mixing_fermion = self.fermion_dependent.mixing_matrix
                mixing_scalar = self.scalar_dependent.mixing_matrix

                # TODO important! notice the scalar mass matrix is quadratic and write it somewhere so people will know
                ljm = 1 / (16 * np.pi ** 2) * mass_fermion / (mass_scalar ** 2 - mass_fermion ** 2) * (
                        mass_fermion ** 2 * np.log(float(mass_fermion ** 2)) - mass_scalar ** 2 * np.log(
                    float(mass_scalar ** 2)))

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

        self.neutrino_dependent.mass_eigenstates, self.neutrino_dependent.mixing_matrix = diagonalization(
            self.neutrino_dependent.mass_matrix)

        # TODO one of the neutrino mass eigenvalues is actually zero! Due to numerical uncertainties it is around 1e-20
        # should it just be fixed to 0 automatically?

    def calculate_dependent_variables(self):
        # TODO one should only be able to use this function from outside, the other should not be avilable
        self.calculate_higgs_mass()
        self.calculate_scalar_masses_and_mixings()
        self.calculate_fermion_masses_and_mixings()
        self.calculate_neutrino_masses_and_mixings()

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

    pretty = pprint.PrettyPrinter(indent=4)
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
