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
        self.mm.change_input(key, 'basis set', 'sto-3g')
        egy = self.mm.run_as(TotalEnergy(), key, mol)
        self.assertAlmostEqual(egy, -1.094184522864, places=5)

    def setUp(self):
        self.mm = ModuleManager()
        nwx.load_modules(self.mm)
