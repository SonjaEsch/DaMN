import Fermion
import Higgs
import ModelT12ANeutrinoCouplings
import NeutrinoCouplings
import Particle
import Scalar


class ModelSPheno(ModelT12ANeutrinoCouplings.ModelT12A):
    input_slha_template_path = "SPhenoInputTemplate.slha"
    input_slha_template_data = None

    input_slha_parameter_path = "/tmp/sphenoInput.slha"

    def __init__(self, higgs, fermion, scalar, neutrino):
        super().__init__(higgs, fermion, scalar, neutrino)

        if self.input_slha_template_data is None:
            with open(self.input_slha_template_path, "r") as f:
                self.input_slha_template_data = f.read()

    def write_slha_file(self):
        parameter_dict = {
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

    def calculate_dependent_variables(self):
        self.write_slha_file()


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
