import numpy as np

from pybrownomics.control.src.game import StackelbergGame
from pybrownomics.control.src.token_dynamics import (
    TokenPriceEvolution,
    ConsumerBehavior,
)


class TokenEconomy:
    def __init__(
        self,
        dynamic: TokenPriceEvolution,
        consumer_behavior: ConsumerBehavior,
        game: StackelbergGame,
        initial_values=None,
    ):
        # Default initial values
        self.default_initial_values = {
            "St": 1000,  # Initial token supply
            "RUSD_t": 10000,  # Initial dollar reserve
            "RTok_t": 5000,  # Initial token reserve
            "pTok_t": 10,  # Initial token price
        }
        self.dynamic = dynamic
        self.game = game
        self.consumer_behavior = consumer_behavior
        # If user provides initial values, override defaults
        if initial_values:
            for key, value in initial_values.items():
                if key in self.default_initial_values:
                    self.default_initial_values[key] = value

        self.St = self.default_initial_values["St"]
        self.RUSD_t = self.default_initial_values["RUSD_t"]
        self.RTok_t = self.default_initial_values["RTok_t"]
        self.pTok_t = self.default_initial_values["pTok_t"]

    def dynamics(self, xt, ut, st):
        # Unpack the state and control variables for clarity
        St, RUSD_t, RTok_t, pTok_t = xt
        uB_t, uP_t, delta_p = ut

        # Define the system dynamics using equations from the paper
        next_St = St + uB_t - uB_t / (pTok_t + delta_p)
        next_RUSD_t = RUSD_t + st[1] - uB_t
        next_RTok_t = RTok_t + uB_t / (pTok_t + delta_p) - uP_t
        next_pTok_t = st[0] / next_St

        # Update the state variables
        self.St = next_St
        self.RUSD_t = next_RUSD_t
        self.RTok_t = next_RTok_t
        self.pTok_t = next_pTok_t

        return [next_St, next_RUSD_t, next_RTok_t, next_pTok_t]

    def cost(self, xt, ut, x_ref, u_ref, beta):
        return (
            beta[0] * (xt[3] - x_ref[3]) ** 2
            + beta[1] * (ut[0] - u_ref[0]) ** 2
            + beta[2] * (ut[1] - u_ref[1]) ** 2
        )


if __name__ == "__main__":
    # Initialize the token economy system
    token_system = TokenEconomy()

    # Initial state and control values
    # These are just sample values, you'd want to initialize these based on your actual starting conditions
    xt_initial = np.array([1000, 5000, 2000, 50])  # St, RUSD_t, RTok_t, pTok_t
    ut_initial = np.array([100, 50, 5])  # uB_t, uP_t, Δp_t

    # Reference state and control values
    # These would typically be derived from your desired steady state or other target conditions
    x_ref = np.array([1200, 5200, 2100, 55])
    u_ref = np.array([110, 60, 6])

    # Beta values as weights for the cost function
    beta = np.array([0.5, 0.3, 0.2])

    # Forecast values (as an example)
    st = np.array([110, 55])

    # Calculate the next state using the system dynamics
    xt_next = token_system.dynamics(xt_initial, ut_initial, st)

    # Calculate the associated cost
    cost_value = token_system.cost(xt_next, ut_initial, x_ref, u_ref, beta)

    # Display the results
    print(f"Initial State: {xt_initial}")
    print(f"Control Input: {ut_initial}")
    print(f"Next State: {xt_next}")
    print(f"Associated Cost: {cost_value}")
