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
        """Declare an input for the module (e.g., 'basis_set')."""
        self.inputs[name] = None  # Initialize with None, you can update this later

    def declare_output(self, name):
        """Declare an output for the module (e.g., 'energy')."""
        self.outputs[name] = None  # Initialize with None

    def run(self):
        """Fetch the energy for the given basis set."""
        basis_set = self.inputs.get("basis_set")  # Retrieve the input basis set

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


# Example Usage
if __name__ == "__main__":
    # Create the AOEnergyModule instance
    module = AOEnergyModule()
    
    # Declare input and output
    module.declare_input("basis_set")
    module.declare_output("energy")
    
    # Set the input basis set
    module.inputs["basis_set"] = "aug-cc-pvdz"
    
    # Run the module to compute the energy
    module.run()
    
    # Retrieve and print the output energy
    energy = module.get_output()
    print(f"Energy for basis set 'aug-cc-pvdz': {energy}")
