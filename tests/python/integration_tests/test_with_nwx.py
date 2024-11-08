import sys
import os

# Add pluginplay to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../../pluginplay')))

from pluginplay import ModuleManager
import nwchemex as nwx
from chemist import Atom, Molecule, ChemicalSystem
from simde import TotalEnergy
import unittest


def make_h2():
    mol = Molecule()
    mol.push_back(Atom('H', 1, 1837.15264648179, 0.0, 0.0, 0.0))
    mol.push_back(Atom('H', 1, 1837.15264648179, 0.0, 0.0, 1.68185))

    return ChemicalSystem(mol)


class TestWithNWChemEx(unittest.TestCase):

    def test_scf(self):
        mol = make_h2()
        key = 'NWChem : SCF'

         # Define the basis sets you want to test
        basis_sets = ['aug-cc-pvdz', 'aug-cc-pvtz', 'aug-cc-pvqz']
        expected_energies = {
            'aug-cc-pvdz': -1.094184522864,  # Replace with actual expected values if known
            'aug-cc-pvtz': -1.1,             # Placeholder value; replace with actual expected values
            'aug-cc-pvqz': -1.105            # Placeholder value; replace with actual expected values
        }

        print('hi')

        for basis in basis_sets:
            with self.subTest(basis=basis):
                self.mm.change_input(key, 'basis set', basis)
                egy = self.mm.run_as(TotalEnergy(), key, mol)
                print(f"Basis set: {basis}, Calculated Energy (egy): {egy}")
                
                # If you have expected values, use them to validate the result
                self.assertAlmostEqual(egy, expected_energies[basis], places=5)    

        # self.mm.change_input(key, 'basis set', 'aug-cc-pvdz')
        # egy = self.mm.run_as(TotalEnergy(), key, mol)
        # self.assertAlmostEqual(egy, -1.094184522864, places=5)
       
    def setUp(self):
        self.mm = ModuleManager()
        nwx.load_modules(self.mm)
