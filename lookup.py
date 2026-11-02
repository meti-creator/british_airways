from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_FILE = DATA_DIR / "British Airways Summer Schedule Dataset - Forage Data Science Task 1.xlsx"
LOOKUP_FILE = DATA_DIR / "lounge_eligibility_lookup.csv"


def load_schedule() -> pd.DataFrame:
    """Load the British Airways summer schedule from the data folder."""
    return pd.read_excel(DATA_FILE, sheet_name=0)


def estimate_eligible(haul, time_of_day, seats, tier):
    """Estimate how many passengers in a flight group are eligible for a lounge tier."""
    table = pd.read_csv(LOOKUP_FILE)
    tier_map = {1: "tier1_pct_potential", 2: "tier2_pct", 3: "tier3_pct"}

    try:
        tier = int(tier)
    except (TypeError, ValueError) as exc:
        raise ValueError("Tier must be one of 1, 2, or 3") from exc

    if tier not in tier_map:
        raise ValueError("Tier must be one of 1, 2, or 3")

    col = tier_map[tier]
    haul_key = str(haul).upper()
    time_key = str(time_of_day).title()
    row = table[(table["HAUL"] == haul_key) & (table["TIME_OF_DAY"] == time_key)]
    if row.empty:
        raise ValueError("No matching group in the lookup table")
    return round(seats * row[col].iloc[0] / 100, 1)


if __name__ == "__main__":
    schedule = load_schedule()
    print(f"Loaded {len(schedule)} rows and {len(schedule.columns)} columns.")
    print(schedule.head())