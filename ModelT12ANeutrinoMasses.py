import ModelT12ANeutrinoCouplings
import Particle
import Higgs
import Scalar
import Fermion
import NeutrinoMasses
import numpy as np
import math


# TODO catch all exceptions otherwise one could mess up a whole scan afterwards

class ModelT12A(ModelT12ANeutrinoCouplings.ModelT12A):

    def calculate_neutrino_dependent(self):

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

        co11, co12, co22 = self.get_neutrino_coefficients()
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

    model.pprint()



