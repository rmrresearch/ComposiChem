#Importing necessary modules 
from chemist.basis_set import AOBasisSetF, AOBasisSetD
from chemist.basis_set import AtomicBasisSetF, AtomicBasisSetD
from chemist.basis_set import ShellF, ShellD
from chemist.basis_set import ContractedGaussianF, ContractedGaussianD
from chemist.basis_set import PrimitiveF, PrimitiveD
from chemist import PointF, PointD
from chemist import ShellType
import unittest

class AOEnergyModule(ModuleBase): #this module computes the AO energy given its basis set
    """"A module to compute AO Energy."""

    def __init__(self):
        super().__init__() #initialises the module by calling base class constructor
        self.declare_input("basis_set")
        self.declare_input("molecule")
        self.declare_output("energy")

    def run(self): 
        """"Executes the AOEnergy computation."""
        basis_set = self.inputs["basis_set"]  #get the inputs to the molecule 
        molecule = self.inputs["molecule"]

        #Computation of energy  
        energy = self._compute_energy(basis_set, molecule) #call a placeholder method to compute energy 
        self.outputs["energy"] = energy #store computed energy as output

    def _compute_energy(self, basis_set, molecule):
        """"Energy calculation."""
        energy = 0.0 

        #Iterate over all atomic centres and their shells 
        for center in basis_set.centers():
            if isinstance(center, AtomicBasisSetF):
                #For each atomic basis set
                for shell in center.shells():
                    #For each shell, we calculate its contributiosn based on primitive and other factors
                    energy += self.calculate_shell_energy(shell)

        #Add contributions from molecular geometry (positions and charges)
        for atom in molecule.atoms():
            position = atom.position
            charge = atom.charge
            #To add potential energy calculations here 
            energy+= charge * sum(position)

        return energy

    def _calculate_shell_energy(self, shell):
        """"Calculate energy contribution from given shell."""
        #Simple calculations based on shell properties?
        energy_contrib = 0.0
        for primitive in shell:
            #integrate over primitives in shell
            energy_contrib += primitive.coefficient * primitive.exponent
        return energy_contrib

class TestAOEnergyModule(unittest.TestCase):
    """"Unit tests for the AOEnergyModule."""

    def setUp(self):
        self.molecule = Molecule("H2O", [
            (0.0,0.0,0.0), #oxygen
            (0.0,0.0,1.0), #hydrogen 1
            (1.0,0.0,0.0)  #hydrogen 2
        ]) 
        #create a molecule object for testing (water molecule with 3 atoms)
        self.basis_set = AOBasisSetF() # create a specific type of basis set 
        o_point = PointF(0.0, 0.0, 0.0)
        h1_point = PointF(0.0,0.0,1.0)
        h2_point = PointF(1.0,0.0,0.0)
        #add atomic basic sets
        self.basis_set.add_center(AtomicBasisSetF("aug-cc-pvdz",8,o_point, [
            ShellF(l_value=0, is_pure=True),
            ShellF(l_value=1, is_pure=False)
        ])) 
        self.basis_set.add_center(AtomicBasisSetF("aug-cc-pvdz",1,h1_point, [
            ShellF(l_value=0, is_pure=True),
        ]))
        self.basis_set.add_center(AtomicBasisSetF("aug-cc-pvdz",1,h2_point, [
            ShellF(l_value=0, is_pure=True),
        ]))

        self.module = AOEnergyModule() #initialize the AOEnergyModule
        self.module.inputs["basis_set"] = self.basis_set #inputs for modules
        self.module.inputs["molecule"] = self.molecule

    def test_ao_energy(self):
        """Test energy computation."""
        self.module.run() #Run the module (this shld compute the energy)
        energy = self.module.outputs["energy"] #get energy from modules output
        expected_energy = -1.117990008492
        self.assertEqual(energy, expected_energy) #check is computed energy matches expected energy

if __name__ == "__main__": #run the tests when script is executed 
    unittest.main()