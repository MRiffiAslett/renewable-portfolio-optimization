import os
import pandas as pd
from data_fetch import main as data_fetch_main
from model import build_two_stage_model, solve_model

def main():
    """
    Orchestrate the full process:
    1. Fetch real data from EIA and save to CSV.
    2. Load data, build model, solve it.
    3. Display results.
    """
   
    print("Fetching data from EIA...")
    data_fetch_main()

    data_path = "../data/eia_data.csv"
    data_df = pd.read_csv(data_path)

    print(f"Data loaded. Shape: {data_df.shape}")
    print(data_df.head())

    model = build_two_stage_model(data_df, num_scenarios=5, alpha_cvar=0.95)


    model, results = solve_model(model)

    print("\nOptimization Results:")
    print(f"Wind capacity (MW) = {model.wind_capacity.value}")
    print(f"Solar capacity (MW) = {model.solar_capacity.value}")

    
    scenario_costs = [model.excess_cost[s].value for s in model.SCENARIOS]
    print(f"Scenario costs: {scenario_costs}")
    print(f"Objective value: {model.obj.expr()}")

    

if __name__ == "__main__":
    main()
