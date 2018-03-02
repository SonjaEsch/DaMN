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

print(higgs)
print(scalar)
print(fermion)
print(neutrino)

model = ModelT12ANeutrinoCouplings.ModelT12A(higgs, fermion, scalar, neutrino)

print("Model parameters")
print(higgs)
print(scalar)
print(fermion)
print(neutrino)


model.calculate_dependent_variables()

print("Higgs")
model.higgs_dependent.pprint()

print("Scalar")
model.scalar_dependent.pprint()

print("Fermion")
model.fermion_dependent.pprint()

print("Neutrino")
model.neutrino_dependent.pprint()
