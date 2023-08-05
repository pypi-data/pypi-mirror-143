# Copyright (c) 2021, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide an abstract chemical species repository class interface."""


from abc import ABC, abstractmethod
from typing import FrozenSet

from .chemical_species import ChemicalSpecies


class AbstractChemicalSpeciesRepository(ABC):
    """Define the abstract interface for a chemical species repository."""

    def __init__(self, **kwargs) -> None:
        """Initialize the base."""
        super().__init__(**kwargs)

    @abstractmethod
    def find_by_inchikey(self, inchikey: str) -> ChemicalSpecies:
        """Find a chemical species in the repository by its InChIKey."""

    @abstractmethod
    def get_inchikeys(self) -> FrozenSet[str]:
        """Return InChIKeys that already exist in the repository."""

    @abstractmethod
    def add(self, chemical_species: ChemicalSpecies) -> None:
        """Add a chemical species to the repository."""

    @abstractmethod
    def remove(self, chemical_species: ChemicalSpecies) -> None:
        """Remove a chemical species from the repository."""

    @abstractmethod
    def log_summary(self) -> None:
        """Log a comprehensive summary of the repository in implementing classes."""
