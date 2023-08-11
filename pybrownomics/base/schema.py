from typing import TypedDict, Union
import numpy as np


class Series(TypedDict):
    """Timeseries schema."""

    name: str
    description: str
    series: list[float]


class Simulation(TypedDict):
    """Simulation schema."""

    name: str
    description: str
    series: list[Series]


def create_series(
    name: str, description: str, series: Union[list[float], np.ndarray]
) -> Series:
    """Create a series object."""
    return Series(name=name, description=description, series=list(series))


def create_simulation(name: str, description: str, series: list[Series]) -> Simulation:
    """Create a simulation object."""
    return Simulation(name=name, description=description, series=series)
