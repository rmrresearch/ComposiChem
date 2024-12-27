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

from pluginplay import ModuleManager, ModuleBase
import nwchemex as nwx
from chemist import Atom, Molecule, ChemicalSystem
from simde import AOEnergy, AOBasisSetF
import unittest


def make_h2():
    mol = Molecule()
    mol.push_back(Atom('H', 1, 1837.15264648179, 0.0, 0.0, 0.0))
    mol.push_back(Atom('H', 1, 1837.15264648179, 0.0, 0.0, 1.68185))

    return ChemicalSystem(mol)


def h2_energies(basis_name):
    energy_dict = {
        "aug-cc-pvdz": -1.117990008492,
        "aug-cc-pvtz": -1.120288703906,
        "aug-cc-pvqz": -1.120632483879
    }
    return energy_dict[basis_name]


class H2LambdaModule(ModuleBase):
    """
    Contains the hard-coded SCF energies for H2 molecule.
    """

    def __init__(self):
        ModuleBase.__init__(self)
        self.satisfies_property_type(AOEnergy())

    def run_(self, inputs, _):
        pt = AOEnergy()
        [aos, _] = pt.unwrap_inputs(inputs)

        basis_name = aos.at(
            0).basis_set_name()  # XXX: Assume same for all atoms

        rv = self.results()
        return pt.wrap_results(rv, h2_energies[basis_name])


class TestWithNWChemEx(unittest.TestCase):

    def test_scf(self):
        basis_name = 'aug-cc-pvdz'
        basis = self.mm.run_as(AOBasisSetF(), basis_name, self.h2)
        egy = self.mm.run_as(AOEnergy(), self.key, basis, self.h2)
        print(egy)
        self.assertAlmostEqual(egy, h2_energies(basis_name), places=6)

    def setUp(self):
        self.mm = ModuleManager()
        nwx.load_modules(self.mm)
        self.key = 'My lambda module'
        self.mm.add_module(H2LambdaModule(), self.key)
        self.h2 = make_h2()
