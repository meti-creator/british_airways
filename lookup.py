from pathlib import Path

import pandas as pd


DATA_FILE = (
    Path(__file__).resolve().parent
    / "data"
    / "British Airways Summer Schedule Dataset - Forage Data Science Task 1.xlsx"
)


def load_schedule() -> pd.DataFrame:
    """Load the British Airways summer schedule from the data folder."""
    return pd.read_excel(DATA_FILE, sheet_name=0)


if __name__ == "__main__":
    schedule = load_schedule()
    print(f"Loaded {len(schedule)} rows and {len(schedule.columns)} columns.")
    print(schedule.head())

def estimate_eligible(haul, time_of_day, seats, tier):
    table = pd.read_csv("../data/lounge_eligibility_lookup.csv")
    col = {1: "tier1_pct_potential", 2: "tier2_pct", 3: "tier3_pct"}[tier]
    row = table[(table["HAUL"] == haul.upper()) & (table["TIME_OF_DAY"] == time_of_day.title())]
    if row.empty:
        raise ValueError("No matching group in the lookup table")
    return round(seats * row[col].iloc[0] / 100, 1)