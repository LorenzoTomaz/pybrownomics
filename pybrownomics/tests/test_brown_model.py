from pybrownomics import run_brown_simulation


def test_run_optimal_control_simulation():
    simulations = run_brown_simulation(period=2)
    simulation = simulations[0]
    series = simulation["series"][0]["series"]
    assert simulation["name"] == "Token price simulation"
    assert len(series) == 2


def test_run_optimal_control_simulation_n_simulations():
    simulations = run_brown_simulation(period=2, n_simulations=2)
    assert len(simulations) == 2
    assert len(simulations[0]["series"][0]["series"]) == 2
    assert len(simulations[1]["series"][0]["series"]) == 2
