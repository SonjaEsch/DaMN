import Fermion
import Higgs
import ModelT12ANeutrinoCouplings
import ModelSPheno
import NeutrinoCouplings
import Particle
import Scalar

if __name__ == "__main__":
    higgs_creator = Particle.ParticleCreator(Higgs.Higgs, "configs/higgs.json")
    higgsDummy = higgs_creator.create()

    scalar_creator = Particle.ParticleCreator(Scalar.Scalar, "configs/scalar.json")
    scalarDummy = scalar_creator.create()

    fermion_creator = Particle.ParticleCreator(Fermion.Fermion, "configs/fermion.json")
    fermionDummy = fermion_creator.create()

    neutrino_creator = Particle.ParticleCreator(NeutrinoCouplings.Neutrino, "configs/neutrino_couplings.json")
    neutrinoDummy = neutrino_creator.create()

    model = ModelT12ANeutrinoCouplings.ModelT12A(higgsDummy, fermionDummy, scalarDummy, neutrinoDummy)
    model.calculate_dependent_variables()

    modelSPheno = ModelSPheno.ModelSPheno(higgsDummy, fermionDummy, scalarDummy, neutrinoDummy, False, False)
    modelSPheno.calculate_dependent_variables()

    print(model.scalar_dependent.mass_eigenstates)
    print(modelSPheno.scalar_dependent.mass_eigenstates)
