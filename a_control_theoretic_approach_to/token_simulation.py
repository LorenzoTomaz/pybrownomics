from src.token_dynamics import ConsumerBehavior, TokenPriceEvolution
from src.token_economy import TokenEconomy
from src.game import StackelbergGame
import matplotlib.pyplot as plt


class TokenSimulation:
    def __init__(self, initial_state, economy: TokenEconomy, time_horizon):
        self.current_state = initial_state
        self.economy = economy
        self.time_horizon = time_horizon

    def run_simulation(self):
        states_over_time = [self.current_state]

        for _ in range(self.time_horizon):
            ut = self.economy.game.solve_player1(self.current_state)
            xt_next = self.economy.dynamic.step(ut)
            states_over_time.append(xt_next)
            self.current_state = xt_next

        return states_over_time


if __name__ == "__main__":
    token_price_evolution = TokenPriceEvolution(initial_price=10, volatility=5)
    initial_population = 100  # price at which consumers start selling
    adoption_rate = 0.1  # price at which consumers start buying

    consumer_behavior = ConsumerBehavior(
        initial_population=initial_population, adoption_rate=adoption_rate
    )
    p_tok_t_default = 10.0
    s_t_default = 1_000_000
    gamma_default = 0.9
    expected_future_price_default = 11.0

    stackelberg_game = StackelbergGame(
        p_tok_t=p_tok_t_default,
        s_t=s_t_default,
        gamma=gamma_default,
        expected_future_price=expected_future_price_default,
    )

    economy = TokenEconomy(
        dynamic=token_price_evolution,
        consumer_behavior=consumer_behavior,
        game=stackelberg_game,
    )
    initial_state = 100  # example initial state
    time_horizon = 365
    simulation = TokenSimulation(
        initial_state=initial_state, economy=economy, time_horizon=time_horizon
    )

    # Run the simulation
    states_over_time = simulation.run_simulation()

    # Visualization (as previously shown):

    prices = [state for state in states_over_time]
    plt.plot(prices)
    plt.xlabel("Days")
    plt.ylabel("Token Price ($)")
    plt.show()
