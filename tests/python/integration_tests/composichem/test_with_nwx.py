# Copyright 2024 Richard Group
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
        basis = 'aug-cc-pvdz'
        self.mm.change_input(key, 'basis set', basis)
        egy = self.mm.run_as(TotalEnergy(), key, mol)
        print(f"Basis set: {basis}, Calculated Energy (egy): {egy}")

    def setUp(self):
        self.mm = ModuleManager()
        nwx.load_modules(self.mm)
