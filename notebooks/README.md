# Modeling Lounge Eligibility at Heathrow Terminal 3

A data science project based on the British Airways job simulation on Forage (Task 1). The goal is to help British Airways plan future lounge demand at Terminal 3 by estimating **what share of passengers are eligible for each lounge tier**, grouped by flight category rather than by individual flight.

**Author:** Meti Assefa Belachew ([GitHub](https://github.com/meti-creator))

---

## The business question

British Airways plans lounge space years ahead, when specific flight numbers and aircraft are unknown. So the model must be built on **stable, high-level groups** and produce a **reusable lookup table** that can be applied to any future schedule.

| Tier | Lounge | Who is eligible |
|---|---|---|
| 1 | Concorde Room | First Class customers, BA premier cardholders, BA Gold Guest List members |
| 2 | First Lounge | BA Gold Members |
| 3 | Club Lounge | BA Silver cardholders, Club World (business class) customers |

> **Note:** There is currently no Concorde Room at Terminal 3. Tier 1 results are treated as **potential demand only**, not a confirmed development.

## Data

`data/British_Airways_Summer_Schedule_Dataset_-_Forage_Data_Science_Task_1.xlsx`: a summer schedule of 10,000 flights. Each row is one flight, with its haul type (short/long), time of day, arrival region, seats per cabin, and the number of passengers eligible for each lounge tier (`TIER1_ELIGIBLE_PAX`, `TIER2_ELIGIBLE_PAX`, `TIER3_ELIGIBLE_PAX`).

## Method

1. **Total seats** per flight = first + business + economy seats.
2. **Group** flights by `HAUL` and `TIME_OF_DAY` (8 groups).
3. For each group, **sum** the eligible passengers per tier and the total seats.
4. **Divide once per group:** `eligible passengers / total seats * 100`.

Summing first and dividing once (instead of averaging per-flight percentages) keeps large aircraft from being under- or over-weighted.

## Result: lookup table

Share of seats held by passengers eligible for each lounge (%).

| Haul | Time of day | Flights | Tier 1 (potential) | Tier 2 | Tier 3 |
|---|---|---|---|---|---|
| Long | Morning | 1,461 | 0.21 | 2.79 | 10.63 |
| Long | Lunchtime | 435 | 0.18 | 2.71 | 10.38 |
| Long | Afternoon | 939 | 0.20 | 2.77 | 10.52 |
| Long | Evening | 1,190 | 0.21 | 2.67 | 10.26 |
| Short | Morning | 2,069 | 0.34 | 4.36 | 16.74 |
| Short | Lunchtime | 757 | 0.39 | 4.55 | 17.28 |
| Short | Afternoon | 1,366 | 0.34 | 4.31 | 16.59 |
| Short | Evening | 1,783 | 0.33 | 4.45 | 17.00 |

Saved as `data/lounge_eligibility_lookup.csv`.

### How to use it

```python
estimate_eligible("short", "lunchtime", 180, 3)   # about 31 eligible passengers
```

Find a future flight's group, read the percentage, and multiply by its seat count.

## Key findings

- **Haul type is what separates the groups.** Short-haul flights have a higher eligible share than long-haul (Tier 3: about 17% vs. about 10%).
- **Time of day barely changes the percentages** (under 1 percentage point within each haul type). It is kept because flight volume, and therefore lounge crowding, peaks in the morning, even though the share of eligible passengers is stable.
- **Arrival region adds nothing beyond haul in this dataset.** All short-haul flights go to Europe, and the three long-haul regions (Asia, Middle East, North America) have nearly identical percentages.
- **First Class seats do not translate into Tier 1 counts.** Of 1,652 flights with a First Class cabin, 1,054 show zero Tier 1 eligible passengers, and I found no pattern by aircraft or region.

## Assumptions and limitations

- Total seats is used as a proxy for total passengers (flights are assumed to be full).
- The data covers one summer; future summers are assumed to look similar. This finds a pattern, not a trend over time.
- Tier 1 is hypothetical because there is no Concorde Room at Terminal 3.
- The cause of the zero Tier 1 counts on First Class flights is not explained by the dataset, so the eligible-passenger columns were used as given.
- Results are totals across the whole summer, not peak-hour demand. A natural next step is to look at how many flights depart in the same hour.

## Project structure

```
ba-lounge-eligibility/
├── data/
│   ├── British_Airways_Summer_Schedule_Dataset_-_Forage_Data_Science_Task_1.xlsx
│   └── lounge_eligibility_lookup.csv
├── notebooks/
│   └── analysis.ipynb
├── .gitignore
└── README.md
```

## How to run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install pandas openpyxl jupyter matplotlib
```

Then open `notebooks/analysis.ipynb` in VS Code and run the cells in order.

## Tools

Python, pandas, Jupyter, VS Code.