from typing import List
from pybrownomics.base.schema import Simulation, create_simulation, create_series
from pybrownomics.base.simulation import BaseTokenSimulation
from pybrownomics.control.src.token_dynamics import (
    ConsumerBehavior,
    TokenPriceEvolution,
)
from pybrownomics.control.src.token_economy import TokenEconomy
from pybrownomics.control.src.game import StackelbergGame
import matplotlib.pyplot as plt


class TokenSimulation(BaseTokenSimulation):
    def __init__(
        self, initial_state, economy: TokenEconomy, time_horizon, n_simulations
    ):
        self.current_state = initial_state
        self.economy = economy
        self.time_horizon = time_horizon
        self.n_simulations = n_simulations

    def _generate_metadata(self, states: List[float]) -> Simulation:
        series = create_series(
            name="Token price", description="Token price over time", series=states
        )
        return create_simulation(
            name="Token price simulation",
            description="Token price simulation using optimal control theory",
            series=[series],
        )

    def run_simulation(self) -> List[Simulation]:
        simulations = []
        for _ in range(self.n_simulations):
            states_over_time = [self.current_state]
            for _ in range(self.time_horizon):
                ut = self.economy.game.solve_moderator(self.current_state)
                xt_next = self.economy.dynamic.step(ut)
                states_over_time.append(xt_next)
                self.current_state = xt_next
            simulations.append(self._generate_metadata(states_over_time))
        return simulations


def run_simulation(
    initial_state: float = 100,
    time_horizon: int = 365,
    p_tok_t: float = 10.0,
    s_t: int = 1_000_000,
    gamma: float = 0.9,
    expected_future_price: float = 11.0,
    initial_population: int = 100,
    adoption_rate: float = 0.1,
    n_simulations: int = 1,
) -> List[Simulation]:
    """Run the simulation."""
    token_price_evolution = TokenPriceEvolution(initial_price=10, volatility=5)

    consumer_behavior = ConsumerBehavior(
        initial_population=initial_population, adoption_rate=adoption_rate
    )

    stackelberg_game = StackelbergGame(
        p_tok_t=p_tok_t,
        s_t=s_t,
        gamma=gamma,
        expected_future_price=expected_future_price,
    )

    economy = TokenEconomy(
        dynamic=token_price_evolution,
        consumer_behavior=consumer_behavior,
        game=stackelberg_game,
    )
    simulation = TokenSimulation(
        initial_state=initial_state,
        economy=economy,
        time_horizon=time_horizon,
        n_simulations=n_simulations,
    )

    # Run the simulation
    return simulation.run_simulation()
