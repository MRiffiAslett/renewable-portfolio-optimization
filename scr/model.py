import pandas as pd
import numpy as np
from pyomo.environ import (
    ConcreteModel, Var, Objective, Constraint, NonNegativeReals, minimize, SolverFactory, Param, RangeSet
)
from pyomo.core import Suffix
from pyomo.opt import TerminationCondition

def build_two_stage_model(data_df: pd.DataFrame, num_scenarios: int = 5, alpha_cvar: float = 0.95):
    """
    Build a two-stage stochastic optimization Pyomo model for renewable portfolio design.
    Incorporates CVaR for risk aversion.

    Parameters:
    -----------
    data_df : pd.DataFrame
        Real historical data with columns, e.g., ["timestamp", "demand"] (and potentially price).
    num_scenarios : int
        Number of scenarios for stochastic modeling. This example splits the data into subsets.
    alpha_cvar : float
        Confidence level for CVaR (0 < alpha_cvar < 1).

    Returns:
    --------
    model : pyomo.environ.ConcreteModel
        The constructed two-stage Pyomo model.
    """
 
    demand_scenarios = []
    chunk_size = len(data_df) // num_scenarios

    for i in range(num_scenarios):
        scenario_data = data_df.iloc[i*chunk_size : (i+1)*chunk_size]
        demand_scenarios.append(scenario_data["demand"].values)

    # Basic parameters
    bigM = 1e6  # large constant for constraints
    time_points_per_scenario = chunk_size

    # Create model
    model = ConcreteModel()

     model.SCENARIOS = RangeSet(0, num_scenarios-1)
    model.TIME = RangeSet(0, time_points_per_scenario-1)
 
    model.cost_of_wind = Param(initialize=1000.0, mutable=True)
    model.cost_of_solar = Param(initialize=800.0, mutable=True)

    # Demand data for each scenario/time
    def demand_init(model, s, t):
        return demand_scenarios[s][t]
    model.demand = Param(model.SCENARIOS, model.TIME, initialize=demand_init, mutable=True)

    # Variables
    # First-stage: capacity decisions (MW)
    model.wind_capacity = Var(domain=NonNegativeReals)
    model.solar_capacity = Var(domain=NonNegativeReals)

     
    model.gen_wind = Var(model.SCENARIOS, model.TIME, domain=NonNegativeReals)
    model.gen_solar = Var(model.SCENARIOS, model.TIME, domain=NonNegativeReals)
    model.load_shed = Var(model.SCENARIOS, model.TIME, domain=NonNegativeReals)

     
    model.excess_cost = Var(model.SCENARIOS, domain=NonNegativeReals)
     model.t_cvar = Var(domain=NonNegativeReals)

     
    def wind_gen_limit_rule(model, s, t):
        # e.g. generation cannot exceed capacity
        return model.gen_wind[s, t] <= model.wind_capacity
    model.wind_gen_limit = Constraint(model.SCENARIOS, model.TIME, rule=wind_gen_limit_rule)

    def solar_gen_limit_rule(model, s, t):
        return model.gen_solar[s, t] <= model.solar_capacity
    model.solar_gen_limit = Constraint(model.SCENARIOS, model.TIME, rule=solar_gen_limit_rule)

     
    def demand_rule(model, s, t):
        return model.demand[s,t] <= model.gen_wind[s,t] + model.gen_solar[s,t] + model.load_shed[s,t]
    model.demand_constraint = Constraint(model.SCENARIOS, model.TIME, rule=demand_rule)

     
    penalty_of_load_shed = 2000.0

    def scenario_cost_rule(model, s):
         time_cost = sum(model.load_shed[s, t] * penalty_of_load_shed for t in model.TIME)
        invest_cost = model.wind_capacity * model.cost_of_wind + model.solar_capacity * model.cost_of_solar
        return model.excess_cost[s] >= invest_cost + time_cost
    model.excess_cost_constraint = Constraint(model.SCENARIOS, rule=scenario_cost_rule)

    # 4) CVaR definition: t_cvar >= average of (excess_cost_s - t_cvar)+ / (1-alpha)
    def cvar_constraint_rule(model, s):
        return model.excess_cost[s] - model.t_cvar <= 0
    model.cvar_constraint = Constraint(model.SCENARIOS, rule=cvar_constraint_rule)
 

    lambda_risk = 0.3  

    def objective_rule(model):
         avg_cost = sum(model.excess_cost[s] for s in model.SCENARIOS) / num_scenarios
         max_cost = max(model.excess_cost[s] for s in range(num_scenarios))
        return avg_cost + lambda_risk * max_cost

    model.obj = Objective(rule=objective_rule, sense=minimize)

    return model

def solve_model(model):
    """
    Solve the Pyomo model and return results.
    """
    solver = SolverFactory("glpk")  # or cbc, gurobi, cplex, etc.
    results = solver.solve(model, tee=False)
    if (results.solver.termination_condition == TerminationCondition.optimal) or \
       (results.solver.termination_condition == TerminationCondition.feasible):
        print("Solver finished with a feasible/optimal solution.")
    else:
        print("Solver finished with status:", results.solver.termination_condition)

    return model, results
