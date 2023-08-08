import numpy as np
from scipy.optimize import minimize


class StackelbergGame:
    def __init__(self, p_tok_t, s_t, gamma, expected_future_price):
        self.p_tok_t = p_tok_t
        self.s_t = s_t
        self.gamma = gamma
        self.expected_future_price = expected_future_price

    # Define Player 2's utility function
    def player2_utility(self, alpha_t, delta_p_t):
        return (
            alpha_t * self.s_t * (self.p_tok_t + delta_p_t)
            + (1 - alpha_t) * self.gamma * self.s_t * self.expected_future_price
        )

    # Gradient of the utility function w.r.t. alpha_t
    def player2_utility_gradient(self, alpha_t, delta_p_t):
        return (
            self.s_t * (self.p_tok_t + delta_p_t)
            - self.gamma * self.s_t * self.expected_future_price
        )

    # Solve Player 2's optimization problem
    def solve_player2(self, delta_p_t):
        result = minimize(
            lambda alpha_t: -self.player2_utility(
                alpha_t, delta_p_t
            ),  # We minimize the negative utility to maximize the actual utility
            0.5,  # initial guess for alpha_t
            bounds=[(0, 1)],  # alpha_t is between 0 and 1
            jac=lambda alpha_t: -self.player2_utility_gradient(
                alpha_t, delta_p_t
            ),  # negative gradient
        )
        return result.x[0]  # Return the optimal alpha_t

    # Player 1's objective
    def player1_objective(self, delta_p_t, desired_supply):
        alpha_t_optimal = self.solve_player2(delta_p_t)
        actual_supply_after_buyback = self.s_t - alpha_t_optimal * self.s_t * (
            self.p_tok_t + delta_p_t
        )
        return (
            actual_supply_after_buyback - desired_supply
        ) ** 2  # Squared difference as objective

    # Solve Player 1's optimization problem
    def solve_player1(self, desired_supply):
        result = minimize(
            lambda delta_p_t: self.player1_objective(delta_p_t[0], desired_supply),
            0,  # initial guess for delta_p_t
            bounds=[(0, None)],  # delta_p_t is non-negative
        )
        return result.x[0]  # Return the optimal delta_p_t


if __name__ == "__main__":
    # Example:
    game = StackelbergGame(p_tok_t=10, s_t=1000, gamma=0.9, expected_future_price=11)
    optimal_delta_p_t = game.solve_player1(desired_supply=900)
    print(f"Optimal pricing strategy for Player 1: {optimal_delta_p_t}")
