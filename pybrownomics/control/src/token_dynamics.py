import numpy as np


class TokenPriceEvolution:
    def __init__(self, initial_price, volatility, trend_rate=0):
        """
        Initialize the token price dynamics.
        :param initial_price: Starting price of the token.
        :param volatility: Standard deviation of the price change.
        :param trend_rate: Rate at which price is trending upwards (positive) or downwards (negative).
        """
        self.price = initial_price
        self.volatility = volatility
        self.trend_rate = trend_rate

    def step(self, dt) -> float:
        """
        Simulate the token price for a time step dt.
        """
        random_change = np.random.randn() * self.volatility
        trend_change = self.trend_rate * dt
        self.price += random_change + trend_change
        return self.price


class ConsumerBehavior:
    def __init__(self, initial_population, adoption_rate):
        """
        Initialize consumer behavior dynamics.
        :param initial_population: Number of consumers at the start.
        :param adoption_rate: Rate at which new consumers adopt the token.
        """
        self.population = initial_population
        self.adoption_rate = adoption_rate

    def step(self, dt, token_price) -> float:
        """
        Simulate the change in consumer population for a time step dt,
        possibly based on the current token price.
        """
        # Here, we assume that adoption rate is inversely proportional to token price.
        change = self.adoption_rate / (1 + token_price) * dt
        self.population += change
        return self.population


# Example of how to use the library:


def simulate_dynamics(T, dt):
    # Initialize dynamics
    token_price_dynamics = TokenPriceEvolution(
        initial_price=100, volatility=5, trend_rate=0.01
    )
    consumer_dynamics = ConsumerBehavior(initial_population=1000, adoption_rate=50)

    time_steps = np.arange(0, T, dt)
    token_prices = []
    consumer_populations = []

    for t in time_steps:
        token_prices.append(token_price_dynamics.step(dt))
        consumer_populations.append(
            consumer_dynamics.step(dt, token_price_dynamics.price)
        )

    return time_steps, token_prices, consumer_populations


if __name__ == "__main__":
    T, dt = 10, 0.1
    time_steps, token_prices, consumer_populations = simulate_dynamics(T, dt)

    # Here, you can plot or analyze the results as needed.
