# Infrastructure-Centric Blockchain Tokenomics Package

This Python package implements the concepts outlined in the research article [A Control Theoretic Approach to Infrastructure-Centric Blockchain Tokenomics](https://arxiv.org/pdf/2210.12881.pdf) by Oguzhan Akcin, Robert P. Streit, Benjamin Oommen, Sriram Vishwanath, and Sandeep Chinchali.

Overview
The package focuses on designing and simulating token economies for blockchain-based physical infrastructure systems. The main goal is to create a dynamic and adaptable token economy that incentivizes participation while maintaining equilibrium and stability. The package provides a framework for modeling, simulating, and optimizing token economies in infrastructure networks.

## Project Files

- token_simulation.py: This is the main file for running simulations of the token economy in the infrastructure network.
- src/token_economy.py: This module defines the TokenEconomy class, which contains the definitions for the cost and dynamics of the system. It provides the foundation for modeling the token economy.
- src/token_dynamics.py: Here, the evolution of token prices and consumer behavior is defined. This module captures the dynamic changes in the token economy based on various factors.
- src/game.py: Implements a Stackelberg game that involves both consumers and the organization. This game aims to establish strategic pricing and goals for both parties to achieve a balanced token economy.
- src/solver.py: Implements an ILQRSolver, which is utilized for optimization purposes within the token economy simulation.

### Usage

To simulate the infrastructure-centric token economy, you can use the token_simulation.py file. It imports the necessary components from the src directory to create a comprehensive simulation of the token economy.

```shell
python simulation.py
```
