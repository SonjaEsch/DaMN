import Model
import Particle
import Higgs
import Scalar
import Fermion
import NeutrinoMasses
import numpy as np
import math
from DependentVariables import DependentVariables


# TODO all questions for ModelT12ANeutrinoCouplings apply here as well
# TODO catch all exceptions otherwise one could mess up a whole scan afterwards

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
        self.scalar_dependent.mass_matrix = [
            [self.scalar.mass_singlet ** 2 + 1 / 4.0 * self.higgs.vev ** 2 * self.scalar.lambda_S,
             self.scalar.A * self.higgs.vev / math.sqrt(2.0),
             0],
            [self.scalar.A * self.higgs.vev / math.sqrt(2.0),
             self.scalar.mass_doublet ** 2 + 1 / 4.0 * self.higgs.vev ** 2 * (
                     self.scalar.lambda_D + self.scalar.lambda_P + 2 * self.scalar.lambda_PP),
             0],
            [0,
             0,
             self.scalar.mass_doublet ** 2 + 1 / 4.0 * self.higgs.vev ** 2 * (
                     self.scalar.lambda_D + self.scalar.lambda_P - 2 * self.scalar.lambda_PP)]]

        self.scalar_dependent.calculate_eigenstates_mixing_matrix_from_mass_matrix()

    def calculate_fermion_masses_and_mixings(self):

        temp1 = self.fermion.y1 * self.higgs.vev / math.sqrt(2.0)
        temp2 = self.fermion.y2 * self.higgs.vev / math.sqrt(2.0)

        self.fermion_dependent.mass_matrix = [[self.fermion.mass_singlet, temp1, temp2],
                                              [temp1, 0, self.fermion.mass_doublet],
                                              [temp2, self.fermion.mass_doublet, 0]]
        self.fermion_dependent.calculate_eigenstates_mixing_matrix_from_mass_matrix()

    def calculate_neutrino_masses_mixings_and_couplings(self):

        m1 = 0
        m2 = math.sqrt(self.neutrino.delta_m12_squared_e5 * 10 ** (-5))
        m3 = math.sqrt(
            self.neutrino.delta_m23_squared_e4 * 10 ** (-4) + 0.5 * self.neutrino.delta_m12_squared_e5 * 10 ** (-5))

        self.neutrino_dependent.mass_eigenstates = [m1, m2, m3]

        s12 = math.sqrt(self.neutrino.sin_theta12_squared)
        s13 = math.sqrt(self.neutrino.sin_theta13_squared)
        s23 = math.sqrt(self.neutrino.sin_theta23_squared)

        c12 = math.sqrt(1 - s12 ** 2)
        c13 = math.sqrt(1 - s13 ** 2)
        c23 = math.sqrt(1 - s23 ** 2)

        self.neutrino_dependent.mixing_matrix = [[c12 * c13, -s12 * c23 - c12 * s23 * s13, s12 * s23 - c12 * c23 * s13],
                                                 [s12 * c13, c12 * c23 - s12 * s23 * s13, -c12 * s23 - s12 * c23 * s13],
                                                 [s13, s23 * c13, c23 * c13]]

        co11 = 0.0
        co12 = 0.0
        co22 = 0.0

        for j in range(3):
            for m in range(3):
                mass_fermion = self.fermion_dependent.mass_eigenstates[j]
                mass_scalar = math.sqrt(self.scalar_dependent.mass_eigenstates[m])

                mixing_fermion = self.fermion_dependent.mixing_matrix
                mixing_scalar = self.scalar_dependent.mixing_matrix

                ljm = 1 / (16 * math.pi ** 2) * mass_fermion / (mass_scalar ** 2 - mass_fermion ** 2) * (
                        mass_fermion ** 2 * math.log(float(mass_fermion ** 2)) - mass_scalar ** 2 * math.log((mass_scalar ** 2)))

                co11 += mixing_fermion[2][j] ** 2 * mixing_scalar[0][m] ** 2 * ljm
                co12 += mixing_fermion[0][j] * mixing_fermion[2][j] * mixing_scalar[0][m] * mixing_scalar[1][m] * ljm
                co22 += mixing_fermion[0][j] ** 2 * (mixing_scalar[1][m] ** 2 - mixing_scalar[2][m] ** 2) * ljm

        matrix_a = [[-co11, co12], [co12, -co22]]
        # TODO are the signs reasonable?

        eigenvalues_np_array, eigenvectors_np_array = np.linalg.eig(np.array(matrix_a))
        eigenvalues = eigenvalues_np_array.tolist()
        eigenvectors = eigenvectors_np_array.tolist()

        # TODO raise exception if one or more eigenvalues are zero! this parameter point does not converge
        # TODO it is necessary to use a new one
        # TODO how to stop and not proceed in this case?
        # TODO question: how many points are excluded because of this?
        # TODO think about better text for exception

        temp = []

        for entry in eigenvalues:
            try:
                val = 1/math.sqrt(entry)
                temp.append(val)

            except ValueError:
                print("Cannot calculate neutrino couplings. Encountered negative value in sqrt")
                raise ValueError("Cannot calculate neutrino couplings. Encountered negative value in sqrt")

        diag_a_sqrt_inverse = np.diag(temp)
        diag_nu_sqrt = np.diag([math.sqrt(m1), math.sqrt(m2), math.sqrt(m3)])
        u_a = np.array(eigenvectors)
        u_nu = np.array(self.neutrino_dependent.mixing_matrix)

        cr = self.neutrino.cos_casas_ibarra_angle
        sr = math.sqrt(1 - cr ** 2)
        r = np.array([[0, cr, -sr], [0, sr, cr]])

        neutrino_couplings = np.dot(np.dot(np.dot(u_a, diag_a_sqrt_inverse), np.dot(r, diag_nu_sqrt)), u_nu.transpose())

        self.neutrino.g11 = neutrino_couplings[0][0]
        self.neutrino.g12 = neutrino_couplings[0][1]
        self.neutrino.g13 = neutrino_couplings[0][2]

        self.neutrino.g21 = neutrino_couplings[1][0]
        self.neutrino.g22 = neutrino_couplings[1][1]
        self.neutrino.g23 = neutrino_couplings[1][2]

    def calculate_dependent_variables(self):
        self.calculate_higgs_mass()
        self.calculate_scalar_masses_and_mixings()
        self.calculate_fermion_masses_and_mixings()
        self.calculate_neutrino_masses_mixings_and_couplings()


if __name__ == "__main__":
    higgs_creator = Particle.ParticleCreator(Higgs.Higgs, "configs/higgs.json")
    higgsDummy = higgs_creator.create()

    scalar_creator = Particle.ParticleCreator(Scalar.Scalar, "configs/scalar.json")
    scalarDummy = scalar_creator.create()

    fermion_creator = Particle.ParticleCreator(Fermion.Fermion, "configs/fermion.json")
    fermionDummy = fermion_creator.create()

    neutrino_creator = Particle.ParticleCreator(NeutrinoMasses.Neutrino, "configs/neutrino_masses.json")
    neutrinoDummy = neutrino_creator.create()

    model = ModelT12A(higgsDummy, fermionDummy, scalarDummy, neutrinoDummy)

    model.calculate_dependent_variables()

    print("Neutrino")
    model.neutrino_dependent.pprint()



