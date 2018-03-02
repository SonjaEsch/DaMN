import ModelT12ANeutrinoCouplings
import Particle
import Higgs
import Scalar
import Fermion
import NeutrinoCouplings


higgs_creator = Particle.ParticleCreator(Higgs.Higgs, "configs/higgs_test.json")
higgs = higgs_creator.create()

scalar_creator = Particle.ParticleCreator(Scalar.Scalar, "configs/scalar_test.json")
scalar = scalar_creator.create()

fermion_creator = Particle.ParticleCreator(Fermion.Fermion, "configs/fermion_test.json")
fermion = fermion_creator.create()

neutrino_creator = Particle.ParticleCreator(NeutrinoCouplings.Neutrino, "configs/neutrino_couplings_test.json")
neutrino = neutrino_creator.create()

model = ModelT12ANeutrinoCouplings.ModelT12A(higgs, fermion, scalar, neutrino)

model.calculate_dependent_variables()

model.pprint()
