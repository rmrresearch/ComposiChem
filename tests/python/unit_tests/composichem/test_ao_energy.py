#Importing necessary modules
from chemist.basis_set import AOBasisSetF, AOBasisSetD
from chemist.basis_set import AtomicBasisSetF, AtomicBasisSetD
from chemist.basis_set import ShellF, ShellD
from chemist.basis_set import ContractedGaussianF, ContractedGaussianD
from chemist.basis_set import PrimitiveF, PrimitiveD
from chemist import PointF, PointD
from chemist import ShellType
import unittest


class AOEnergyModule:
    """Module to return precomputed AO energy based on the provided basis set."""

    def __init__(self):
        # Declare the module's input and output
        self.inputs = {}
        self.outputs = {}

    def declare_input(self, name):
        """Declare an input for the module."""
        self.inputs[
            name] = None  # Initialize with None, you can update this later

    def declare_output(self, name):
        """Declare an output for the module."""
        self.outputs[name] = None  # Initialize with None

    def run(self):
        """Fetch the energy for the given basis set."""
        basis_set = self.inputs.get(
            "basis_set")  # Retrieve the input basis set

        if not basis_set:
            raise ValueError("Basis set is not provided.")

        # Simple dictionary to look up precomputed energy values
        energy_dict = {
            "aug-cc-pvdz": -1.117990008492,
            "aug-cc-pvtz": -1.120288703906,
            "aug-cc-pvqz": -1.120632483879
        }

        # Check if the basis set name is in the dictionary
        if basis_set in energy_dict:
            self.outputs["energy"] = energy_dict[basis_set]
        else:
            raise ValueError(f"Unknown basis set: {basis_set}")

    def get_output(self):
        """Retrieve the output energy."""
        return self.outputs.get("energy")


def make_h2():
    """Creates simple hydrogen molecule for tsting"""
    return "H2 molecule placeholder"


class TestAOEnergy(unitttest.TestCase):

    def test_ao_energy(self):
        # Create a ModuleManager instance
        mm = ModuleManager()

        #load necessary modules into it
        nwx.load_modules(mm)

        #Add the AOEnergyModule to it
        mm.add_module(AOEnergyModule(), 'My Module')

        #create a test molecule
        mol = make_h2()

        # Run MolecularBasisSet to get the basis set object
        basis = mm.run_as(AOBasisSetF(), 'aug-cc-pvdz', mol)

        # Run the AOEnergyModule to get the energy
        energy = mm.run_as(AOEnergyModule(), 'My Module', basis, mol)

        # Print the energy output
        print(f"Energy for basis set 'aug-cc-pvdz': {energy}")
