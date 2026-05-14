"""
Generate pedagogically useful subsets of real waiting-time data
for MATH 476 / 563 assignments.

This script:
- loads NYC 311 data (filtered at source)
- computes inter-arrival times
- searches for subsets (n≈20)
- compares exact vs CLT inference
- selects a good subset and prints the sample
"""

import pandas as pd
import numpy as np
from scipy.stats import chi2, norm

print("Starting script...")

# --- LOAD DATA (server-side filtered) ---
url = (
    "https://data.cityofnewyork.us/resource/erm2-nwe9.csv"
    "?complaint_type=Noise%20-%20Residential"
    "&$limit=50000"
)

print("Downloading data from NYC Open Data...")
df = pd.read_csv(url, low_memory=False)

print("Raw data shape:", df.shape)

# --- CLEAN / PREP ---
df["created_date"] = pd.to_datetime(df["created_date"])

df = df.rename(columns={
    "created_date": "Created Date",
    "complaint_type": "Complaint Type"
})

print("Columns:", list(df.columns)[:10])

# --- SORT ---
df = df.sort_values("Created Date")

print("First timestamps:")
print(df["Created Date"].head())

# --- COMPUTE INTER-ARRIVAL TIMES ---
times = df["Created Date"].values.astype("datetime64[s]")
waits = np.diff(times).astype(int)

# remove zeros and extreme outliers (optional light cleaning)
waits = waits[waits > 0]

print("Number of waiting times:", len(waits))
print("First 10 waits:", waits[:10])

# --- PARAMETERS ---
theta0 = 60
n = 20
alpha = 0.05

def analyze(sample):
    S = np.sum(sample)
    xbar = np.mean(sample)

    # exact
    T = 2 * S / theta0
    p_exact = 1 - chi2.cdf(T, 2 * n)
    thetaU_exact = 2 * S / chi2.ppf(alpha, 2 * n)

    # CLT
    Z = (xbar - theta0) / (theta0 / np.sqrt(n))
    p_clt = 1 - norm.cdf(Z)
    thetaU_clt = xbar + norm.ppf(0.95) * xbar / np.sqrt(n)

    return {
        "mean": xbar,
        "p_exact": p_exact,
        "p_clt": p_clt,
        "diff": abs(p_exact - p_clt),
        "thetaU_exact": thetaU_exact,
        "thetaU_clt": thetaU_clt
    }

# --- SEARCH FOR GOOD SUBSETS ---
print("\nSearching for candidate subsets...")

results = []

for seed in range(200):
    if seed % 20 == 0:
        print(f"Processing seed {seed}...")

    rng = np.random.default_rng(seed)
    sample = rng.choice(waits, size=n, replace=False)
    stats = analyze(sample)
    stats["seed"] = seed
    results.append(stats)

res = pd.DataFrame(results)

print("\nFinished generating candidates.")
print("Total candidates:", len(res))

# --- FILTER ---
good = res[
    (res["p_exact"] > 0.02) &
    (res["p_exact"] < 0.15) &
    (res["diff"] > 0.01)
]

good_sorted = good.sort_values("p_exact")

print("\nTop candidate subsets:")
print(good_sorted.head(10))

# --- SELECT BEST ---
best = good_sorted.iloc[0]
best_seed = int(best["seed"])

print("\nSelected seed:", best_seed)
print("Summary stats:", best.to_dict())

# --- EXTRACT FINAL SAMPLE ---
rng = np.random.default_rng(best_seed)
sample = rng.choice(waits, size=n, replace=False)

print("\nFinal sample (n=20):")
print(sample)

print("\nSorted sample (nicer for assignment):")
print(np.sort(sample))