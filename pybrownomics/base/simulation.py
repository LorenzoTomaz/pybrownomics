from abc import ABC, abstractmethod
from typing import List, Union

from pybrownomics.base.schema import Simulation


class BaseTokenSimulation(ABC):
    @abstractmethod
    def run_simulation(self) -> List[Simulation]:
        pass
