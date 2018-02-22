import ModelT12ANeutrinoCouplings
import Particle
import Higgs
import Scalar
import Fermion
import NeutrinoCouplings
import pprint


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

print("Model parameters")
print(higgs)
print(scalar)
print(fermion)
print(neutrino)


model.calculate_dependent_variables()

pretty = pprint.PrettyPrinter(indent=3, depth=3)
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


