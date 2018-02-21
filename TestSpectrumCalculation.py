import ModelT12ANeutrinoCouplings
import Particle
import Higgs
import Scalar
import Fermion
import NeutrinoCouplings


higgs_creator = Higgs.HiggsCreator("higgs_test.json")
higgs = higgs_creator.create()

scalar_creator = Particle.ParticleCreator(Scalar.Scalar, "scalar_test.json")
scalar = scalar_creator.create()

fermion_creator = Particle.ParticleCreator(Fermion.Fermion, "fermion_test.json")
fermion = fermion_creator.create()

neutrino_creator = Particle.ParticleCreator(NeutrinoCouplings.Neutrino, "neutrino_couplings_test.json")
neutrino = neutrino_creator.create()

print(higgs)
print(scalar)
print(fermion)
print(neutrino)

model = ModelT12ANeutrinoCouplings.ModelT12A(higgs, fermion, scalar, neutrino)

model.calculate_dependent_variables()

print(model)

