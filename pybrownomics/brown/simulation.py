from pybrownomics.base.schema import Simulation, create_series, create_simulation
from pybrownomics.base.simulation import BaseTokenSimulation
from pybrownomics.brown.src.simulator import Simulator
from typing import List
import numpy as np


class TokenSimulation(BaseTokenSimulation):
    def __init__(
        self,
        period: int = 365,
        agents: int = 1000,
        n_simulations: int = 1,
        beta: float = 0.3,
        chi: float = 1.0,
        interest_rate: float = 0.05,
        token_supply: float = 1000000000,
        price_mu: float = 0.03,
        productivity_initial_value: float = 100.0,
        productivity_mu: float = 0.02,
        productivity_sigma: float = 2.0,
        utility_mu: float = 1.0,
        utility_sigma: float = 10.0,
    ):
        self.df = {
            "period": period,
            "agents": agents,
            "n_simulations": n_simulations,
            "beta": beta,
            "chi": chi,
            "interest_rate": interest_rate,
            "token_supply": token_supply,
            "price": {"mu": price_mu},
            "productivity": {
                "initial_value": productivity_initial_value,
                "mu": productivity_mu,
                "sigma": productivity_sigma,
            },
            "utility": {"mu": utility_mu, "sigma": utility_sigma},
        }
        self.n_simulations = n_simulations

    def _generate_metadata(self, states: List[float]) -> Simulation:
        series = create_series(
            name="Token price", description="Token price over time", series=states
        )
        return create_simulation(
            name="Token price simulation",
            description="Token price simulation using geometric brownian motion",
            series=[series],
        )

    def run_simulation(self) -> List[Simulation]:
        period: int = self.df["period"]
        prices = np.zeros((self.n_simulations, period))
        simulations = []
        for i in range(0, self.n_simulations):
            sim = Simulator(self.df)
            # generate productivity
            sim.calc_productivity()
            # generate utility
            sim.calc_utility()

            # simulate price
            for t in range(0, period):
                sim.calc_userbase_and_threshold(t)
                sim.calc_aggregate_transaction_need(t)
                sim.calc_price(t)
            prices[i] = sim.price

            simulations.append(self._generate_metadata(states=sim.price))

        return simulations


def run_simulation(
    period: int = 365,
    agents: int = 1000,
    n_simulations: int = 1,
    beta: float = 0.3,
    chi: float = 1.0,
    interest_rate: float = 0.05,
    token_supply: float = 1000000000,
    price_mu: float = 0.03,
    productivity_initial_value: float = 100.0,
    productivity_mu: float = 0.02,
    productivity_sigma: float = 2.0,
    utility_mu: float = 1.0,
    utility_sigma: float = 10.0,
):
    """Run the simulation."""
    token_simulation = TokenSimulation(
        period=period,
        agents=agents,
        n_simulations=n_simulations,
        beta=beta,
        chi=chi,
        interest_rate=interest_rate,
        token_supply=token_supply,
        price_mu=price_mu,
        productivity_initial_value=productivity_initial_value,
        productivity_mu=productivity_mu,
        productivity_sigma=productivity_sigma,
        utility_mu=utility_mu,
        utility_sigma=utility_sigma,
    )
    return token_simulation.run_simulation()
