import Model
import Particle
import Higgs
import Scalar
import Fermion
import NeutrinoCouplings
import numpy as np


class ModelT12A(Model.Model):

    def __init__(self, higgs, fermion, scalar, neutrino):
        super().__init__()
        self.higgs = higgs
        self.scalar = scalar
        self.fermion = fermion
        self.neutrino = neutrino
        self.scalar_mass_matrix = []
        self.scalar_mass_eigenstates = []
        self.scalar_mixing_matrix = []
        self.fermion_mass_matrix = []
        self.fermion_mass_eigenstates = []
        self.fermion_mixing_matrix = []
        self.neutrino_mass_matrix = []
        self.neutrino_mass_eigenstates = []
        self.neutrino_mixing_matrix = []

    def calculate_dependent_variables(self):
        self.calculate_higgs_mass()
        self.calculate_scalar_masses_and_mixings()
        self.calculate_fermion_masses_and_mixings()
        self.calculate_neutrino_masses_and_mixings()

    def calculate_higgs_mass(self):
        self.higgs.mass = np.sqrt(self.higgs.lambda_higgs * self.higgs.vev ** 2)

    def calculate_scalar_masses_and_mixings(self):  # TODO soll das alles in einer funktion sein? nicht lieber getrennt?
        # erscheint mir sehr unelegant!
        self.scalar_mass_matrix = [[self.scalar.mass_singlet ** 2 + 0.5 * self.higgs.vev ** 2 * self.scalar.lambda_S,
                                    self.scalar.A * self.higgs.vev, 0],
                                   [self.scalar.A * self.higgs.vev,
                                    self.scalar.mass_doublet ** 2 + 0.5 * self.higgs.vev ** 2 * (
                                            self.scalar.lambda_D + self.scalar.lambda_P + self.scalar.lambda_PP), 0],
                                   [0, 0, self.scalar.mass_doublet ** 2 + 0.5 * self.higgs.vev ** 2 * (
                                           self.scalar.lambda_D + self.scalar.lambda_P - self.scalar.lambda_PP)]]

        eigenvalues, eigenvectors = np.linalg.eig(np.array(self.scalar_mass_matrix))
        self.scalar_mass_eigenstates = eigenvalues.tolist()
        self.scalar_mixing_matrix = eigenvectors.tolist()

    def calculate_fermion_masses_and_mixings(self):

        temp1 = self.fermion.y1 * self.higgs.vev / np.sqrt(2.0)
        temp2 = self.fermion.y2 * self.higgs.vev / np.sqrt(2.0)

        self.fermion_mass_matrix = [[self.fermion.mass_singlet, temp1, temp2],
                                    [temp1, 0, self.fermion.mass_doublet],
                                    [temp2, self.fermion.mass_doublet, temp2]]

        eigenvalues, eigenvectors = np.linalg.eig(np.array(self.fermion_mass_matrix))
        self.fermion_mass_eigenstates = eigenvalues.tolist()
        self.fermion_mixing_matrix = eigenvectors.tolist()

    def calculate_neutrino_masses_and_mixings(self):
        couplings1 = [self.neutrino.g11, self.neutrino.g12, self.neutrino.g13]
        couplings2 = [self.neutrino.g21, self.neutrino.g22, self.neutrino.g23]

        self.neutrino_mass_matrix = []

        c11 = 0.0
        c12 = 0.0
        c22 = 0.0

        for j in range(3):
            for m in range(3):
                mass_fermion = self.fermion_mass_eigenstates[j]
                mass_scalar = self.scalar_mass_eigenstates[m]
                mixing_fermion = self.fermion_mixing_matrix
                mixing_scalar = self.scalar_mixing_matrix

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

            self.neutrino_mass_matrix.append(row)

        eigenvalues, eigenvectors = np.linalg.eig(np.array(self.fermion_mass_matrix))
        self.fermion_mass_eigenstates = eigenvalues.tolist()
        self.fermion_mixing_matrix = eigenvectors.tolist()


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

    print("compare")
    print(higgsDummy.vev)
    print("=?")
    print(model.higgs.vev)

    print("empty?")
    print(model.scalar_mixing_matrix)
    model.calculate_dependent_variables()
    print("not any more:")
    print(model.scalar_mixing_matrix)
