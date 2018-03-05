import Fermion
import Higgs
import ModelT12ANeutrinoCouplings
import NeutrinoCouplings
import Particle
import Scalar

import os
import subprocess
import pyslha


class ModelSPheno(ModelT12ANeutrinoCouplings.ModelT12A):
    input_slha_template_path = "SPhenoInputTemplate.slha"
    input_slha_template_data = None

    input_slha_parameter_path = "/tmp/{}-sphenoInput.slha".format(os.getpid())
    spheno_executable_path = "./SPhenoT12aTest"
    spheno_output_file_path = "/tmp/{}-sphenoOutput.slha".format(os.getpid())

    def __init__(
            self,
            higgs,
            fermion,
            scalar,
            neutrino,
            calculate_branching_ratios=True,
            calculate_one_loop_masses=True
            ):

        super().__init__(higgs, fermion, scalar, neutrino)

        self.calculate_branching_ratios = calculate_branching_ratios
        self.calculate_one_loop_masses = calculate_one_loop_masses

        if self.input_slha_template_data is None:
            with open(self.input_slha_template_path, "r") as f:
                self.input_slha_template_data = f.read()

    def write_slha_file(self):
        parameter_dict = {
            "branching_ratios": int(self.calculate_branching_ratios),
            "one_loop_masses": int(self.calculate_one_loop_masses),
            
            "lambda_higgs": self.higgs.lambda_higgs,
            "vev": self.higgs.vev,

            "g11": self.neutrino.g11,
            "g12": self.neutrino.g12,
            "g13": self.neutrino.g13,
            "g21": self.neutrino.g21,
            "g22": self.neutrino.g22,
            "g23": self.neutrino.g23,

            "fermion_mass_doublet": self.fermion.mass_doublet,
            "fermion_mass_singlet": self.fermion.mass_singlet,
            "y1": self.fermion.y1,
            "y2": self.fermion.y2,

            "A": self.scalar.A,
            "lambda_D": self.scalar.lambda_D,
            "lambda_P": self.scalar.lambda_P,
            "lambda_PP": self.scalar.lambda_PP,
            "lambda_S": self.scalar.lambda_S,
            "scalar_mass_doublet_squared": self.scalar.mass_doublet ** 2,
            "scalar_mass_singlet_squared": self.scalar.mass_singlet ** 2
        }

        with open(self.input_slha_parameter_path, "w") as f:
            f.write(self.input_slha_template_data.format(**parameter_dict))

    def run_spheno(self):
        subprocess.call([self.spheno_executable_path, self.input_slha_parameter_path, self.spheno_output_file_path],
                        stdout=open(os.devnull, 'wb'))

    def read_spheno_output(self):
        data = pyslha.read(self.spheno_output_file_path)
        self.set_higgs_dependent_variables(data)
        self.set_fermion_dependent_variables(data)
        self.set_scalar_dependent_variables(data)
        self.set_neutrino_dependent_variables(data)

    def set_higgs_dependent_variables(self, data):
        self.higgs_dependent.mass_eigenstates = [data.blocks["MASS"][25]]

        if self.higgs_dependent.mass_eigenstates[0] == 0.0:
            raise ValueError

    def set_fermion_dependent_variables(self, data):
        self.fermion_dependent.mass_eigenstates = [
            data.blocks["MASS"][1000],
            data.blocks["MASS"][1001],
            data.blocks["MASS"][1002]
        ]

        if (self.fermion_dependent.mass_eigenstates[0] == 0.0 or
            self.fermion_dependent.mass_eigenstates[1] == 0.0 or
            self.fermion_dependent.mass_eigenstates[2] == 0.0
        ):
            raise ValueError

        self.fermion_dependent.mixing_matrix = [[data.blocks["ETA"][i, j] for i in range(1, 4)] for j in range(1, 4)]

    def set_scalar_dependent_variables(self, data):
        self.scalar_dependent.mass_eigenstates = [
            data.blocks["MASS"][1005],
            data.blocks["MASS"][10015],
            data.blocks["MASS"][1004]
        ]

        if (self.scalar_dependent.mass_eigenstates[0] == 0.0 or
            self.scalar_dependent.mass_eigenstates[1] == 0.0 or
            self.scalar_dependent.mass_eigenstates[2] == 0.0
        ):
            raise ValueError

        self.scalar_dependent.mixing_matrix = [[data.blocks["ETB"][i, j] for i in range(1, 4)] for j in range(1, 4)]

    def set_neutrino_dependent_variables(self, data):
        self.neutrino_dependent.mass_eigenstates = [
            data.blocks["MASS"][12],
            data.blocks["MASS"][14],
            data.blocks["MASS"][16]
        ]

        self.neutrino_dependent.mixing_matrix = [[data.blocks["UN"][i, j] for i in range(1, 4)] for j in range(1, 4)]

    def calculate_dependent_variables(self):
        self.write_slha_file()
        self.run_spheno()
        self.read_spheno_output()


if __name__ == "__main__":
    higgs_creator = Particle.ParticleCreator(Higgs.Higgs, "configs/higgs.json")
    higgsDummy = higgs_creator.create()

    scalar_creator = Particle.ParticleCreator(Scalar.Scalar, "configs/scalar.json")
    scalarDummy = scalar_creator.create()

    fermion_creator = Particle.ParticleCreator(Fermion.Fermion, "configs/fermion.json")
    fermionDummy = fermion_creator.create()

    neutrino_creator = Particle.ParticleCreator(NeutrinoCouplings.Neutrino, "configs/neutrino_couplings.json")
    neutrinoDummy = neutrino_creator.create()

    model = ModelSPheno(higgsDummy, fermionDummy, scalarDummy, neutrinoDummy)

    model.calculate_dependent_variables()

    model.pprint()
