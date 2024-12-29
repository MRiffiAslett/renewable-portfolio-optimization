# Stochastic Optimization for Renewable Energy Portfolio Design

This repository demonstrates a research-driven approach to designing an optimal portfolio of renewable energy assets (such as wind and solar) in the face of uncertain electricity demand and prices. The project uses **real** data from the U.S. Energy Information Administration (EIA) to construct and solve a **two-stage stochastic optimization** model in Python with Pyomo. To address uncertainty in a risk-averse manner, we apply techniques from **Conditional Value-at-Risk (CVaR)**, thereby emphasizing both expected costs and their worst-case tails.

## Methodology

The methodology implemented here draws directly upon established research in stochastic programming. We take inspiration from:

- Birge and Louveaux (2011)
- Shapiro, Dentcheva, and Ruszczyński (2009)

The decision-making problem is structured as a **two-stage model**:
1. **First Stage**: Invest in generation capacities before demand uncertainties are realized.
2. **Second Stage**: Adjust operational decisions—how much wind or solar to dispatch, or how much load to shed—based on observed demand.

We incorporate **Conditional Value-at-Risk (CVaR)** to ensure risk-averse behavior by penalizing high-cost scenarios more heavily than lower-cost scenarios. This follows Rockafellar and Uryasev (2000), where CVaR is shown to provide a coherent and tractable measure of tail risk.

The mathematical model can be expressed as a **Mixed-Integer Linear Program (MILP)** if certain decisions, such as turbine block purchases, are integrally constrained. In this example, we primarily model capacity as continuous variables for simplicity, but Pyomo can handle discrete (integer) decisions as well. Solvers like **GLPK**, **CBC**, **Gurobi**, or **CPLEX** can be used to solve the resulting MILP.



## References

- Birge, J. R., & Louveaux, F. (2011). *Introduction to Stochastic Programming* (2nd ed.). Springer.
- Rockafellar, R. T., & Uryasev, S. (2000). Optimization of conditional value-at-risk. *Journal of Risk, 2*(3), 21–42.
- Shapiro, A., Dentcheva, D., & Ruszczyński, A. (2009). *Lectures on Stochastic Programming: Modeling and Theory*. SIAM.

