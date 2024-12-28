import os
import requests
import pandas as pd
from dotenv import load_dotenv

def fetch_eia_data(api_key: str, frequency: str = "hourly") -> pd.DataFrame:
    """
    Fetch real electricity data (demand and optionally price) from EIA API.
    By default, it pulls hourly data for the ERCOT region.
    
    Parameters:
    -----------
    api_key : str
        Your EIA API key.
    frequency : str
        Data frequency (e.g., hourly, daily, etc.). This example uses hourly.
    
    Returns:
    --------
    data_df : pd.DataFrame
        A DataFrame with timestamp, demand (MW), and price if available.
    """

    series_id = "EBA.TEX-ALL.D.H"

    url = (
        f"https://api.eia.gov/v2/electricity/rto/region-data/data/"
        f"?api_key={api_key}"
        f"&frequency={frequency}"
        f"&data[0]=value"
        f"&facets[respondent][]=TEX"  # TEX = ERCOT region
        f"&facets[type][]=D"
        f"&start=2023-01-01T00"       # Adjust date range as needed
        f"&end=2023-03-01T23"
        f"&sort[0][column]=period"
        f"&sort[0][direction]=asc"
        f"&offset=0"
        f"&length=5000"
    )

    r = requests.get(url)
    r.raise_for_status()  
    json_data = r.json()
    records = json_data["response"]["data"]

    data_df = pd.DataFrame(records)

    data_df = data_df.rename(columns={"value": "demand", "period": "timestamp"})
    data_df["timestamp"] = pd.to_datetime(data_df["timestamp"], utc=True)

    # Sort by timestamp
    data_df = data_df.sort_values("timestamp").reset_index(drop=True)

    return data_df

def save_data_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """
    Save fetched data to CSV.
    """
    df.to_csv(filepath, index=False)

def main():
    load_dotenv()
    api_key = os.getenv("EIA_API_KEY")

    df = fetch_eia_data(api_key=api_key, frequency="hourly")
    save_data_to_csv(df, "../data/eia_data.csv")
    print("Data fetched and saved to ../data/eia_data.csv")

if __name__ == "__main__":
    main()
