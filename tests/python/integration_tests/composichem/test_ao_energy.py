#Importing necessary modules 
from chemist.basis_set import AOBasisSetF, AOBasisSetD
from chemist.basis_set import AtomicBasisSetF, AtomicBasisSetD
from chemist.basis_set import ShellF, ShellD
from chemist.basis_set import ContractedGaussianF, ContractedGaussianD
from chemist.basis_set import PrimitiveF, PrimitiveD
from chemist import PointF, PointD
from chemist import ShellType
# Placeholder imports (Ensure these are defined in your environment)

from pluginplay import ModuleManager
import nwchemex as nwx
from chemist import Atom, Molecule, ChemicalSystem
from simde import TotalEnergy
import unittest


class AOEnergyModule:
    """Module to return precomputed AO energy based on the provided basis set."""
    
    def __init__(self):
        # Declare the module's input and output
        print("[AOEnergyModule] Initializing module...")
        self.inputs = {}    
        self.outputs = {}

    def declare_input(self, name):
        """Declare an input for the module."""
        print(f"[AOEnergyModule] Declaring input: {name}")
        self.inputs[name] = None  # Initialize with None, you can update this later

    def declare_output(self, name):
        """Declare an output for the module."""
        print(f"[AOEnergyModule] Declaring output: {name}")
        self.outputs[name] = None  # Initialize with None

    def run(self):
        """Fetch the energy for the given basis set."""
        print("[AOEnergyModule] Running module...")
        
        basis_set = self.inputs.get("basis_set")  # Retrieve the input basis set

        if not basis_set:
            print("[AOEnergyModule] Error: Basis set is not provided.")
            raise ValueError("Basis set is not provided.")
        
        print(f"[AOEnergyModule] Basis set provided: {basis_set}")
        
        # Simple dictionary to look up precomputed energy values
        energy_dict = {
            "aug-cc-pvdz": -1.117990008492,
            "aug-cc-pvtz": -1.120288703906,
            "aug-cc-pvqz": -1.120632483879
        }

        # Check if the basis set name is in the dictionary
        if basis_set in energy_dict:
            self.outputs["energy"] = energy_dict[basis_set]
            print(f"[AOEnergyModule] Energy for '{basis_set}': {self.outputs['energy']}")
        else:
            print(f"[AOEnergyModule] Error: Unknown basis set '{basis_set}'")
            raise ValueError(f"Unknown basis set: {basis_set}")

    def get_output(self):
        """Retrieve the output energy."""
        print(f"[AOEnergyModule] Retrieving output: {self.outputs.get('energy')}")
        return self.outputs.get("energy")
    
def make_h2():
    """Creates simple hydrogen molecule for tsting"""
    print("[make_h2] Creating H2 molecule placeholder...")
    return "H2 molecule placeholder"

# ------------------ Unit Tests ------------------

class TestAOEnergyModule(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        print("\n[TestAOEnergyModule] Setting up module for testing...")
        self.module = AOEnergyModule()
        self.module.declare_input("basis_set")
        self.module.declare_output("energy")

    def test_valid_basis_set(self):
        """Test energy calculation for a valid basis set."""
        print("[TestAOEnergyModule] Testing valid basis set...")
        self.module.inputs["basis_set"] = "aug-cc-pvdz"
        self.module.run()
        energy = self.module.get_output()
        print(f"[TestAOEnergyModule] Energy obtained: {energy}")
        self.assertAlmostEqual(energy, -1.117990008492, places=6)

    def test_invalid_basis_set(self):
        """Test error on invalid basis set."""
        print("[TestAOEnergyModule] Testing invalid basis set...")
        self.module.inputs["basis_set"] = "invalid-set"
        with self.assertRaises(ValueError):
            self.module.run()

    def test_missing_basis_set(self):
        """Test error when basis set is not provided."""
        print("[TestAOEnergyModule] Testing missing basis set...")
        with self.assertRaises(ValueError):
            self.module.run()


# Example 
if __name__ == "__main__":
    # Create a ModuleManager instance
    print("[Main] Starting AO Energy Module Example...")
    mm = ModuleManager()
    print("[Main] ModuleManager created.")

    #load necessary modules into it
    nwx.load_modules(mm)
    print("[Main] Modules loaded into ModuleManager.")

    #Add the AOEnergyModule to it
    mm.add_module(AOEnergyModule(), 'My Module')
    print("[Main] AOEnergyModule added to ModuleManager as 'My Module'.")

    #create a test molecule 
    mol = make_h2()
    print(f"[Main] Test molecule created: {mol}")
    
    # Run MolecularBasisSet to get the basis set object
    print("[Main] Running AOBasisSetF to get basis set object...")
    basis = mm.run_as(AOBasisSetF(), 'aug-cc-pvdz', mol)

    # Run the AOEnergyModule to get the energy
    print("[Main] Running AOEnergyModule to calculate energy...")
    energy = mm.run_as(AOEnergyModule(), 'My Module', basis, mol)

    # Print the energy output
    print("[Main] AO Energy Module Output:")
    print(f"Energy for basis set 'aug-cc-pvdz': {energy}")

    # Run unit tests
    print("[Main] Running unit tests...")
    unittest.main()
   