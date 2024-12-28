# Stochastic Optimization for Renewable Energy Portfolio Design

This repository demonstrates a research-driven approach to designing an optimal portfolio of renewable energy assets (such as wind and solar) in the face of uncertain electricity demand and prices. The project uses **real** data from the U.S. Energy Information Administration (EIA) to construct and solve a **two-stage stochastic optimization** model in Python with Pyomo. To address uncertainty in a risk-averse manner, we apply techniques from **Conditional Value-at-Risk (CVaR)**, thereby emphasizing both expected costs and their worst-case tails.

## Project Structure

All files are organized so that data can be fetched, cleaned, and then used directly in the stochastic model.

- **data/**: Contains the downloaded time-series of electricity demand.
- **src/**: Includes Python scripts for:
  - Data fetching (`data_fetch.py`)
  - Model definition (`model.py`)
  - Main execution workflow (`main.py`)
- **requirements.txt**: Lists necessary Python libraries.
- **README.md**: Provides the project overview.

## Getting Started

To replicate the experiments, install the required dependencies:
```bash
pip install -r requirements.txt
```

Next, obtain an EIA API key (available free from the EIA Open Data website) and set it as an environment variable or in a local `.env` file. Once your key is properly set, navigate to `src` and run:
```bash
python main.py
```

This script automatically fetches real data from EIA, saves it to `data/eia_data.csv`, and solves the stochastic optimization model. Results (such as optimal capacities for wind and solar) will appear in the console output.

## Methodology

The methodology implemented here draws directly upon established research in stochastic programming. We take inspiration from:

- Birge and Louveaux (2011)
- Shapiro, Dentcheva, and Ruszczyński (2009)

The decision-making problem is structured as a **two-stage model**:
1. **First Stage**: Invest in generation capacities before demand uncertainties are realized.
2. **Second Stage**: Adjust operational decisions—how much wind or solar to dispatch, or how much load to shed—based on observed demand.

We incorporate **Conditional Value-at-Risk (CVaR)** to ensure risk-averse behavior by penalizing high-cost scenarios more heavily than lower-cost scenarios. This follows Rockafellar and Uryasev (2000), where CVaR is shown to provide a coherent and tractable measure of tail risk.

The mathematical model can be expressed as a **Mixed-Integer Linear Program (MILP)** if certain decisions, such as turbine block purchases, are integrally constrained. In this example, we primarily model capacity as continuous variables for simplicity, but Pyomo can handle discrete (integer) decisions as well. Solvers like **GLPK**, **CBC**, **Gurobi**, or **CPLEX** can be used to solve the resulting MILP.

## Real Data Usage

All demand data in this repository is sourced programmatically via the **EIA API**. By default, we fetch hourly demand from the ERCOT region (Texas). However, the code can be adapted easily to query any other region supported by EIA or to incorporate data from other providers for detailed price series. This ensures the study remains grounded in **real-world conditions** rather than simulated or synthetic data.

## License

This project is released under the **MIT License**.

## References

- Birge, J. R., & Louveaux, F. (2011). *Introduction to Stochastic Programming* (2nd ed.). Springer.
- Rockafellar, R. T., & Uryasev, S. (2000). Optimization of conditional value-at-risk. *Journal of Risk, 2*(3), 21–42.
- Shapiro, A., Dentcheva, D., & Ruszczyński, A. (2009). *Lectures on Stochastic Programming: Modeling and Theory*. SIAM.
