from pybrownomics import run_optimal_control_simulation


def test_run_optimal_control_simulation():
    simulations = run_optimal_control_simulation()
    simulation = simulations[0]
    series = simulation["series"][0]["series"]
    assert simulation["name"] == "Token price simulation"
    assert len(series) == 366


def test_run_optimal_control_simulation_n_simulations():
    simulations = run_optimal_control_simulation(n_simulations=2)
    assert len(simulations[0]["series"][0]["series"]) == 366
    assert len(simulations[1]["series"][0]["series"]) == 366
